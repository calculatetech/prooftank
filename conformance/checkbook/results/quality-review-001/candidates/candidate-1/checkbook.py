from __future__ import annotations

import csv
import datetime as _dt
import hashlib
import io
import re
import sqlite3


_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_CURRENCY_RE = re.compile(r"^[A-Z]{3}$")


class CheckbookError(Exception):
    def __init__(self, code: str, message: str | None = None, operation_id: str | None = None):
        super().__init__(message or code)
        self.code = code
        self.operation_id = operation_id


class Checkbook:
    def __init__(self, database_path: str):
        if not isinstance(database_path, str) or not database_path:
            raise CheckbookError("invalid_database_path")
        self._conn = sqlite3.connect(database_path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON")
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
                source TEXT,
                external_id TEXT
            );

            CREATE UNIQUE INDEX IF NOT EXISTS idx_import_identity
            ON transactions(account_id, source, external_id)
            WHERE source IS NOT NULL AND external_id IS NOT NULL;

            CREATE UNIQUE INDEX IF NOT EXISTS idx_reversal_once
            ON transactions(reversal_of)
            WHERE reversal_of IS NOT NULL;

            CREATE TABLE IF NOT EXISTS audit_events (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                account_id TEXT NOT NULL REFERENCES accounts(account_id),
                transaction_id TEXT
            );
            """
        )

    def create_account(
        self,
        account_id: str,
        currency: str,
        opening_balance_minor: int,
        operation_id: str,
    ) -> dict:
        self._require_operation_id(operation_id)
        self._require_identifier(account_id, "account_id", operation_id)
        self._require_currency(currency, operation_id)
        self._require_minor_units(opening_balance_minor, "opening_balance_minor", operation_id)
        try:
            with self._conn:
                if self._fetchone(
                    "SELECT 1 FROM accounts WHERE account_id = ?",
                    (account_id,),
                ):
                    self._error("account_exists", operation_id)
                self._conn.execute(
                    """
                    INSERT INTO accounts(account_id, currency, opening_balance_minor, closed_through_date)
                    VALUES (?, ?, ?, NULL)
                    """,
                    (account_id, currency, opening_balance_minor),
                )
                self._audit("account_created", account_id, operation_id)
        except sqlite3.DatabaseError as exc:
            self._storage_error(operation_id, exc)
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
        self._require_identifier(account_id, "account_id", operation_id)
        self._require_identifier(transaction_id, "transaction_id", operation_id)
        self._require_date(posted_date, operation_id)
        self._require_minor_units(amount_minor, "amount_minor", operation_id)
        self._require_text(description, "description", operation_id)
        try:
            with self._conn:
                account = self._get_account_row(account_id, operation_id)
                self._ensure_open_date(account["closed_through_date"], posted_date, operation_id)
                if self._fetchone(
                    "SELECT 1 FROM transactions WHERE transaction_id = ?",
                    (transaction_id,),
                ):
                    self._error("transaction_exists", operation_id)
                self._conn.execute(
                    """
                    INSERT INTO transactions(
                        transaction_id, account_id, posted_date, amount_minor, description,
                        version, cleared, reconciled, reversal_of, source, external_id
                    )
                    VALUES (?, ?, ?, ?, ?, 1, 0, 0, NULL, NULL, NULL)
                    """,
                    (transaction_id, account_id, posted_date, amount_minor, description),
                )
                self._audit("transaction_recorded", account_id, operation_id, transaction_id)
        except sqlite3.DatabaseError as exc:
            self._storage_error(operation_id, exc)
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
        self._require_identifier(transaction_id, "transaction_id", operation_id)
        self._require_minor_units(expected_version, "expected_version", operation_id)
        self._require_date(posted_date, operation_id)
        self._require_minor_units(amount_minor, "amount_minor", operation_id)
        self._require_text(description, "description", operation_id)
        try:
            with self._conn:
                row = self._get_transaction_row(transaction_id, operation_id)
                account = self._get_account_row(row["account_id"], operation_id)
                if row["version"] != expected_version:
                    self._error("stale_version", operation_id)
                if row["reconciled"]:
                    self._error("transaction_reconciled", operation_id)
                close_date = account["closed_through_date"]
                if close_date and (row["posted_date"] <= close_date or posted_date <= close_date):
                    self._error("period_closed", operation_id)
                self._conn.execute(
                    """
                    UPDATE transactions
                    SET posted_date = ?, amount_minor = ?, description = ?, version = version + 1
                    WHERE transaction_id = ?
                    """,
                    (posted_date, amount_minor, description, transaction_id),
                )
                self._audit("transaction_edited", row["account_id"], operation_id, transaction_id)
        except sqlite3.DatabaseError as exc:
            self._storage_error(operation_id, exc)
        return self.get_transaction(transaction_id)

    def mark_cleared(
        self,
        transaction_id: str,
        expected_version: int,
        operation_id: str,
    ) -> dict:
        self._require_operation_id(operation_id)
        self._require_identifier(transaction_id, "transaction_id", operation_id)
        self._require_minor_units(expected_version, "expected_version", operation_id)
        try:
            with self._conn:
                row = self._get_transaction_row(transaction_id, operation_id)
                account = self._get_account_row(row["account_id"], operation_id)
                if row["version"] != expected_version:
                    self._error("stale_version", operation_id)
                if row["reconciled"]:
                    self._error("transaction_reconciled", operation_id)
                self._ensure_open_date(account["closed_through_date"], row["posted_date"], operation_id)
                if row["cleared"]:
                    self._error("already_cleared", operation_id)
                self._conn.execute(
                    """
                    UPDATE transactions
                    SET cleared = 1, version = version + 1
                    WHERE transaction_id = ?
                    """,
                    (transaction_id,),
                )
                self._audit("transaction_cleared", row["account_id"], operation_id, transaction_id)
        except sqlite3.DatabaseError as exc:
            self._storage_error(operation_id, exc)
        return self.get_transaction(transaction_id)

    def import_csv(
        self,
        account_id: str,
        source: str,
        csv_text: str,
        operation_id: str,
    ) -> dict:
        self._require_operation_id(operation_id)
        self._require_identifier(account_id, "account_id", operation_id)
        self._require_identifier(source, "source", operation_id)
        self._require_text(csv_text, "csv_text", operation_id)
        try:
            with self._conn:
                account = self._get_account_row(account_id, operation_id)
                parsed_rows = self._parse_import_rows(
                    account_id,
                    source,
                    csv_text,
                    account["closed_through_date"],
                    operation_id,
                )
                inserted = 0
                duplicates = 0
                for row in parsed_rows:
                    existing = self._fetchone(
                        """
                        SELECT posted_date, amount_minor, description
                        FROM transactions
                        WHERE account_id = ? AND source = ? AND external_id = ?
                        """,
                        (account_id, source, row["external_id"]),
                    )
                    if existing:
                        if (
                            existing["posted_date"] != row["posted_date"]
                            or existing["amount_minor"] != row["amount_minor"]
                            or existing["description"] != row["description"]
                        ):
                            self._error("duplicate_conflict", operation_id)
                        duplicates += row["occurrences"]
                        continue
                    transaction_id = self._import_transaction_id(account_id, source, row["external_id"])
                    self._conn.execute(
                        """
                        INSERT INTO transactions(
                            transaction_id, account_id, posted_date, amount_minor, description,
                            version, cleared, reconciled, reversal_of, source, external_id
                        )
                        VALUES (?, ?, ?, ?, ?, 1, 0, 0, NULL, ?, ?)
                        """,
                        (
                            transaction_id,
                            account_id,
                            row["posted_date"],
                            row["amount_minor"],
                            row["description"],
                            source,
                            row["external_id"],
                        ),
                    )
                    inserted += 1
                    duplicates += row["occurrences"] - 1
                    self._audit("transaction_imported", account_id, operation_id, transaction_id)
        except sqlite3.DatabaseError as exc:
            self._storage_error(operation_id, exc)
        return {"inserted": inserted, "duplicates": duplicates}

    def reconcile(
        self,
        account_id: str,
        statement_date: str,
        ending_balance_minor: int,
        operation_id: str,
    ) -> dict:
        self._require_operation_id(operation_id)
        self._require_identifier(account_id, "account_id", operation_id)
        self._require_date(statement_date, operation_id)
        self._require_minor_units(ending_balance_minor, "ending_balance_minor", operation_id)
        try:
            with self._conn:
                account = self._get_account_row(account_id, operation_id)
                close_date = account["closed_through_date"]
                if close_date and statement_date <= close_date:
                    self._error("period_closed", operation_id)
                prior = self._fetchone(
                    """
                    SELECT COALESCE(SUM(amount_minor), 0) AS total
                    FROM transactions
                    WHERE account_id = ? AND reconciled = 1 AND posted_date <= ?
                    """,
                    (account_id, statement_date),
                )["total"]
                candidates = self._fetchall(
                    """
                    SELECT transaction_id, posted_date, amount_minor
                    FROM transactions
                    WHERE account_id = ? AND cleared = 1 AND reconciled = 0 AND posted_date <= ?
                    ORDER BY posted_date, transaction_id
                    """,
                    (account_id, statement_date),
                )
                if close_date and any(row["posted_date"] <= close_date for row in candidates):
                    self._error("period_closed", operation_id)
                candidate_total = sum(row["amount_minor"] for row in candidates)
                balance = account["opening_balance_minor"] + prior + candidate_total
                if balance != ending_balance_minor:
                    self._error("reconciliation_mismatch", operation_id)
                if candidates:
                    self._conn.executemany(
                        "UPDATE transactions SET reconciled = 1 WHERE transaction_id = ?",
                        [(row["transaction_id"],) for row in candidates],
                    )
                self._audit("reconciled", account_id, operation_id)
        except sqlite3.DatabaseError as exc:
            self._storage_error(operation_id, exc)
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
        self._require_identifier(original_transaction_id, "original_transaction_id", operation_id)
        self._require_identifier(reversal_transaction_id, "reversal_transaction_id", operation_id)
        self._require_date(posted_date, operation_id)
        try:
            with self._conn:
                original = self._get_transaction_row(original_transaction_id, operation_id)
                account = self._get_account_row(original["account_id"], operation_id)
                if not original["reconciled"]:
                    self._error("transaction_not_reconciled", operation_id)
                if original["reversal_of"] is not None:
                    self._error("invalid_reversal", operation_id)
                self._ensure_open_date(account["closed_through_date"], posted_date, operation_id)
                if self._fetchone(
                    "SELECT 1 FROM transactions WHERE reversal_of = ?",
                    (original_transaction_id,),
                ):
                    self._error("duplicate_reversal", operation_id)
                if self._fetchone(
                    "SELECT 1 FROM transactions WHERE transaction_id = ?",
                    (reversal_transaction_id,),
                ):
                    self._error("transaction_exists", operation_id)
                self._conn.execute(
                    """
                    INSERT INTO transactions(
                        transaction_id, account_id, posted_date, amount_minor, description,
                        version, cleared, reconciled, reversal_of, source, external_id
                    )
                    VALUES (?, ?, ?, ?, ?, 1, 0, 0, ?, NULL, NULL)
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
                self._audit("transaction_reversed", original["account_id"], operation_id, reversal_transaction_id)
        except sqlite3.DatabaseError as exc:
            self._storage_error(operation_id, exc)
        return self.get_transaction(reversal_transaction_id)

    def close_period(
        self,
        account_id: str,
        through_date: str,
        operation_id: str,
    ) -> dict:
        self._require_operation_id(operation_id)
        self._require_identifier(account_id, "account_id", operation_id)
        self._require_date(through_date, operation_id)
        try:
            with self._conn:
                account = self._get_account_row(account_id, operation_id)
                if account["closed_through_date"] and through_date < account["closed_through_date"]:
                    self._error("period_close_backwards", operation_id)
                self._conn.execute(
                    "UPDATE accounts SET closed_through_date = ? WHERE account_id = ?",
                    (through_date, account_id),
                )
                self._audit("period_closed", account_id, operation_id)
        except sqlite3.DatabaseError as exc:
            self._storage_error(operation_id, exc)
        return self.get_account(account_id)

    def get_account(self, account_id: str) -> dict:
        self._require_identifier(account_id, "account_id", None)
        row = self._get_account_row(account_id, None)
        return {
            "account_id": row["account_id"],
            "currency": row["currency"],
            "opening_balance_minor": row["opening_balance_minor"],
            "closed_through_date": row["closed_through_date"],
        }

    def get_transaction(self, transaction_id: str) -> dict:
        self._require_identifier(transaction_id, "transaction_id", None)
        row = self._get_transaction_row(transaction_id, None)
        return self._transaction_record(row)

    def list_transactions(self, account_id: str) -> list[dict]:
        self._require_identifier(account_id, "account_id", None)
        self._get_account_row(account_id, None)
        rows = self._fetchall(
            """
            SELECT transaction_id, account_id, posted_date, amount_minor, description,
                   version, cleared, reconciled, reversal_of, source, external_id
            FROM transactions
            WHERE account_id = ?
            ORDER BY posted_date, transaction_id
            """,
            (account_id,),
        )
        return [self._transaction_record(row) for row in rows]

    def list_audit_events(self) -> list[dict]:
        rows = self._fetchall(
            """
            SELECT event_id, operation_id, event_type, account_id
            FROM audit_events
            ORDER BY event_id
            """
        )
        return [
            {
                "event_id": row["event_id"],
                "operation_id": row["operation_id"],
                "event_type": row["event_type"],
                "account_id": row["account_id"],
            }
            for row in rows
        ]

    def _parse_import_rows(
        self,
        account_id: str,
        source: str,
        csv_text: str,
        closed_through_date: str | None,
        operation_id: str,
    ) -> list[dict]:
        reader = csv.reader(io.StringIO(csv_text, newline=""))
        header = next(reader, None)
        if header != ["external_id", "posted_date", "amount_minor", "description"]:
            self._error("invalid_csv_header", operation_id)
        seen: dict[str, dict] = {}
        for raw_row in reader:
            if len(raw_row) != 4:
                self._error("invalid_csv_row", operation_id)
            external_id, posted_date, amount_text, description = raw_row
            self._require_identifier(external_id, "external_id", operation_id)
            self._require_date(posted_date, operation_id)
            if closed_through_date and posted_date <= closed_through_date:
                self._error("period_closed", operation_id)
            amount_minor = self._parse_csv_amount(amount_text, operation_id)
            self._require_text(description, "description", operation_id)
            row = {
                "account_id": account_id,
                "source": source,
                "external_id": external_id,
                "posted_date": posted_date,
                "amount_minor": amount_minor,
                "description": description,
            }
            existing = seen.get(external_id)
            if existing:
                if (
                    existing["posted_date"] != posted_date
                    or existing["amount_minor"] != amount_minor
                    or existing["description"] != description
                ):
                    self._error("duplicate_conflict", operation_id)
                existing["occurrences"] += 1
                continue
            row["occurrences"] = 1
            seen[external_id] = row
        return [seen[key] for key in sorted(seen)]

    def _parse_csv_amount(self, text: str, operation_id: str) -> int:
        try:
            value = int(text)
        except ValueError:
            self._error("invalid_amount_minor", operation_id)
        self._require_minor_units(value, "amount_minor", operation_id)
        return value

    def _import_transaction_id(self, account_id: str, source: str, external_id: str) -> str:
        digest = hashlib.sha256(f"{account_id}\0{source}\0{external_id}".encode("utf-8")).hexdigest()
        return f"import-{digest[:24]}"

    def _audit(
        self,
        event_type: str,
        account_id: str,
        operation_id: str,
        transaction_id: str | None = None,
    ) -> None:
        self._conn.execute(
            """
            INSERT INTO audit_events(operation_id, event_type, account_id, transaction_id)
            VALUES (?, ?, ?, ?)
            """,
            (operation_id, event_type, account_id, transaction_id),
        )

    def _get_account_row(self, account_id: str, operation_id: str | None) -> sqlite3.Row:
        row = self._fetchone(
            """
            SELECT account_id, currency, opening_balance_minor, closed_through_date
            FROM accounts
            WHERE account_id = ?
            """,
            (account_id,),
        )
        if not row:
            self._error("account_not_found", operation_id)
        return row

    def _get_transaction_row(self, transaction_id: str, operation_id: str | None) -> sqlite3.Row:
        row = self._fetchone(
            """
            SELECT transaction_id, account_id, posted_date, amount_minor, description,
                   version, cleared, reconciled, reversal_of, source, external_id
            FROM transactions
            WHERE transaction_id = ?
            """,
            (transaction_id,),
        )
        if not row:
            self._error("transaction_not_found", operation_id)
        return row

    def _transaction_record(self, row: sqlite3.Row) -> dict:
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

    def _fetchone(self, sql: str, params: tuple = ()) -> sqlite3.Row | None:
        return self._conn.execute(sql, params).fetchone()

    def _fetchall(self, sql: str, params: tuple = ()) -> list[sqlite3.Row]:
        return list(self._conn.execute(sql, params).fetchall())

    def _require_operation_id(self, operation_id: str) -> None:
        if not isinstance(operation_id, str) or not operation_id:
            self._error("invalid_operation_id", operation_id if isinstance(operation_id, str) else None)

    def _require_identifier(self, value: str, field: str, operation_id: str | None) -> None:
        if not isinstance(value, str) or not value:
            self._error(f"invalid_{field}", operation_id)

    def _require_text(self, value: str, field: str, operation_id: str | None) -> None:
        if not isinstance(value, str):
            self._error(f"invalid_{field}", operation_id)

    def _require_minor_units(self, value: int, field: str, operation_id: str | None) -> None:
        if isinstance(value, bool) or not isinstance(value, int):
            self._error(f"invalid_{field}", operation_id)

    def _require_currency(self, currency: str, operation_id: str | None) -> None:
        if not isinstance(currency, str) or not _CURRENCY_RE.fullmatch(currency):
            self._error("invalid_currency", operation_id)

    def _require_date(self, value: str, operation_id: str | None) -> None:
        if not isinstance(value, str) or not _DATE_RE.fullmatch(value):
            self._error("invalid_date", operation_id)
        try:
            _dt.date.fromisoformat(value)
        except ValueError:
            self._error("invalid_date", operation_id)

    def _ensure_open_date(self, closed_through_date: str | None, posted_date: str, operation_id: str | None) -> None:
        if closed_through_date and posted_date <= closed_through_date:
            self._error("period_closed", operation_id)

    def _storage_error(self, operation_id: str | None, exc: sqlite3.DatabaseError) -> None:
        raise CheckbookError("storage_error", str(exc), operation_id) from exc

    def _error(self, code: str, operation_id: str | None) -> None:
        raise CheckbookError(code, code, operation_id)
