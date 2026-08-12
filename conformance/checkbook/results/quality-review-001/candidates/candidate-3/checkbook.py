import csv
import io
import sqlite3
from datetime import date


class CheckbookError(Exception):
    def __init__(self, code: str, operation_id: str | None = None, message: str = ""):
        super().__init__(message or code)
        self.code = code
        self.operation_id = operation_id


class Checkbook:
    def __init__(self, database_path: str):
        self._conn = sqlite3.connect(database_path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._init_db()

    def create_account(
        self,
        account_id: str,
        currency: str,
        opening_balance_minor: int,
        operation_id: str,
    ) -> dict:
        self._require_operation_id(operation_id)
        self._require_identifier(account_id, "invalid_account_id", operation_id)
        self._require_currency(currency, operation_id)
        self._require_minor_amount(opening_balance_minor, operation_id)
        with self._conn:
            if self._account_row(account_id) is not None:
                self._fail("account_exists", operation_id)
            self._conn.execute(
                """
                INSERT INTO accounts(account_id, currency, opening_balance_minor, closed_through_date)
                VALUES (?, ?, ?, NULL)
                """,
                (account_id, currency, opening_balance_minor),
            )
            self._audit("account_created", operation_id, account_id)
        return self.get_account(account_id)

    def record_transaction(
        self,
        account_id: str,
        transaction_id: str,
        posted_date: str,
        amount_minor: int,
        description: str,
        operation_id: str,
    ) -> dict:
        self._require_operation_id(operation_id)
        self._require_identifier(account_id, "invalid_account_id", operation_id)
        self._require_identifier(transaction_id, "invalid_transaction_id", operation_id)
        posted = self._require_date(posted_date, operation_id)
        self._require_minor_amount(amount_minor, operation_id)
        self._require_description(description, operation_id)
        with self._conn:
            account = self._require_account(account_id, operation_id)
            self._reject_closed(account["closed_through_date"], posted, operation_id)
            if self._transaction_row(transaction_id) is not None:
                self._fail("transaction_exists", operation_id)
            self._insert_transaction(
                transaction_id=transaction_id,
                account_id=account_id,
                posted_date=posted,
                amount_minor=amount_minor,
                description=description,
                reversal_of=None,
                source=None,
                external_id=None,
            )
            self._audit("transaction_recorded", operation_id, account_id, transaction_id)
        return self.get_transaction(transaction_id)

    def edit_transaction(
        self,
        transaction_id: str,
        expected_version: int,
        posted_date: str,
        amount_minor: int,
        description: str,
        operation_id: str,
    ) -> dict:
        self._require_operation_id(operation_id)
        self._require_identifier(transaction_id, "invalid_transaction_id", operation_id)
        posted = self._require_date(posted_date, operation_id)
        self._require_version(expected_version, operation_id)
        self._require_minor_amount(amount_minor, operation_id)
        self._require_description(description, operation_id)
        with self._conn:
            tx = self._require_transaction(transaction_id, operation_id)
            if tx["version"] != expected_version:
                self._fail("stale_version", operation_id)
            if tx["reconciled"]:
                self._fail("reconciled_transaction", operation_id)
            account = self._require_account(tx["account_id"], operation_id)
            self._reject_closed(account["closed_through_date"], tx["posted_date"], operation_id)
            self._reject_closed(account["closed_through_date"], posted, operation_id)
            self._conn.execute(
                """
                UPDATE transactions
                SET posted_date = ?, amount_minor = ?, description = ?, version = version + 1
                WHERE transaction_id = ?
                """,
                (posted, amount_minor, description, transaction_id),
            )
            self._audit("transaction_edited", operation_id, tx["account_id"], transaction_id)
        return self.get_transaction(transaction_id)

    def mark_cleared(
        self,
        transaction_id: str,
        expected_version: int,
        operation_id: str,
    ) -> dict:
        self._require_operation_id(operation_id)
        self._require_identifier(transaction_id, "invalid_transaction_id", operation_id)
        self._require_version(expected_version, operation_id)
        with self._conn:
            tx = self._require_transaction(transaction_id, operation_id)
            if tx["version"] != expected_version:
                self._fail("stale_version", operation_id)
            if tx["cleared"]:
                self._fail("already_cleared", operation_id)
            account = self._require_account(tx["account_id"], operation_id)
            self._reject_closed(account["closed_through_date"], tx["posted_date"], operation_id)
            self._conn.execute(
                "UPDATE transactions SET cleared = 1, version = version + 1 WHERE transaction_id = ?",
                (transaction_id,),
            )
            self._audit("transaction_cleared", operation_id, tx["account_id"], transaction_id)
        return self.get_transaction(transaction_id)

    def import_csv(
        self,
        account_id: str,
        source: str,
        csv_text: str,
        operation_id: str,
    ) -> dict:
        self._require_operation_id(operation_id)
        self._require_identifier(account_id, "invalid_account_id", operation_id)
        self._require_identifier(source, "invalid_source", operation_id)
        rows = self._parse_csv(csv_text, operation_id)
        prepared = []
        seen = {}
        with self._conn:
            account = self._require_account(account_id, operation_id)
            closed = account["closed_through_date"]
            for external_id, posted, amount_minor, description in rows:
                self._reject_closed(closed, posted, operation_id)
                key = (source, external_id)
                normalized = (posted, amount_minor, description)
                if key in seen:
                    if seen[key] != normalized:
                        self._fail("duplicate_conflict", operation_id)
                    continue
                seen[key] = normalized
                existing = self._conn.execute(
                    """
                    SELECT transaction_id, posted_date, amount_minor, description
                    FROM transactions
                    WHERE account_id = ? AND source = ? AND external_id = ?
                    """,
                    (account_id, source, external_id),
                ).fetchone()
                if existing is not None:
                    current = (
                        existing["posted_date"],
                        existing["amount_minor"],
                        existing["description"],
                    )
                    if current != normalized:
                        self._fail("duplicate_conflict", operation_id)
                    prepared.append(("duplicate", existing["transaction_id"], external_id, posted, amount_minor, description))
                    continue
                transaction_id = self._import_transaction_id(account_id, source, external_id)
                if self._transaction_row(transaction_id) is not None:
                    self._fail("duplicate_conflict", operation_id)
                prepared.append(("insert", transaction_id, external_id, posted, amount_minor, description))
            inserted = 0
            duplicates = 0
            for action, transaction_id, external_id, posted, amount_minor, description in prepared:
                if action == "duplicate":
                    duplicates += 1
                    continue
                self._insert_transaction(
                    transaction_id=transaction_id,
                    account_id=account_id,
                    posted_date=posted,
                    amount_minor=amount_minor,
                    description=description,
                    reversal_of=None,
                    source=source,
                    external_id=external_id,
                )
                self._audit("transaction_imported", operation_id, account_id, transaction_id)
                inserted += 1
        return {"inserted": inserted, "duplicates": duplicates}

    def reconcile(
        self,
        account_id: str,
        statement_date: str,
        ending_balance_minor: int,
        operation_id: str,
    ) -> dict:
        self._require_operation_id(operation_id)
        self._require_identifier(account_id, "invalid_account_id", operation_id)
        statement = self._require_date(statement_date, operation_id)
        self._require_minor_amount(ending_balance_minor, operation_id)
        with self._conn:
            account = self._require_account(account_id, operation_id)
            self._reject_closed(account["closed_through_date"], statement, operation_id)
            reconciled_total = self._scalar(
                """
                SELECT COALESCE(SUM(amount_minor), 0)
                FROM transactions
                WHERE account_id = ? AND reconciled = 1
                """,
                (account_id,),
            )
            candidates = self._conn.execute(
                """
                SELECT transaction_id
                FROM transactions
                WHERE account_id = ?
                  AND cleared = 1
                  AND reconciled = 0
                  AND posted_date <= ?
                ORDER BY posted_date, transaction_id
                """,
                (account_id, statement),
            ).fetchall()
            candidate_total = self._scalar(
                """
                SELECT COALESCE(SUM(amount_minor), 0)
                FROM transactions
                WHERE account_id = ?
                  AND cleared = 1
                  AND reconciled = 0
                  AND posted_date <= ?
                """,
                (account_id, statement),
            )
            actual = account["opening_balance_minor"] + reconciled_total + candidate_total
            if actual != ending_balance_minor:
                self._fail("reconciliation_mismatch", operation_id)
            for row in candidates:
                self._conn.execute(
                    "UPDATE transactions SET reconciled = 1 WHERE transaction_id = ?",
                    (row["transaction_id"],),
                )
            self._audit("account_reconciled", operation_id, account_id)
        return {
            "account_id": account_id,
            "statement_date": statement,
            "ending_balance_minor": ending_balance_minor,
        }

    def reverse_reconciled_transaction(
        self,
        original_transaction_id: str,
        reversal_transaction_id: str,
        posted_date: str,
        operation_id: str,
    ) -> dict:
        self._require_operation_id(operation_id)
        self._require_identifier(original_transaction_id, "invalid_transaction_id", operation_id)
        self._require_identifier(reversal_transaction_id, "invalid_transaction_id", operation_id)
        posted = self._require_date(posted_date, operation_id)
        with self._conn:
            original = self._require_transaction(original_transaction_id, operation_id)
            if not original["reconciled"]:
                self._fail("not_reconciled", operation_id)
            account = self._require_account(original["account_id"], operation_id)
            self._reject_closed(account["closed_through_date"], posted, operation_id)
            if self._transaction_row(reversal_transaction_id) is not None:
                self._fail("transaction_exists", operation_id)
            existing = self._conn.execute(
                "SELECT 1 FROM transactions WHERE reversal_of = ?",
                (original_transaction_id,),
            ).fetchone()
            if existing is not None:
                self._fail("reversal_exists", operation_id)
            self._insert_transaction(
                transaction_id=reversal_transaction_id,
                account_id=original["account_id"],
                posted_date=posted,
                amount_minor=-original["amount_minor"],
                description=original["description"],
                reversal_of=original_transaction_id,
                source=None,
                external_id=None,
            )
            self._audit(
                "transaction_reversed",
                operation_id,
                original["account_id"],
                reversal_transaction_id,
            )
        return self.get_transaction(reversal_transaction_id)

    def close_period(
        self,
        account_id: str,
        through_date: str,
        operation_id: str,
    ) -> dict:
        self._require_operation_id(operation_id)
        self._require_identifier(account_id, "invalid_account_id", operation_id)
        through = self._require_date(through_date, operation_id)
        with self._conn:
            account = self._require_account(account_id, operation_id)
            current = account["closed_through_date"]
            if current is not None and through < current:
                self._fail("close_backwards", operation_id)
            self._conn.execute(
                "UPDATE accounts SET closed_through_date = ? WHERE account_id = ?",
                (through, account_id),
            )
            self._audit("period_closed", operation_id, account_id)
        return self.get_account(account_id)

    def get_account(self, account_id: str) -> dict:
        self._require_identifier(account_id, "invalid_account_id", None)
        row = self._account_row(account_id)
        if row is None:
            self._fail("account_not_found", None)
        return {
            "account_id": row["account_id"],
            "currency": row["currency"],
            "opening_balance_minor": row["opening_balance_minor"],
            "closed_through_date": row["closed_through_date"],
        }

    def get_transaction(self, transaction_id: str) -> dict:
        self._require_identifier(transaction_id, "invalid_transaction_id", None)
        row = self._transaction_row(transaction_id)
        if row is None:
            self._fail("transaction_not_found", None)
        return self._transaction_dict(row)

    def list_transactions(self, account_id: str) -> list[dict]:
        self._require_identifier(account_id, "invalid_account_id", None)
        self._require_account(account_id, None)
        rows = self._conn.execute(
            """
            SELECT *
            FROM transactions
            WHERE account_id = ?
            ORDER BY posted_date, transaction_id
            """,
            (account_id,),
        ).fetchall()
        return [self._transaction_dict(row) for row in rows]

    def list_audit_events(self) -> list[dict]:
        rows = self._conn.execute(
            """
            SELECT event_id, operation_id, event_type, account_id, transaction_id
            FROM audit_events
            ORDER BY event_id
            """
        ).fetchall()
        return [
            {
                "event_id": row["event_id"],
                "operation_id": row["operation_id"],
                "event_type": row["event_type"],
                "account_id": row["account_id"],
                "transaction_id": row["transaction_id"],
            }
            for row in rows
        ]

    def _init_db(self) -> None:
        self._conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS accounts(
                account_id TEXT PRIMARY KEY,
                currency TEXT NOT NULL,
                opening_balance_minor INTEGER NOT NULL,
                closed_through_date TEXT
            );
            CREATE TABLE IF NOT EXISTS transactions(
                transaction_id TEXT PRIMARY KEY,
                account_id TEXT NOT NULL REFERENCES accounts(account_id),
                posted_date TEXT NOT NULL,
                amount_minor INTEGER NOT NULL,
                description TEXT NOT NULL,
                version INTEGER NOT NULL,
                cleared INTEGER NOT NULL,
                reconciled INTEGER NOT NULL,
                reversal_of TEXT REFERENCES transactions(transaction_id),
                source TEXT,
                external_id TEXT
            );
            CREATE UNIQUE INDEX IF NOT EXISTS transactions_import_identity
            ON transactions(account_id, source, external_id);
            CREATE UNIQUE INDEX IF NOT EXISTS transactions_reversal_once
            ON transactions(reversal_of)
            WHERE reversal_of IS NOT NULL;
            CREATE TABLE IF NOT EXISTS audit_events(
                event_id INTEGER PRIMARY KEY,
                operation_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                account_id TEXT NOT NULL,
                transaction_id TEXT
            );
            """
        )

    def _parse_csv(self, csv_text: str, operation_id: str) -> list[tuple[str, str, int, str]]:
        reader = csv.reader(io.StringIO(csv_text))
        try:
            header = next(reader)
        except StopIteration:
            self._fail("csv_header_mismatch", operation_id)
        if header != ["external_id", "posted_date", "amount_minor", "description"]:
            self._fail("csv_header_mismatch", operation_id)
        rows = []
        for row in reader:
            if len(row) != 4:
                self._fail("invalid_csv_row", operation_id)
            external_id, posted_date, amount_minor, description = row
            self._require_identifier(external_id, "invalid_external_id", operation_id)
            posted = self._require_date(posted_date, operation_id)
            try:
                amount = int(amount_minor)
            except (TypeError, ValueError):
                self._fail("invalid_amount", operation_id)
            self._require_minor_amount(amount, operation_id)
            self._require_description(description, operation_id)
            rows.append((external_id, posted, amount, description))
        return rows

    def _insert_transaction(
        self,
        transaction_id: str,
        account_id: str,
        posted_date: str,
        amount_minor: int,
        description: str,
        reversal_of: str | None,
        source: str | None,
        external_id: str | None,
    ) -> None:
        self._conn.execute(
            """
            INSERT INTO transactions(
                transaction_id, account_id, posted_date, amount_minor, description,
                version, cleared, reconciled, reversal_of, source, external_id
            )
            VALUES (?, ?, ?, ?, ?, 1, 0, 0, ?, ?, ?)
            """,
            (
                transaction_id,
                account_id,
                posted_date,
                amount_minor,
                description,
                reversal_of,
                source,
                external_id,
            ),
        )

    def _audit(
        self,
        event_type: str,
        operation_id: str,
        account_id: str,
        transaction_id: str | None = None,
    ) -> None:
        self._conn.execute(
            """
            INSERT INTO audit_events(operation_id, event_type, account_id, transaction_id)
            VALUES (?, ?, ?, ?)
            """,
            (operation_id, event_type, account_id, transaction_id),
        )

    def _account_row(self, account_id: str):
        return self._conn.execute(
            "SELECT * FROM accounts WHERE account_id = ?",
            (account_id,),
        ).fetchone()

    def _transaction_row(self, transaction_id: str):
        return self._conn.execute(
            "SELECT * FROM transactions WHERE transaction_id = ?",
            (transaction_id,),
        ).fetchone()

    def _require_account(self, account_id: str, operation_id: str | None):
        row = self._account_row(account_id)
        if row is None:
            self._fail("account_not_found", operation_id)
        return row

    def _require_transaction(self, transaction_id: str, operation_id: str | None):
        row = self._transaction_row(transaction_id)
        if row is None:
            self._fail("transaction_not_found", operation_id)
        return row

    def _scalar(self, sql: str, params: tuple):
        return self._conn.execute(sql, params).fetchone()[0]

    def _transaction_dict(self, row: sqlite3.Row) -> dict:
        return {
            "transaction_id": row["transaction_id"],
            "account_id": row["account_id"],
            "posted_date": row["posted_date"],
            "amount_minor": row["amount_minor"],
            "description": row["description"],
            "version": row["version"],
            "cleared": bool(row["cleared"]),
            "reconciled": bool(row["reconciled"]),
            "reversal_of": row["reversal_of"],
            "source": row["source"],
            "external_id": row["external_id"],
        }

    def _import_transaction_id(self, account_id: str, source: str, external_id: str) -> str:
        return f"import:{account_id}:{source}:{external_id}"

    def _require_operation_id(self, operation_id: str) -> None:
        self._require_identifier(operation_id, "invalid_operation_id", operation_id)

    def _require_identifier(self, value: str, code: str, operation_id: str | None) -> None:
        if not isinstance(value, str) or not value:
            self._fail(code, operation_id)

    def _require_currency(self, currency: str, operation_id: str) -> None:
        if not isinstance(currency, str) or len(currency) != 3 or currency.upper() != currency or not currency.isalpha():
            self._fail("invalid_currency", operation_id)

    def _require_minor_amount(self, amount_minor: int, operation_id: str | None) -> None:
        if isinstance(amount_minor, bool) or not isinstance(amount_minor, int):
            self._fail("invalid_amount", operation_id)

    def _require_version(self, expected_version: int, operation_id: str | None) -> None:
        if isinstance(expected_version, bool) or not isinstance(expected_version, int) or expected_version < 1:
            self._fail("invalid_version", operation_id)

    def _require_description(self, description: str, operation_id: str | None) -> None:
        if not isinstance(description, str):
            self._fail("invalid_description", operation_id)

    def _require_date(self, value: str, operation_id: str | None) -> str:
        if not isinstance(value, str):
            self._fail("invalid_date", operation_id)
        try:
            parsed = date.fromisoformat(value)
        except ValueError:
            self._fail("invalid_date", operation_id)
        if value != parsed.isoformat():
            self._fail("invalid_date", operation_id)
        return value

    def _reject_closed(self, closed_through_date: str | None, posted_date: str, operation_id: str | None) -> None:
        if closed_through_date is not None and posted_date <= closed_through_date:
            self._fail("closed_period", operation_id)

    def _fail(self, code: str, operation_id: str | None) -> None:
        raise CheckbookError(code, operation_id)
