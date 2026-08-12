"""Private reference fixture for validating the external benchmark suite."""

from __future__ import annotations

import csv
import hashlib
import io
import re
import sqlite3
from datetime import date


class CheckbookError(Exception):
    def __init__(
        self, code: str, operation_id: str | None = None, message: str = ""
    ) -> None:
        super().__init__(message or code)
        self.code = code
        self.operation_id = operation_id


class Checkbook:
    def __init__(self, database_path: str):
        self.connection = sqlite3.connect(database_path, timeout=10)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS accounts (
                account_id TEXT PRIMARY KEY,
                currency TEXT NOT NULL,
                opening_balance_minor INTEGER NOT NULL,
                closed_through TEXT
            );
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id TEXT PRIMARY KEY,
                account_id TEXT NOT NULL REFERENCES accounts(account_id),
                posted_date TEXT NOT NULL,
                amount_minor INTEGER NOT NULL,
                description TEXT NOT NULL,
                version INTEGER NOT NULL DEFAULT 1,
                cleared INTEGER NOT NULL DEFAULT 0,
                reconciled INTEGER NOT NULL DEFAULT 0,
                reversal_of TEXT REFERENCES transactions(transaction_id),
                source TEXT,
                external_id TEXT,
                UNIQUE(account_id, source, external_id)
            );
            CREATE TABLE IF NOT EXISTS audit_events (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                account_id TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS reconciliations (
                reconciliation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id TEXT NOT NULL,
                statement_date TEXT NOT NULL,
                ending_balance_minor INTEGER NOT NULL
            );
            """
        )

    @staticmethod
    def _identifier(value: object, operation_id: str | None = None) -> str:
        if not isinstance(value, str) or not value:
            raise CheckbookError("invalid_identifier", operation_id)
        return value

    @staticmethod
    def _money(value: object, operation_id: str | None = None) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise CheckbookError("invalid_money", operation_id)
        return value

    @staticmethod
    def _date(value: object, operation_id: str | None = None) -> str:
        if not isinstance(value, str):
            raise CheckbookError("invalid_date", operation_id)
        try:
            parsed = date.fromisoformat(value)
        except ValueError as error:
            raise CheckbookError("invalid_date", operation_id) from error
        if parsed.isoformat() != value:
            raise CheckbookError("invalid_date", operation_id)
        return value

    @classmethod
    def _operation(cls, value: object) -> str:
        return cls._identifier(value)

    def _account_row(
        self, account_id: str, operation_id: str | None = None
    ) -> sqlite3.Row:
        row = self.connection.execute(
            "SELECT * FROM accounts WHERE account_id = ?", (account_id,)
        ).fetchone()
        if row is None:
            raise CheckbookError("account_not_found", operation_id)
        return row

    def _transaction_row(
        self, transaction_id: str, operation_id: str | None = None
    ) -> sqlite3.Row:
        row = self.connection.execute(
            "SELECT * FROM transactions WHERE transaction_id = ?",
            (transaction_id,),
        ).fetchone()
        if row is None:
            raise CheckbookError("transaction_not_found", operation_id)
        return row

    @staticmethod
    def _account_dict(row: sqlite3.Row) -> dict:
        return {
            "account_id": row["account_id"],
            "currency": row["currency"],
            "opening_balance_minor": row["opening_balance_minor"],
            "closed_through": row["closed_through"],
        }

    @staticmethod
    def _transaction_dict(row: sqlite3.Row) -> dict:
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

    def _audit(self, operation_id: str, event_type: str, account_id: str) -> None:
        self.connection.execute(
            """
            INSERT INTO audit_events(operation_id, event_type, account_id)
            VALUES (?, ?, ?)
            """,
            (operation_id, event_type, account_id),
        )

    @staticmethod
    def _check_open(account: sqlite3.Row, posted_date: str, operation_id: str) -> None:
        closed = account["closed_through"]
        if closed is not None and posted_date <= closed:
            raise CheckbookError("period_closed", operation_id)

    def create_account(
        self,
        account_id: str,
        currency: str,
        opening_balance_minor: int,
        operation_id: str,
    ) -> dict:
        operation_id = self._operation(operation_id)
        account_id = self._identifier(account_id, operation_id)
        opening_balance_minor = self._money(opening_balance_minor, operation_id)
        if not isinstance(currency, str) or not re.fullmatch(r"[A-Z]{3}", currency):
            raise CheckbookError("invalid_currency", operation_id)
        try:
            with self.connection:
                self.connection.execute(
                    """
                    INSERT INTO accounts(
                        account_id, currency, opening_balance_minor
                    ) VALUES (?, ?, ?)
                    """,
                    (account_id, currency, opening_balance_minor),
                )
                self._audit(operation_id, "account_created", account_id)
        except sqlite3.IntegrityError as error:
            raise CheckbookError("account_exists", operation_id) from error
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
        operation_id = self._operation(operation_id)
        account_id = self._identifier(account_id, operation_id)
        transaction_id = self._identifier(transaction_id, operation_id)
        posted_date = self._date(posted_date, operation_id)
        amount_minor = self._money(amount_minor, operation_id)
        if not isinstance(description, str):
            raise CheckbookError("invalid_description", operation_id)
        account = self._account_row(account_id, operation_id)
        self._check_open(account, posted_date, operation_id)
        try:
            with self.connection:
                self.connection.execute(
                    """
                    INSERT INTO transactions(
                        transaction_id, account_id, posted_date,
                        amount_minor, description
                    ) VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        transaction_id,
                        account_id,
                        posted_date,
                        amount_minor,
                        description,
                    ),
                )
                self._audit(operation_id, "transaction_recorded", account_id)
        except sqlite3.IntegrityError as error:
            raise CheckbookError("transaction_exists", operation_id) from error
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
        operation_id = self._operation(operation_id)
        transaction_id = self._identifier(transaction_id, operation_id)
        expected_version = self._money(expected_version, operation_id)
        posted_date = self._date(posted_date, operation_id)
        amount_minor = self._money(amount_minor, operation_id)
        if not isinstance(description, str):
            raise CheckbookError("invalid_description", operation_id)
        row = self._transaction_row(transaction_id, operation_id)
        if row["reconciled"]:
            raise CheckbookError("transaction_reconciled", operation_id)
        account = self._account_row(row["account_id"], operation_id)
        self._check_open(account, row["posted_date"], operation_id)
        self._check_open(
            account,
            posted_date,
            operation_id,
        )
        with self.connection:
            cursor = self.connection.execute(
                """
                UPDATE transactions
                SET posted_date = ?, amount_minor = ?, description = ?,
                    version = version + 1
                WHERE transaction_id = ? AND version = ? AND reconciled = 0
                """,
                (
                    posted_date,
                    amount_minor,
                    description,
                    transaction_id,
                    expected_version,
                ),
            )
            if cursor.rowcount != 1:
                raise CheckbookError("version_conflict", operation_id)
            self._audit(operation_id, "transaction_edited", row["account_id"])
        return self.get_transaction(transaction_id)

    def mark_cleared(
        self, transaction_id: str, expected_version: int, operation_id: str
    ) -> dict:
        operation_id = self._operation(operation_id)
        expected_version = self._money(expected_version, operation_id)
        row = self._transaction_row(transaction_id, operation_id)
        if row["reconciled"]:
            raise CheckbookError("transaction_reconciled", operation_id)
        self._check_open(
            self._account_row(row["account_id"], operation_id),
            row["posted_date"],
            operation_id,
        )
        with self.connection:
            cursor = self.connection.execute(
                """
                UPDATE transactions
                SET cleared = 1, version = version + 1
                WHERE transaction_id = ? AND version = ? AND reconciled = 0
                """,
                (transaction_id, expected_version),
            )
            if cursor.rowcount != 1:
                raise CheckbookError("version_conflict", operation_id)
            self._audit(operation_id, "transaction_cleared", row["account_id"])
        return self.get_transaction(transaction_id)

    @staticmethod
    def _import_id(account_id: str, source: str, external_id: str) -> str:
        value = f"{account_id}\0{source}\0{external_id}".encode()
        return f"imp-{hashlib.sha256(value).hexdigest()[:24]}"

    def import_csv(
        self,
        account_id: str,
        source: str,
        csv_text: str,
        operation_id: str,
    ) -> dict:
        operation_id = self._operation(operation_id)
        account_id = self._identifier(account_id, operation_id)
        source = self._identifier(source, operation_id)
        if not isinstance(csv_text, str):
            raise CheckbookError("invalid_csv", operation_id)
        account = self._account_row(account_id, operation_id)
        try:
            reader = csv.DictReader(io.StringIO(csv_text, newline=""))
            expected = ["external_id", "posted_date", "amount_minor", "description"]
            if reader.fieldnames != expected:
                raise ValueError
            rows = []
            for item in reader:
                if None in item or any(item[name] is None for name in expected):
                    raise ValueError
                external_id = self._identifier(item["external_id"], operation_id)
                posted_date = self._date(item["posted_date"], operation_id)
                self._check_open(account, posted_date, operation_id)
                amount_minor = self._money(int(item["amount_minor"]), operation_id)
                if str(amount_minor) != item["amount_minor"]:
                    raise ValueError
                rows.append(
                    (
                        external_id,
                        posted_date,
                        amount_minor,
                        item["description"],
                    )
                )
        except (ValueError, csv.Error) as error:
            raise CheckbookError("invalid_csv", operation_id) from error

        inserted = 0
        duplicates = 0
        with self.connection:
            for external_id, posted_date, amount_minor, description in rows:
                existing = self.connection.execute(
                    """
                    SELECT * FROM transactions
                    WHERE account_id = ? AND source = ? AND external_id = ?
                    """,
                    (account_id, source, external_id),
                ).fetchone()
                if existing is not None:
                    identity = (
                        existing["posted_date"],
                        existing["amount_minor"],
                        existing["description"],
                    )
                    if identity != (posted_date, amount_minor, description):
                        raise CheckbookError("duplicate_conflict", operation_id)
                    duplicates += 1
                    continue
                self.connection.execute(
                    """
                    INSERT INTO transactions(
                        transaction_id, account_id, posted_date, amount_minor,
                        description, source, external_id
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        self._import_id(account_id, source, external_id),
                        account_id,
                        posted_date,
                        amount_minor,
                        description,
                        source,
                        external_id,
                    ),
                )
                inserted += 1
            if inserted:
                self._audit(operation_id, "statement_imported", account_id)
        return {"inserted": inserted, "duplicates": duplicates}

    def reconcile(
        self,
        account_id: str,
        statement_date: str,
        ending_balance_minor: int,
        operation_id: str,
    ) -> dict:
        operation_id = self._operation(operation_id)
        account_id = self._identifier(account_id, operation_id)
        statement_date = self._date(statement_date, operation_id)
        ending_balance_minor = self._money(ending_balance_minor, operation_id)
        account = self._account_row(account_id, operation_id)
        self._check_open(account, statement_date, operation_id)
        reconciled_total = self.connection.execute(
            """
            SELECT COALESCE(SUM(amount_minor), 0) FROM transactions
            WHERE account_id = ? AND reconciled = 1
            """,
            (account_id,),
        ).fetchone()[0]
        candidates = self.connection.execute(
            """
            SELECT transaction_id, amount_minor FROM transactions
            WHERE account_id = ? AND cleared = 1 AND reconciled = 0
              AND posted_date <= ? ORDER BY transaction_id
            """,
            (account_id, statement_date),
        ).fetchall()
        actual = (
            account["opening_balance_minor"]
            + reconciled_total
            + sum(row["amount_minor"] for row in candidates)
        )
        if actual != ending_balance_minor:
            raise CheckbookError("reconciliation_mismatch", operation_id)
        with self.connection:
            for row in candidates:
                self.connection.execute(
                    """
                    UPDATE transactions SET reconciled = 1, version = version + 1
                    WHERE transaction_id = ?
                    """,
                    (row["transaction_id"],),
                )
            cursor = self.connection.execute(
                """
                INSERT INTO reconciliations(
                    account_id, statement_date, ending_balance_minor
                ) VALUES (?, ?, ?)
                """,
                (account_id, statement_date, ending_balance_minor),
            )
            self._audit(operation_id, "account_reconciled", account_id)
        return {
            "reconciliation_id": cursor.lastrowid,
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
        operation_id = self._operation(operation_id)
        original = self._transaction_row(original_transaction_id, operation_id)
        if not original["reconciled"]:
            raise CheckbookError("transaction_not_reconciled", operation_id)
        posted_date = self._date(posted_date, operation_id)
        account = self._account_row(original["account_id"], operation_id)
        self._check_open(account, posted_date, operation_id)
        duplicate = self.connection.execute(
            "SELECT 1 FROM transactions WHERE reversal_of = ?",
            (original_transaction_id,),
        ).fetchone()
        if duplicate is not None:
            raise CheckbookError("duplicate_reversal", operation_id)
        try:
            with self.connection:
                self.connection.execute(
                    """
                    INSERT INTO transactions(
                        transaction_id, account_id, posted_date, amount_minor,
                        description, reversal_of
                    ) VALUES (?, ?, ?, ?, ?, ?)
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
                self._audit(
                    operation_id,
                    "transaction_reversed",
                    original["account_id"],
                )
        except sqlite3.IntegrityError as error:
            raise CheckbookError("transaction_exists", operation_id) from error
        return self.get_transaction(reversal_transaction_id)

    def close_period(
        self, account_id: str, through_date: str, operation_id: str
    ) -> dict:
        operation_id = self._operation(operation_id)
        through_date = self._date(through_date, operation_id)
        account = self._account_row(account_id, operation_id)
        if account["closed_through"] is not None:
            if through_date < account["closed_through"]:
                raise CheckbookError("close_cannot_move_backward", operation_id)
            if through_date == account["closed_through"]:
                return self.get_account(account_id)
        with self.connection:
            self.connection.execute(
                "UPDATE accounts SET closed_through = ? WHERE account_id = ?",
                (through_date, account_id),
            )
            self._audit(operation_id, "period_closed", account_id)
        return self.get_account(account_id)

    def get_account(self, account_id: str) -> dict:
        return self._account_dict(self._account_row(account_id))

    def get_transaction(self, transaction_id: str) -> dict:
        return self._transaction_dict(self._transaction_row(transaction_id))

    def list_transactions(self, account_id: str) -> list[dict]:
        self._account_row(account_id)
        rows = self.connection.execute(
            """
            SELECT * FROM transactions
            WHERE account_id = ? ORDER BY transaction_id
            """,
            (account_id,),
        ).fetchall()
        return [self._transaction_dict(row) for row in rows]

    def list_audit_events(self) -> list[dict]:
        rows = self.connection.execute(
            "SELECT * FROM audit_events ORDER BY event_id"
        ).fetchall()
        return [dict(row) for row in rows]
