from __future__ import annotations

import csv
import io
import json
import sqlite3
from datetime import date


class CheckbookError(Exception):
    def __init__(self, code: str, message: str, operation_id: str | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.operation_id = operation_id


class Checkbook:
    def __init__(self, database_path: str):
        if not isinstance(database_path, str) or not database_path:
            raise CheckbookError("invalid_database_path", "database_path must be a non-empty string")
        self._conn = sqlite3.connect(database_path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._init_schema()

    def create_account(
        self,
        account_id: str,
        currency: str,
        opening_balance_minor: int,
        operation_id: str,
    ) -> dict:
        operation_id = self._require_operation_id(operation_id)
        account_id = self._require_identifier("account_id", account_id, operation_id)
        currency = self._require_currency(currency, operation_id)
        opening_balance_minor = self._require_money(opening_balance_minor, operation_id)
        try:
            with self._conn:
                self._conn.execute(
                    """
                    INSERT INTO accounts (
                        account_id, currency, opening_balance_minor, closed_through_date
                    ) VALUES (?, ?, ?, NULL)
                    """,
                    (account_id, currency, opening_balance_minor),
                )
                self._insert_audit(
                    operation_id,
                    "account_created",
                    account_id,
                    None,
                    {"opening_balance_minor": opening_balance_minor},
                )
        except sqlite3.IntegrityError as exc:
            raise CheckbookError("account_exists", "account already exists", operation_id) from exc
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
        operation_id = self._require_operation_id(operation_id)
        account = self._get_account_row(account_id, operation_id)
        transaction_id = self._require_identifier("transaction_id", transaction_id, operation_id)
        posted_date = self._require_date(posted_date, operation_id)
        amount_minor = self._require_money(amount_minor, operation_id)
        description = self._require_string("description", description, operation_id)
        self._require_open_period(account, posted_date, operation_id)
        try:
            with self._conn:
                self._insert_transaction(
                    transaction_id=transaction_id,
                    account_id=account["account_id"],
                    posted_date=posted_date,
                    amount_minor=amount_minor,
                    description=description,
                    reversal_of=None,
                    source=None,
                    external_id=None,
                )
                self._insert_audit(
                    operation_id,
                    "transaction_recorded",
                    account["account_id"],
                    transaction_id,
                    None,
                )
        except sqlite3.IntegrityError as exc:
            raise CheckbookError("transaction_exists", "transaction already exists", operation_id) from exc
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
        operation_id = self._require_operation_id(operation_id)
        transaction = self._get_transaction_row(transaction_id, operation_id)
        account = self._get_account_row(transaction["account_id"], operation_id)
        expected_version = self._require_version(expected_version, operation_id)
        posted_date = self._require_date(posted_date, operation_id)
        amount_minor = self._require_money(amount_minor, operation_id)
        description = self._require_string("description", description, operation_id)
        if transaction["version"] != expected_version:
            raise CheckbookError("stale_version", "transaction version is stale", operation_id)
        if transaction["reconciled"]:
            raise CheckbookError("reconciled_transaction", "transaction is reconciled", operation_id)
        self._require_open_period(account, transaction["posted_date"], operation_id)
        self._require_open_period(account, posted_date, operation_id)
        with self._conn:
            self._conn.execute(
                """
                UPDATE transactions
                SET posted_date = ?, amount_minor = ?, description = ?, version = version + 1
                WHERE transaction_id = ?
                """,
                (posted_date, amount_minor, description, transaction_id),
            )
            self._insert_audit(
                operation_id,
                "transaction_edited",
                transaction["account_id"],
                transaction_id,
                None,
            )
        return self.get_transaction(transaction_id)

    def mark_cleared(
        self,
        transaction_id: str,
        expected_version: int,
        operation_id: str,
    ) -> dict:
        operation_id = self._require_operation_id(operation_id)
        transaction = self._get_transaction_row(transaction_id, operation_id)
        account = self._get_account_row(transaction["account_id"], operation_id)
        expected_version = self._require_version(expected_version, operation_id)
        if transaction["version"] != expected_version:
            raise CheckbookError("stale_version", "transaction version is stale", operation_id)
        if transaction["reconciled"]:
            raise CheckbookError("reconciled_transaction", "transaction is reconciled", operation_id)
        if transaction["cleared"]:
            raise CheckbookError("already_cleared", "transaction is already cleared", operation_id)
        self._require_open_period(account, transaction["posted_date"], operation_id)
        with self._conn:
            self._conn.execute(
                """
                UPDATE transactions
                SET cleared = 1, version = version + 1
                WHERE transaction_id = ?
                """,
                (transaction_id,),
            )
            self._insert_audit(
                operation_id,
                "transaction_cleared",
                transaction["account_id"],
                transaction_id,
                None,
            )
        return self.get_transaction(transaction_id)

    def import_csv(
        self,
        account_id: str,
        source: str,
        csv_text: str,
        operation_id: str,
    ) -> dict:
        operation_id = self._require_operation_id(operation_id)
        account = self._get_account_row(account_id, operation_id)
        source = self._require_identifier("source", source, operation_id)
        csv_text = self._require_string("csv_text", csv_text, operation_id)
        rows = self._parse_import_csv(account, source, csv_text, operation_id)
        inserted = 0
        duplicates = 0
        try:
            with self._conn:
                for row in rows:
                    existing = self._find_import_identity(account["account_id"], source, row["external_id"])
                    if existing is None:
                        self._insert_transaction(
                            transaction_id=row["transaction_id"],
                            account_id=account["account_id"],
                            posted_date=row["posted_date"],
                            amount_minor=row["amount_minor"],
                            description=row["description"],
                            reversal_of=None,
                            source=source,
                            external_id=row["external_id"],
                        )
                        inserted += 1
                    else:
                        duplicates += 1
                if inserted:
                    self._insert_audit(
                        operation_id,
                        "transactions_imported",
                        account["account_id"],
                        None,
                        {"inserted": inserted, "duplicates": duplicates, "source": source},
                    )
        except sqlite3.IntegrityError as exc:
            raise CheckbookError("storage_failure", "import could not be stored", operation_id) from exc
        return {"inserted": inserted, "duplicates": duplicates}

    def reconcile(
        self,
        account_id: str,
        statement_date: str,
        ending_balance_minor: int,
        operation_id: str,
    ) -> dict:
        operation_id = self._require_operation_id(operation_id)
        account = self._get_account_row(account_id, operation_id)
        statement_date = self._require_date(statement_date, operation_id)
        ending_balance_minor = self._require_money(ending_balance_minor, operation_id)
        self._require_open_period(account, statement_date, operation_id)
        candidates = self._conn.execute(
            """
            SELECT transaction_id, posted_date, amount_minor
            FROM transactions
            WHERE account_id = ?
              AND cleared = 1
              AND reconciled = 0
              AND posted_date <= ?
            ORDER BY posted_date, transaction_id
            """,
            (account["account_id"], statement_date),
        ).fetchall()
        for candidate in candidates:
            self._require_open_period(account, candidate["posted_date"], operation_id)
        prior_reconciled = self._scalar(
            """
            SELECT COALESCE(SUM(amount_minor), 0)
            FROM transactions
            WHERE account_id = ? AND reconciled = 1
            """,
            (account["account_id"],),
        )
        pending_total = sum(candidate["amount_minor"] for candidate in candidates)
        actual = account["opening_balance_minor"] + prior_reconciled + pending_total
        if actual != ending_balance_minor:
            raise CheckbookError(
                "reconciliation_mismatch",
                "ending balance does not match reconciled balance",
                operation_id,
            )
        with self._conn:
            if candidates:
                self._conn.execute(
                    """
                    UPDATE transactions
                    SET reconciled = 1
                    WHERE account_id = ?
                      AND cleared = 1
                      AND reconciled = 0
                      AND posted_date <= ?
                    """,
                    (account["account_id"], statement_date),
                )
            self._insert_audit(
                operation_id,
                "account_reconciled",
                account["account_id"],
                None,
                {
                    "statement_date": statement_date,
                    "ending_balance_minor": ending_balance_minor,
                    "transaction_count": len(candidates),
                },
            )
        return {
            "account_id": account["account_id"],
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
        operation_id = self._require_operation_id(operation_id)
        original = self._get_transaction_row(original_transaction_id, operation_id)
        account = self._get_account_row(original["account_id"], operation_id)
        reversal_transaction_id = self._require_identifier(
            "reversal_transaction_id", reversal_transaction_id, operation_id
        )
        posted_date = self._require_date(posted_date, operation_id)
        if not original["reconciled"]:
            raise CheckbookError(
                "transaction_not_reconciled",
                "transaction is not reconciled",
                operation_id,
            )
        if original["reversal_of"] is not None:
            raise CheckbookError(
                "reversal_transaction",
                "cannot reverse a reversal transaction",
                operation_id,
            )
        if posted_date <= original["posted_date"]:
            raise CheckbookError(
                "invalid_reversal_date",
                "reversal date must be later than the original transaction date",
                operation_id,
            )
        self._require_open_period(account, posted_date, operation_id)
        existing = self._conn.execute(
            "SELECT transaction_id FROM transactions WHERE reversal_of = ?",
            (original_transaction_id,),
        ).fetchone()
        if existing is not None:
            raise CheckbookError("duplicate_reversal", "transaction already reversed", operation_id)
        try:
            with self._conn:
                self._insert_transaction(
                    transaction_id=reversal_transaction_id,
                    account_id=original["account_id"],
                    posted_date=posted_date,
                    amount_minor=-original["amount_minor"],
                    description=f"Reversal of {original_transaction_id}",
                    reversal_of=original_transaction_id,
                    source=None,
                    external_id=None,
                )
                self._insert_audit(
                    operation_id,
                    "transaction_reversed",
                    original["account_id"],
                    reversal_transaction_id,
                    {"original_transaction_id": original_transaction_id},
                )
        except sqlite3.IntegrityError as exc:
            raise CheckbookError("transaction_exists", "transaction already exists", operation_id) from exc
        return self.get_transaction(reversal_transaction_id)

    def close_period(
        self,
        account_id: str,
        through_date: str,
        operation_id: str,
    ) -> dict:
        operation_id = self._require_operation_id(operation_id)
        account = self._get_account_row(account_id, operation_id)
        through_date = self._require_date(through_date, operation_id)
        current = account["closed_through_date"]
        if current is not None and through_date < current:
            raise CheckbookError("close_moves_backward", "closed period cannot move backward", operation_id)
        if current == through_date:
            raise CheckbookError("already_closed_through", "account already closed through date", operation_id)
        with self._conn:
            self._conn.execute(
                "UPDATE accounts SET closed_through_date = ? WHERE account_id = ?",
                (through_date, account["account_id"]),
            )
            self._insert_audit(
                operation_id,
                "period_closed",
                account["account_id"],
                None,
                {"through_date": through_date},
            )
        return self.get_account(account_id)

    def get_account(self, account_id: str) -> dict:
        account = self._get_account_row(account_id, None)
        current_balance_minor = account["opening_balance_minor"] + self._scalar(
            "SELECT COALESCE(SUM(amount_minor), 0) FROM transactions WHERE account_id = ?",
            (account["account_id"],),
        )
        return {
            "account_id": account["account_id"],
            "currency": account["currency"],
            "opening_balance_minor": account["opening_balance_minor"],
            "closed_through_date": account["closed_through_date"],
            "current_balance_minor": current_balance_minor,
        }

    def get_transaction(self, transaction_id: str) -> dict:
        return self._transaction_to_dict(self._get_transaction_row(transaction_id, None))

    def list_transactions(self, account_id: str) -> list[dict]:
        account_id = self._require_identifier("account_id", account_id, None)
        rows = self._conn.execute(
            """
            SELECT *
            FROM transactions
            WHERE account_id = ?
            ORDER BY posted_date, transaction_id
            """,
            (account_id,),
        ).fetchall()
        return [self._transaction_to_dict(row) for row in rows]

    def list_audit_events(self) -> list[dict]:
        rows = self._conn.execute(
            """
            SELECT event_id, operation_id, event_type, account_id, transaction_id, details_json
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
                "details": json.loads(row["details_json"]) if row["details_json"] else None,
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
                    reversal_of TEXT UNIQUE REFERENCES transactions(transaction_id),
                    source TEXT,
                    external_id TEXT,
                    UNIQUE(account_id, source, external_id)
                );

                CREATE TABLE IF NOT EXISTS audit_events (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    account_id TEXT NOT NULL,
                    transaction_id TEXT,
                    details_json TEXT
                );
                """
            )

    def _insert_transaction(
        self,
        *,
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
            INSERT INTO transactions (
                transaction_id, account_id, posted_date, amount_minor, description,
                version, cleared, reconciled, reversal_of, source, external_id
            ) VALUES (?, ?, ?, ?, ?, 1, 0, 0, ?, ?, ?)
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

    def _insert_audit(
        self,
        operation_id: str,
        event_type: str,
        account_id: str,
        transaction_id: str | None,
        details: dict | None,
    ) -> None:
        self._conn.execute(
            """
            INSERT INTO audit_events (
                operation_id, event_type, account_id, transaction_id, details_json
            ) VALUES (?, ?, ?, ?, ?)
            """,
            (
                operation_id,
                event_type,
                account_id,
                transaction_id,
                json.dumps(details, sort_keys=True) if details is not None else None,
            ),
        )

    def _parse_import_csv(
        self,
        account: sqlite3.Row,
        source: str,
        csv_text: str,
        operation_id: str,
    ) -> list[dict]:
        reader = csv.DictReader(io.StringIO(csv_text))
        expected_header = ["external_id", "posted_date", "amount_minor", "description"]
        if reader.fieldnames != expected_header:
            raise CheckbookError("invalid_csv_header", "csv header is invalid", operation_id)
        seen: dict[str, tuple[str, int, str]] = {}
        parsed: list[dict] = []
        for index, row in enumerate(reader, start=2):
            if row is None or set(row) != set(expected_header):
                raise CheckbookError("invalid_csv_row", f"csv row {index} is malformed", operation_id)
            if None in row.values():
                raise CheckbookError("invalid_csv_row", f"csv row {index} is malformed", operation_id)
            external_id = self._require_identifier("external_id", row["external_id"], operation_id)
            posted_date = self._require_date(row["posted_date"], operation_id)
            amount_minor = self._parse_csv_amount(row["amount_minor"], operation_id)
            description = self._require_string("description", row["description"], operation_id)
            self._require_open_period(account, posted_date, operation_id)
            signature = (posted_date, amount_minor, description)
            prior = seen.get(external_id)
            if prior is not None and prior != signature:
                raise CheckbookError("duplicate_conflict", "import duplicate conflict", operation_id)
            seen[external_id] = signature
            existing = self._find_import_identity(account["account_id"], source, external_id)
            if existing is not None:
                existing_signature = (
                    existing["posted_date"],
                    existing["amount_minor"],
                    existing["description"],
                )
                if existing_signature != signature:
                    raise CheckbookError("duplicate_conflict", "import duplicate conflict", operation_id)
            parsed.append(
                {
                    "transaction_id": self._import_transaction_id(account["account_id"], source, external_id),
                    "external_id": external_id,
                    "posted_date": posted_date,
                    "amount_minor": amount_minor,
                    "description": description,
                }
            )
        return parsed

    def _find_import_identity(self, account_id: str, source: str, external_id: str) -> sqlite3.Row | None:
        return self._conn.execute(
            """
            SELECT transaction_id, posted_date, amount_minor, description
            FROM transactions
            WHERE account_id = ? AND source = ? AND external_id = ?
            """,
            (account_id, source, external_id),
        ).fetchone()

    def _import_transaction_id(self, account_id: str, source: str, external_id: str) -> str:
        return f"import:{account_id}:{source}:{external_id}"

    def _get_account_row(self, account_id: str, operation_id: str | None) -> sqlite3.Row:
        account_id = self._require_identifier("account_id", account_id, operation_id)
        row = self._conn.execute(
            "SELECT * FROM accounts WHERE account_id = ?",
            (account_id,),
        ).fetchone()
        if row is None:
            raise CheckbookError("account_not_found", "account was not found", operation_id)
        return row

    def _get_transaction_row(self, transaction_id: str, operation_id: str | None) -> sqlite3.Row:
        transaction_id = self._require_identifier("transaction_id", transaction_id, operation_id)
        row = self._conn.execute(
            "SELECT * FROM transactions WHERE transaction_id = ?",
            (transaction_id,),
        ).fetchone()
        if row is None:
            raise CheckbookError("transaction_not_found", "transaction was not found", operation_id)
        return row

    def _transaction_to_dict(self, row: sqlite3.Row) -> dict:
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

    def _scalar(self, sql: str, params: tuple) -> int:
        value = self._conn.execute(sql, params).fetchone()[0]
        return int(value)

    def _require_operation_id(self, operation_id: str) -> str:
        return self._require_identifier("operation_id", operation_id, operation_id)

    def _require_identifier(
        self,
        name: str,
        value: str,
        operation_id: str | None,
    ) -> str:
        if not isinstance(value, str) or value == "":
            raise CheckbookError(f"invalid_{name}", f"{name} must be a non-empty string", operation_id)
        return value

    def _require_string(self, name: str, value: str, operation_id: str | None) -> str:
        if not isinstance(value, str):
            raise CheckbookError(f"invalid_{name}", f"{name} must be a string", operation_id)
        return value

    def _require_currency(self, currency: str, operation_id: str | None) -> str:
        if not isinstance(currency, str) or len(currency) != 3 or not currency.isupper() or not currency.isalpha():
            raise CheckbookError("invalid_currency", "currency must be a three-letter uppercase code", operation_id)
        return currency

    def _require_date(self, value: str, operation_id: str | None) -> str:
        if not isinstance(value, str):
            raise CheckbookError("invalid_date", "date must be an ISO string", operation_id)
        try:
            parsed = date.fromisoformat(value)
        except ValueError as exc:
            raise CheckbookError("invalid_date", "date must be a real ISO date", operation_id) from exc
        if parsed.isoformat() != value:
            raise CheckbookError("invalid_date", "date must be a real ISO date", operation_id)
        return value

    def _require_money(self, value: int, operation_id: str | None) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise CheckbookError("invalid_amount_minor", "amount_minor must be an integer", operation_id)
        return value

    def _require_version(self, value: int, operation_id: str | None) -> int:
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise CheckbookError("invalid_expected_version", "expected_version must be a positive integer", operation_id)
        return value

    def _parse_csv_amount(self, value: str, operation_id: str | None) -> int:
        if not isinstance(value, str) or value == "":
            raise CheckbookError("invalid_amount_minor", "amount_minor must be an integer", operation_id)
        if value[0] in "+-":
            digits = value[1:]
        else:
            digits = value
        if not digits.isdigit():
            raise CheckbookError("invalid_amount_minor", "amount_minor must be an integer", operation_id)
        return int(value)

    def _require_open_period(
        self,
        account: sqlite3.Row,
        posted_date: str,
        operation_id: str | None,
    ) -> None:
        closed_through_date = account["closed_through_date"]
        if closed_through_date is not None and posted_date <= closed_through_date:
            raise CheckbookError("closed_period", "date is in a closed period", operation_id)
