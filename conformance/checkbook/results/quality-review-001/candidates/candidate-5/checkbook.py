import csv
import hashlib
import sqlite3
from datetime import date
from io import StringIO


class CheckbookError(Exception):
    def __init__(self, code: str, operation_id: str | None = None, message: str | None = None):
        self.code = code
        self.operation_id = operation_id
        super().__init__(message or code)


class Checkbook:
    def __init__(self, database_path: str):
        self._conn = sqlite3.connect(database_path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._init_schema()

    def create_account(
        self, account_id: str, currency: str, opening_balance_minor: int, operation_id: str
    ) -> dict:
        self._require_operation_id(operation_id)
        self._require_identifier(account_id, "account_id")
        self._require_currency(currency)
        self._require_money(opening_balance_minor, "opening_balance_minor")
        try:
            with self._conn:
                self._conn.execute(
                    """
                    INSERT INTO accounts(account_id, currency, opening_balance_minor, closed_through_date)
                    VALUES (?, ?, ?, NULL)
                    """,
                    (account_id, currency, opening_balance_minor),
                )
                self._audit("account_created", account_id, operation_id)
        except sqlite3.IntegrityError as exc:
            raise CheckbookError("account_exists", operation_id) from exc
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
        self._require_identifier(account_id, "account_id")
        self._require_identifier(transaction_id, "transaction_id")
        posted = self._require_date(posted_date, "posted_date")
        self._require_money(amount_minor, "amount_minor")
        self._require_description(description)
        with self._conn:
            account = self._get_account_row(account_id)
            self._ensure_open_date(account["closed_through_date"], posted, operation_id)
            try:
                self._conn.execute(
                    """
                    INSERT INTO transactions(
                        transaction_id, account_id, posted_date, amount_minor, description,
                        version, cleared, reconciled, reversal_of, reversed_by, source, external_id
                    ) VALUES (?, ?, ?, ?, ?, 1, 0, 0, NULL, NULL, NULL, NULL)
                    """,
                    (transaction_id, account_id, posted_date, amount_minor, description),
                )
            except sqlite3.IntegrityError as exc:
                raise CheckbookError("transaction_exists", operation_id) from exc
            self._audit("transaction_recorded", account_id, operation_id)
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
        self._require_identifier(transaction_id, "transaction_id")
        posted = self._require_date(posted_date, "posted_date")
        self._require_version(expected_version)
        self._require_money(amount_minor, "amount_minor")
        self._require_description(description)
        with self._conn:
            tx = self._get_transaction_row(transaction_id)
            account = self._get_account_row(tx["account_id"])
            self._assert_not_reconciled(tx, operation_id)
            self._ensure_not_closed(account["closed_through_date"], tx["posted_date"], operation_id)
            self._ensure_open_date(account["closed_through_date"], posted, operation_id)
            self._assert_version(tx, expected_version, operation_id)
            self._conn.execute(
                """
                UPDATE transactions
                SET posted_date = ?, amount_minor = ?, description = ?, version = version + 1
                WHERE transaction_id = ?
                """,
                (posted_date, amount_minor, description, transaction_id),
            )
            self._audit("transaction_edited", tx["account_id"], operation_id)
        return self.get_transaction(transaction_id)

    def mark_cleared(self, transaction_id: str, expected_version: int, operation_id: str) -> dict:
        self._require_operation_id(operation_id)
        self._require_identifier(transaction_id, "transaction_id")
        self._require_version(expected_version)
        with self._conn:
            tx = self._get_transaction_row(transaction_id)
            account = self._get_account_row(tx["account_id"])
            self._assert_not_reconciled(tx, operation_id)
            self._ensure_not_closed(account["closed_through_date"], tx["posted_date"], operation_id)
            self._assert_version(tx, expected_version, operation_id)
            if tx["cleared"]:
                raise CheckbookError("already_cleared", operation_id)
            self._conn.execute(
                "UPDATE transactions SET cleared = 1, version = version + 1 WHERE transaction_id = ?",
                (transaction_id,),
            )
            self._audit("transaction_cleared", tx["account_id"], operation_id)
        return self.get_transaction(transaction_id)

    def import_csv(self, account_id: str, source: str, csv_text: str, operation_id: str) -> dict:
        self._require_operation_id(operation_id)
        self._require_identifier(account_id, "account_id")
        self._require_identifier(source, "source")
        with self._conn:
            try:
                rows = self._parse_import_csv(csv_text, operation_id)
                inserted = 0
                duplicates = 0
                staged: list[tuple[str, str, int, str, str, str]] = []
                seen: dict[tuple[str, str], tuple[str, int, str]] = {}
                account = self._get_account_row(account_id)
                for external_id, posted_date, amount_minor, description in rows:
                    self._ensure_open_date(account["closed_through_date"], posted_date, operation_id)
                    identity = (source, external_id)
                    payload = (posted_date, amount_minor, description)
                    prior_seen = seen.get(identity)
                    if prior_seen is not None:
                        if prior_seen != payload:
                            raise CheckbookError("duplicate_conflict", operation_id)
                        duplicates += 1
                        continue
                    seen[identity] = payload
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
                        if current != payload:
                            raise CheckbookError("duplicate_conflict", operation_id)
                        duplicates += 1
                        continue
                    transaction_id = self._import_transaction_id(account_id, source, external_id)
                    staged.append(
                        (transaction_id, account_id, posted_date, amount_minor, description, external_id)
                    )
                for transaction_id, row_account_id, posted_date, amount_minor, description, external_id in staged:
                    self._conn.execute(
                        """
                        INSERT INTO transactions(
                            transaction_id, account_id, posted_date, amount_minor, description,
                            version, cleared, reconciled, reversal_of, reversed_by, source, external_id
                        ) VALUES (?, ?, ?, ?, ?, 1, 0, 0, NULL, NULL, ?, ?)
                        """,
                        (
                            transaction_id,
                            row_account_id,
                            posted_date,
                            amount_minor,
                            description,
                            source,
                            external_id,
                        ),
                    )
                    inserted += 1
                if inserted:
                    self._audit("transactions_imported", account_id, operation_id)
                return {"inserted": inserted, "duplicates": duplicates}
            except CheckbookError as exc:
                if exc.operation_id is None:
                    exc.operation_id = operation_id
                raise

    def reconcile(
        self,
        account_id: str,
        statement_date: str,
        ending_balance_minor: int,
        operation_id: str,
    ) -> dict:
        self._require_operation_id(operation_id)
        self._require_identifier(account_id, "account_id")
        statement = self._require_date(statement_date, "statement_date")
        self._require_money(ending_balance_minor, "ending_balance_minor")
        try:
            with self._conn:
                account = self._get_account_row(account_id)
                if account["closed_through_date"] is not None and statement <= account["closed_through_date"]:
                    raise CheckbookError("closed_period", operation_id)
                prior_total = self._sum_amounts(
                    "SELECT COALESCE(SUM(amount_minor), 0) FROM transactions WHERE account_id = ? AND reconciled = 1",
                    (account_id,),
                )
                candidates = self._conn.execute(
                    """
                    SELECT transaction_id, posted_date
                    FROM transactions
                    WHERE account_id = ? AND cleared = 1 AND reconciled = 0 AND posted_date <= ?
                    ORDER BY posted_date, transaction_id
                    """,
                    (account_id, statement_date),
                ).fetchall()
                for tx in candidates:
                    self._ensure_not_closed(account["closed_through_date"], tx["posted_date"], operation_id)
                candidate_total = self._sum_amounts(
                    """
                    SELECT COALESCE(SUM(amount_minor), 0)
                    FROM transactions
                    WHERE account_id = ? AND cleared = 1 AND reconciled = 0 AND posted_date <= ?
                    """,
                    (account_id, statement_date),
                )
                actual = account["opening_balance_minor"] + prior_total + candidate_total
                if actual != ending_balance_minor:
                    raise CheckbookError("reconciliation_mismatch", operation_id)
                if candidates:
                    self._conn.execute(
                        """
                        UPDATE transactions
                        SET reconciled = 1
                        WHERE account_id = ? AND cleared = 1 AND reconciled = 0 AND posted_date <= ?
                        """,
                        (account_id, statement_date),
                    )
                self._audit("account_reconciled", account_id, operation_id)
        except CheckbookError as exc:
            if exc.operation_id is None:
                exc.operation_id = operation_id
            raise
        return {
            "account_id": account_id,
            "statement_date": statement_date,
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
        self._require_identifier(original_transaction_id, "original_transaction_id")
        self._require_identifier(reversal_transaction_id, "reversal_transaction_id")
        reversal_posted = self._require_date(posted_date, "posted_date")
        with self._conn:
            original = self._get_transaction_row(original_transaction_id)
            account = self._get_account_row(original["account_id"])
            if not original["reconciled"]:
                raise CheckbookError("not_reconciled", operation_id)
            self._ensure_not_closed(account["closed_through_date"], original["posted_date"], operation_id)
            self._ensure_open_date(account["closed_through_date"], reversal_posted, operation_id)
            if original["reversed_by"] is not None:
                raise CheckbookError("duplicate_reversal", operation_id)
            try:
                self._conn.execute(
                    """
                    INSERT INTO transactions(
                        transaction_id, account_id, posted_date, amount_minor, description,
                        version, cleared, reconciled, reversal_of, reversed_by, source, external_id
                    ) VALUES (?, ?, ?, ?, ?, 1, 0, 0, ?, NULL, NULL, NULL)
                    """,
                    (
                        reversal_transaction_id,
                        original["account_id"],
                        posted_date,
                        -original["amount_minor"],
                        f"Reversal of {original_transaction_id}",
                        original_transaction_id,
                    ),
                )
            except sqlite3.IntegrityError as exc:
                raise CheckbookError("transaction_exists", operation_id) from exc
            self._conn.execute(
                "UPDATE transactions SET reversed_by = ? WHERE transaction_id = ?",
                (reversal_transaction_id, original_transaction_id),
            )
            self._audit("transaction_reversed", original["account_id"], operation_id)
        return self.get_transaction(reversal_transaction_id)

    def close_period(self, account_id: str, through_date: str, operation_id: str) -> dict:
        self._require_operation_id(operation_id)
        self._require_identifier(account_id, "account_id")
        through = self._require_date(through_date, "through_date")
        with self._conn:
            account = self._get_account_row(account_id)
            current = account["closed_through_date"]
            if current is not None and through <= current:
                raise CheckbookError("closed_period_regression", operation_id)
            self._conn.execute(
                "UPDATE accounts SET closed_through_date = ? WHERE account_id = ?",
                (through_date, account_id),
            )
            self._audit("period_closed", account_id, operation_id)
        return self.get_account(account_id)

    def get_account(self, account_id: str) -> dict:
        self._require_identifier(account_id, "account_id")
        row = self._get_account_row(account_id)
        return {
            "account_id": row["account_id"],
            "currency": row["currency"],
            "opening_balance_minor": row["opening_balance_minor"],
            "closed_through_date": row["closed_through_date"],
        }

    def get_transaction(self, transaction_id: str) -> dict:
        self._require_identifier(transaction_id, "transaction_id")
        row = self._get_transaction_row(transaction_id)
        return self._transaction_dict(row)

    def list_transactions(self, account_id: str) -> list[dict]:
        self._require_identifier(account_id, "account_id")
        self._get_account_row(account_id)
        rows = self._conn.execute(
            """
            SELECT transaction_id, account_id, posted_date, amount_minor, description, version,
                   cleared, reconciled, reversal_of, source, external_id
            FROM transactions
            WHERE account_id = ?
            ORDER BY posted_date, transaction_id
            """,
            (account_id,),
        ).fetchall()
        return [self._transaction_dict(row) for row in rows]

    def list_audit_events(self) -> list[dict]:
        rows = self._conn.execute(
            "SELECT event_id, operation_id, event_type, account_id FROM audit_events ORDER BY event_id"
        ).fetchall()
        return [
            {
                "event_id": row["event_id"],
                "operation_id": row["operation_id"],
                "event_type": row["event_type"],
                "account_id": row["account_id"],
            }
            for row in rows
        ]

    def _init_schema(self) -> None:
        with self._conn:
            self._conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS accounts (
                    account_id TEXT PRIMARY KEY,
                    currency TEXT NOT NULL,
                    opening_balance_minor INTEGER NOT NULL,
                    closed_through_date TEXT
                );

                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id TEXT PRIMARY KEY,
                    account_id TEXT NOT NULL REFERENCES accounts(account_id),
                    posted_date TEXT NOT NULL,
                    amount_minor INTEGER NOT NULL,
                    description TEXT NOT NULL,
                    version INTEGER NOT NULL,
                    cleared INTEGER NOT NULL,
                    reconciled INTEGER NOT NULL,
                    reversal_of TEXT REFERENCES transactions(transaction_id),
                    reversed_by TEXT UNIQUE REFERENCES transactions(transaction_id),
                    source TEXT,
                    external_id TEXT
                );

                CREATE UNIQUE INDEX IF NOT EXISTS transactions_import_identity
                ON transactions(account_id, source, external_id)
                WHERE source IS NOT NULL AND external_id IS NOT NULL;

                CREATE TABLE IF NOT EXISTS audit_events (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    account_id TEXT NOT NULL REFERENCES accounts(account_id)
                );
                """
            )

    def _audit(self, event_type: str, account_id: str, operation_id: str) -> None:
        self._conn.execute(
            "INSERT INTO audit_events(operation_id, event_type, account_id) VALUES (?, ?, ?)",
            (operation_id, event_type, account_id),
        )

    def _get_account_row(self, account_id: str) -> sqlite3.Row:
        row = self._conn.execute(
            "SELECT account_id, currency, opening_balance_minor, closed_through_date FROM accounts WHERE account_id = ?",
            (account_id,),
        ).fetchone()
        if row is None:
            raise CheckbookError("account_not_found")
        return row

    def _get_transaction_row(self, transaction_id: str) -> sqlite3.Row:
        row = self._conn.execute(
            """
            SELECT transaction_id, account_id, posted_date, amount_minor, description, version,
                   cleared, reconciled, reversal_of, reversed_by, source, external_id
            FROM transactions
            WHERE transaction_id = ?
            """,
            (transaction_id,),
        ).fetchone()
        if row is None:
            raise CheckbookError("transaction_not_found")
        return row

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

    def _parse_import_csv(self, csv_text: str, operation_id: str) -> list[tuple[str, str, int, str]]:
        try:
            reader = csv.DictReader(StringIO(csv_text))
        except csv.Error as exc:
            raise CheckbookError("invalid_csv", operation_id) from exc
        if reader.fieldnames != ["external_id", "posted_date", "amount_minor", "description"]:
            raise CheckbookError("invalid_csv_header", operation_id)
        rows: list[tuple[str, str, int, str]] = []
        for row in reader:
            if row is None or set(row.keys()) != set(reader.fieldnames):
                raise CheckbookError("invalid_csv", operation_id)
            external_id = row["external_id"]
            description = row["description"]
            self._require_identifier(external_id, "external_id", operation_id)
            posted = self._require_date(row["posted_date"], "posted_date", operation_id)
            amount_minor = self._parse_csv_money(row["amount_minor"], "amount_minor", operation_id)
            self._require_description(description, operation_id)
            rows.append((external_id, posted, amount_minor, description))
        return rows

    def _sum_amounts(self, query: str, params: tuple) -> int:
        return int(self._conn.execute(query, params).fetchone()[0])

    def _import_transaction_id(self, account_id: str, source: str, external_id: str) -> str:
        digest = hashlib.sha256(f"{account_id}\0{source}\0{external_id}".encode("utf-8")).hexdigest()
        return f"import_{digest}"

    def _assert_version(self, tx: sqlite3.Row, expected_version: int, operation_id: str) -> None:
        if tx["version"] != expected_version:
            raise CheckbookError("stale_version", operation_id)

    def _assert_not_reconciled(self, tx: sqlite3.Row, operation_id: str) -> None:
        if tx["reconciled"]:
            raise CheckbookError("reconciled_transaction", operation_id)

    def _ensure_not_closed(
        self, closed_through_date: str | None, candidate_date: str, operation_id: str
    ) -> None:
        if closed_through_date is not None and candidate_date <= closed_through_date:
            raise CheckbookError("closed_period", operation_id)

    def _ensure_open_date(
        self, closed_through_date: str | None, candidate_date: str, operation_id: str
    ) -> None:
        self._ensure_not_closed(closed_through_date, candidate_date, operation_id)

    def _require_operation_id(self, operation_id: str) -> None:
        self._require_identifier(operation_id, "operation_id")

    def _require_identifier(
        self, value: str, field_name: str, operation_id: str | None = None
    ) -> str:
        if not isinstance(value, str) or value == "":
            raise CheckbookError(f"invalid_{field_name}", operation_id)
        return value

    def _require_currency(self, currency: str) -> str:
        if not isinstance(currency, str) or len(currency) != 3 or currency.upper() != currency or not currency.isalpha():
            raise CheckbookError("invalid_currency")
        return currency

    def _require_money(self, value: int, field_name: str) -> int:
        return self._coerce_money(value, field_name, None)

    def _coerce_money(self, value, field_name: str, operation_id: str | None) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise CheckbookError(f"invalid_{field_name}", operation_id)
        return value

    def _parse_csv_money(self, value: str, field_name: str, operation_id: str) -> int:
        if not isinstance(value, str) or value == "":
            raise CheckbookError(f"invalid_{field_name}", operation_id)
        try:
            parsed = int(value)
        except ValueError as exc:
            raise CheckbookError(f"invalid_{field_name}", operation_id) from exc
        return parsed

    def _require_date(self, value: str, field_name: str, operation_id: str | None = None) -> str:
        if not isinstance(value, str):
            raise CheckbookError(f"invalid_{field_name}", operation_id)
        try:
            parsed = date.fromisoformat(value)
        except ValueError as exc:
            raise CheckbookError(f"invalid_{field_name}", operation_id) from exc
        if parsed.isoformat() != value:
            raise CheckbookError(f"invalid_{field_name}", operation_id)
        return value

    def _require_description(self, value: str, operation_id: str | None = None) -> str:
        if not isinstance(value, str):
            raise CheckbookError("invalid_description", operation_id)
        return value

    def _require_version(self, value: int) -> int:
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise CheckbookError("invalid_expected_version")
        return value
