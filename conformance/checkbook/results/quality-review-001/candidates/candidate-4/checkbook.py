from __future__ import annotations

import csv
import hashlib
import json
import re
import sqlite3
from contextlib import contextmanager
from datetime import date
from io import StringIO
from pathlib import Path


class CheckbookError(Exception):
    def __init__(self, code: str, message: str, operation_id: str | None = None):
        super().__init__(message)
        self.code = code
        self.operation_id = operation_id


class Checkbook:
    def __init__(self, database_path: str):
        self._database_path = database_path
        Path(database_path).parent.mkdir(parents=True, exist_ok=True)
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
        account_id = _require_identifier("account_id", account_id, operation_id)
        currency = _require_currency(currency, operation_id)
        opening_balance_minor = _require_minor_amount(opening_balance_minor, operation_id)
        operation_id = _require_operation_id(operation_id)
        with self._tx():
            existing = self._conn.execute(
                "SELECT 1 FROM accounts WHERE account_id = ?",
                (account_id,),
            ).fetchone()
            if existing:
                raise CheckbookError("account_exists", "account already exists", operation_id)
            self._conn.execute(
                """
                INSERT INTO accounts(account_id, currency, opening_balance_minor, closed_through_date)
                VALUES (?, ?, ?, NULL)
                """,
                (account_id, currency, opening_balance_minor),
            )
            self._insert_audit_event(
                operation_id,
                "account_created",
                account_id,
                details={"opening_balance_minor": opening_balance_minor},
            )
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
        account_id = _require_identifier("account_id", account_id, operation_id)
        transaction_id = _require_identifier("transaction_id", transaction_id, operation_id)
        posted_date = _require_iso_date(posted_date, "posted_date", operation_id)
        amount_minor = _require_minor_amount(amount_minor, operation_id)
        description = _require_description(description, operation_id)
        operation_id = _require_operation_id(operation_id)
        with self._tx():
            account = self._get_account_row(account_id, operation_id)
            self._ensure_open_date(account, posted_date, operation_id)
            existing = self._conn.execute(
                "SELECT 1 FROM transactions WHERE transaction_id = ?",
                (transaction_id,),
            ).fetchone()
            if existing:
                raise CheckbookError(
                    "transaction_exists",
                    "transaction already exists",
                    operation_id,
                )
            self._conn.execute(
                """
                INSERT INTO transactions(
                    transaction_id, account_id, posted_date, amount_minor, description,
                    version, cleared, reconciled, reversal_of, source, external_id
                ) VALUES (?, ?, ?, ?, ?, 1, 0, 0, NULL, NULL, NULL)
                """,
                (transaction_id, account_id, posted_date, amount_minor, description),
            )
            self._insert_audit_event(
                operation_id,
                "transaction_recorded",
                account_id,
                transaction_id=transaction_id,
            )
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
        transaction_id = _require_identifier("transaction_id", transaction_id, operation_id)
        expected_version = _require_version(expected_version, operation_id)
        posted_date = _require_iso_date(posted_date, "posted_date", operation_id)
        amount_minor = _require_minor_amount(amount_minor, operation_id)
        description = _require_description(description, operation_id)
        operation_id = _require_operation_id(operation_id)
        with self._tx():
            row = self._get_transaction_row(transaction_id, operation_id)
            if row["reconciled"]:
                raise CheckbookError(
                    "transaction_reconciled",
                    "reconciled transactions cannot be edited",
                    operation_id,
                )
            account = self._get_account_row(row["account_id"], operation_id)
            self._ensure_open_date(account, row["posted_date"], operation_id)
            self._ensure_open_date(account, posted_date, operation_id)
            self._require_current_version(row, expected_version, operation_id)
            self._conn.execute(
                """
                UPDATE transactions
                SET posted_date = ?, amount_minor = ?, description = ?, version = version + 1
                WHERE transaction_id = ?
                """,
                (posted_date, amount_minor, description, transaction_id),
            )
            self._insert_audit_event(
                operation_id,
                "transaction_edited",
                row["account_id"],
                transaction_id=transaction_id,
            )
            return self.get_transaction(transaction_id)

    def mark_cleared(
        self,
        transaction_id: str,
        expected_version: int,
        operation_id: str,
    ) -> dict:
        transaction_id = _require_identifier("transaction_id", transaction_id, operation_id)
        expected_version = _require_version(expected_version, operation_id)
        operation_id = _require_operation_id(operation_id)
        with self._tx():
            row = self._get_transaction_row(transaction_id, operation_id)
            if row["reconciled"]:
                raise CheckbookError(
                    "transaction_reconciled",
                    "reconciled transactions cannot be cleared",
                    operation_id,
                )
            if row["cleared"]:
                raise CheckbookError(
                    "transaction_already_cleared",
                    "transaction is already cleared",
                    operation_id,
                )
            account = self._get_account_row(row["account_id"], operation_id)
            self._ensure_open_date(account, row["posted_date"], operation_id)
            self._require_current_version(row, expected_version, operation_id)
            self._conn.execute(
                """
                UPDATE transactions
                SET cleared = 1, version = version + 1
                WHERE transaction_id = ?
                """,
                (transaction_id,),
            )
            self._insert_audit_event(
                operation_id,
                "transaction_cleared",
                row["account_id"],
                transaction_id=transaction_id,
            )
            return self.get_transaction(transaction_id)

    def import_csv(
        self,
        account_id: str,
        source: str,
        csv_text: str,
        operation_id: str,
    ) -> dict:
        operation_id = _require_operation_id(operation_id)
        account_id = _require_identifier("account_id", account_id, operation_id)
        source = _require_identifier("source", source, operation_id)
        if not isinstance(csv_text, str):
            raise CheckbookError("invalid_csv_text", "csv_text must be a string", operation_id)
        with self._tx():
            account = self._get_account_row(account_id, operation_id)
            rows = self._parse_csv_rows(csv_text, operation_id)
            seen: dict[tuple[str, str], dict] = {}
            inserted = 0
            duplicates = 0
            pending: list[dict] = []
            for row in rows:
                external_id = _require_identifier("external_id", row["external_id"], operation_id)
                posted_date = _require_iso_date(row["posted_date"], "posted_date", operation_id)
                self._ensure_open_date(account, posted_date, operation_id)
                amount_minor = _parse_csv_amount(row["amount_minor"], operation_id)
                description = _require_description(row["description"], operation_id)
                identity = (source, external_id)
                normalized = {
                    "source": source,
                    "external_id": external_id,
                    "posted_date": posted_date,
                    "amount_minor": amount_minor,
                    "description": description,
                }
                if identity in seen and seen[identity] != normalized:
                    raise CheckbookError(
                        "duplicate_conflict",
                        "duplicate identities in import differ",
                        operation_id,
                    )
                seen[identity] = normalized
                existing = self._conn.execute(
                    """
                    SELECT posted_date, amount_minor, description
                    FROM transactions
                    WHERE account_id = ? AND source = ? AND external_id = ?
                    """,
                    (account_id, source, external_id),
                ).fetchone()
                if existing:
                    if (
                        existing["posted_date"] != posted_date
                        or existing["amount_minor"] != amount_minor
                        or existing["description"] != description
                    ):
                        raise CheckbookError(
                            "duplicate_conflict",
                            "existing imported row differs",
                            operation_id,
                        )
                    duplicates += 1
                    continue
                pending.append(normalized)
            for row in pending:
                transaction_id = _import_transaction_id(account_id, row["source"], row["external_id"])
                collision = self._conn.execute(
                    "SELECT account_id, source, external_id FROM transactions WHERE transaction_id = ?",
                    (transaction_id,),
                ).fetchone()
                if collision:
                    if (
                        collision["account_id"] == account_id
                        and collision["source"] == row["source"]
                        and collision["external_id"] == row["external_id"]
                    ):
                        duplicates += 1
                        continue
                    raise CheckbookError(
                        "transaction_exists",
                        "imported transaction id collides with existing transaction",
                        operation_id,
                    )
                self._conn.execute(
                    """
                    INSERT INTO transactions(
                        transaction_id, account_id, posted_date, amount_minor, description,
                        version, cleared, reconciled, reversal_of, source, external_id
                    ) VALUES (?, ?, ?, ?, ?, 1, 0, 0, NULL, ?, ?)
                    """,
                    (
                        transaction_id,
                        account_id,
                        row["posted_date"],
                        row["amount_minor"],
                        row["description"],
                        row["source"],
                        row["external_id"],
                    ),
                )
                self._insert_audit_event(
                    operation_id,
                    "transaction_imported",
                    account_id,
                    transaction_id=transaction_id,
                )
                inserted += 1
            return {"inserted": inserted, "duplicates": duplicates}

    def reconcile(
        self,
        account_id: str,
        statement_date: str,
        ending_balance_minor: int,
        operation_id: str,
    ) -> dict:
        operation_id = _require_operation_id(operation_id)
        account_id = _require_identifier("account_id", account_id, operation_id)
        statement_date = _require_iso_date(statement_date, "statement_date", operation_id)
        ending_balance_minor = _require_minor_amount(ending_balance_minor, operation_id)
        with self._tx():
            account = self._get_account_row(account_id, operation_id)
            self._ensure_open_date(account, statement_date, operation_id)
            previously = self._conn.execute(
                """
                SELECT COALESCE(SUM(amount_minor), 0) AS total
                FROM transactions
                WHERE account_id = ? AND reconciled = 1
                """,
                (account_id,),
            ).fetchone()["total"]
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
                (account_id, statement_date),
            ).fetchall()
            candidate_total = 0
            for row in candidates:
                self._ensure_open_date(account, row["posted_date"], operation_id)
                candidate_total += row["amount_minor"]
            computed = account["opening_balance_minor"] + previously + candidate_total
            if computed != ending_balance_minor:
                raise CheckbookError(
                    "reconciliation_mismatch",
                    "reconciliation ending balance does not match",
                    operation_id,
                )
            if candidates:
                self._conn.executemany(
                    "UPDATE transactions SET reconciled = 1 WHERE transaction_id = ?",
                    [(row["transaction_id"],) for row in candidates],
                )
            self._insert_audit_event(
                operation_id,
                "account_reconciled",
                account_id,
                details={
                    "statement_date": statement_date,
                    "ending_balance_minor": ending_balance_minor,
                    "transaction_ids": [row["transaction_id"] for row in candidates],
                },
            )
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
        operation_id = _require_operation_id(operation_id)
        original_transaction_id = _require_identifier(
            "original_transaction_id",
            original_transaction_id,
            operation_id,
        )
        reversal_transaction_id = _require_identifier(
            "reversal_transaction_id",
            reversal_transaction_id,
            operation_id,
        )
        posted_date = _require_iso_date(posted_date, "posted_date", operation_id)
        with self._tx():
            original = self._get_transaction_row(original_transaction_id, operation_id)
            if not original["reconciled"]:
                raise CheckbookError(
                    "transaction_not_reconciled",
                    "only reconciled transactions can be reversed",
                    operation_id,
                )
            duplicate = self._conn.execute(
                "SELECT 1 FROM transactions WHERE reversal_of = ?",
                (original_transaction_id,),
            ).fetchone()
            if duplicate:
                raise CheckbookError(
                    "duplicate_reversal",
                    "transaction already has a reversal",
                    operation_id,
                )
            account = self._get_account_row(original["account_id"], operation_id)
            self._ensure_open_date(account, posted_date, operation_id)
            existing = self._conn.execute(
                "SELECT 1 FROM transactions WHERE transaction_id = ?",
                (reversal_transaction_id,),
            ).fetchone()
            if existing:
                raise CheckbookError(
                    "transaction_exists",
                    "transaction already exists",
                    operation_id,
                )
            self._conn.execute(
                """
                INSERT INTO transactions(
                    transaction_id, account_id, posted_date, amount_minor, description,
                    version, cleared, reconciled, reversal_of, source, external_id
                ) VALUES (?, ?, ?, ?, ?, 1, 0, 0, ?, NULL, NULL)
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
            self._insert_audit_event(
                operation_id,
                "transaction_reversed",
                original["account_id"],
                transaction_id=reversal_transaction_id,
                details={"reversal_of": original_transaction_id},
            )
            return self.get_transaction(reversal_transaction_id)

    def close_period(
        self,
        account_id: str,
        through_date: str,
        operation_id: str,
    ) -> dict:
        operation_id = _require_operation_id(operation_id)
        account_id = _require_identifier("account_id", account_id, operation_id)
        through_date = _require_iso_date(through_date, "through_date", operation_id)
        with self._tx():
            account = self._get_account_row(account_id, operation_id)
            current = account["closed_through_date"]
            if current and through_date < current:
                raise CheckbookError(
                    "period_close_backwards",
                    "closed-through date cannot move backward",
                    operation_id,
                )
            self._conn.execute(
                "UPDATE accounts SET closed_through_date = ? WHERE account_id = ?",
                (through_date, account_id),
            )
            self._insert_audit_event(
                operation_id,
                "period_closed",
                account_id,
                details={"through_date": through_date},
            )
            return self.get_account(account_id)

    def get_account(self, account_id: str) -> dict:
        account_id = _require_identifier("account_id", account_id, None)
        row = self._get_account_row(account_id, None)
        current_balance = self._conn.execute(
            """
            SELECT COALESCE(SUM(amount_minor), 0) AS total
            FROM transactions
            WHERE account_id = ?
            """,
            (account_id,),
        ).fetchone()["total"]
        return {
            "account_id": row["account_id"],
            "currency": row["currency"],
            "opening_balance_minor": row["opening_balance_minor"],
            "closed_through_date": row["closed_through_date"],
            "current_balance_minor": row["opening_balance_minor"] + current_balance,
        }

    def get_transaction(self, transaction_id: str) -> dict:
        transaction_id = _require_identifier("transaction_id", transaction_id, None)
        row = self._get_transaction_row(transaction_id, None)
        return _transaction_dict(row)

    def list_transactions(self, account_id: str) -> list[dict]:
        account_id = _require_identifier("account_id", account_id, None)
        self._get_account_row(account_id, None)
        rows = self._conn.execute(
            """
            SELECT *
            FROM transactions
            WHERE account_id = ?
            ORDER BY posted_date, transaction_id
            """,
            (account_id,),
        ).fetchall()
        return [_transaction_dict(row) for row in rows]

    def list_audit_events(self) -> list[dict]:
        rows = self._conn.execute(
            """
            SELECT event_id, operation_id, event_type, account_id, transaction_id, details_json
            FROM audit_events
            ORDER BY sequence_id
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
                account_id TEXT NOT NULL REFERENCES accounts(account_id) ON DELETE RESTRICT,
                posted_date TEXT NOT NULL,
                amount_minor INTEGER NOT NULL,
                description TEXT NOT NULL,
                version INTEGER NOT NULL,
                cleared INTEGER NOT NULL,
                reconciled INTEGER NOT NULL,
                reversal_of TEXT REFERENCES transactions(transaction_id) ON DELETE RESTRICT,
                source TEXT,
                external_id TEXT
            );

            CREATE UNIQUE INDEX IF NOT EXISTS idx_import_identity
            ON transactions(account_id, source, external_id)
            WHERE source IS NOT NULL AND external_id IS NOT NULL;

            CREATE TABLE IF NOT EXISTS audit_events (
                sequence_id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT UNIQUE,
                operation_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                account_id TEXT NOT NULL REFERENCES accounts(account_id) ON DELETE RESTRICT,
                transaction_id TEXT REFERENCES transactions(transaction_id) ON DELETE RESTRICT,
                details_json TEXT
            );
            """
        )

    @contextmanager
    def _tx(self):
        try:
            self._conn.execute("BEGIN")
            yield
        except Exception:
            self._conn.rollback()
            raise
        else:
            self._conn.commit()

    def _get_account_row(self, account_id: str, operation_id: str | None) -> sqlite3.Row:
        row = self._conn.execute(
            "SELECT * FROM accounts WHERE account_id = ?",
            (account_id,),
        ).fetchone()
        if not row:
            raise CheckbookError("account_not_found", "account not found", operation_id)
        return row

    def _get_transaction_row(self, transaction_id: str, operation_id: str | None) -> sqlite3.Row:
        row = self._conn.execute(
            "SELECT * FROM transactions WHERE transaction_id = ?",
            (transaction_id,),
        ).fetchone()
        if not row:
            raise CheckbookError("transaction_not_found", "transaction not found", operation_id)
        return row

    def _insert_audit_event(
        self,
        operation_id: str,
        event_type: str,
        account_id: str,
        transaction_id: str | None = None,
        details: dict | None = None,
    ) -> None:
        cursor = self._conn.execute(
            """
            INSERT INTO audit_events(event_id, operation_id, event_type, account_id, transaction_id, details_json)
            VALUES (NULL, ?, ?, ?, ?, ?)
            """,
            (
                operation_id,
                event_type,
                account_id,
                transaction_id,
                json.dumps(details, sort_keys=True) if details is not None else None,
            ),
        )
        sequence_id = cursor.lastrowid
        event_id = f"evt-{sequence_id:06d}"
        self._conn.execute(
            "UPDATE audit_events SET event_id = ? WHERE sequence_id = ?",
            (event_id, sequence_id),
        )

    def _ensure_open_date(
        self,
        account: sqlite3.Row,
        effective_date: str,
        operation_id: str,
    ) -> None:
        closed_through = account["closed_through_date"]
        if closed_through and effective_date <= closed_through:
            raise CheckbookError(
                "closed_period",
                "transaction effect falls in a closed period",
                operation_id,
            )

    def _require_current_version(
        self,
        row: sqlite3.Row,
        expected_version: int,
        operation_id: str,
    ) -> None:
        if row["version"] != expected_version:
            raise CheckbookError("stale_version", "expected version is stale", operation_id)

    def _parse_csv_rows(self, csv_text: str, operation_id: str) -> list[dict[str, str]]:
        reader = csv.reader(StringIO(csv_text))
        rows = list(reader)
        if not rows or rows[0] != [
            "external_id",
            "posted_date",
            "amount_minor",
            "description",
        ]:
            raise CheckbookError("invalid_csv_header", "csv header is invalid", operation_id)
        parsed: list[dict[str, str]] = []
        for raw in rows[1:]:
            if len(raw) != 4:
                raise CheckbookError("invalid_csv_row", "csv row is malformed", operation_id)
            parsed.append(
                {
                    "external_id": raw[0],
                    "posted_date": raw[1],
                    "amount_minor": raw[2],
                    "description": raw[3],
                }
            )
        return parsed


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


def _require_identifier(name: str, value: str, operation_id: str | None) -> str:
    if not isinstance(value, str) or not value:
        raise CheckbookError(f"invalid_{name}", f"{name} must be a non-empty string", operation_id)
    return value


def _require_operation_id(operation_id: str) -> str:
    return _require_identifier("operation_id", operation_id, operation_id if isinstance(operation_id, str) else None)


def _require_currency(currency: str, operation_id: str | None) -> str:
    if not isinstance(currency, str) or len(currency) != 3 or not currency.isupper() or not currency.isalpha():
        raise CheckbookError("invalid_currency", "currency must be a three-letter uppercase code", operation_id)
    return currency


def _require_iso_date(value: str, field_name: str, operation_id: str | None) -> str:
    if not isinstance(value, str):
        raise CheckbookError(f"invalid_{field_name}", f"{field_name} must be a string", operation_id)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise CheckbookError(f"invalid_{field_name}", f"{field_name} must be a real ISO date", operation_id)
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise CheckbookError(f"invalid_{field_name}", f"{field_name} must be a real ISO date", operation_id) from exc
    return value


def _require_minor_amount(value: int, operation_id: str | None) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise CheckbookError("invalid_amount_minor", "amount_minor must be an integer", operation_id)
    return value


def _parse_csv_amount(value: str, operation_id: str | None) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise CheckbookError("invalid_amount_minor", "amount_minor must be an integer", operation_id) from exc
    return _require_minor_amount(parsed, operation_id)


def _require_description(value: str, operation_id: str | None) -> str:
    if not isinstance(value, str):
        raise CheckbookError("invalid_description", "description must be a string", operation_id)
    return value


def _require_version(value: int, operation_id: str | None) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise CheckbookError("invalid_expected_version", "expected_version must be a positive integer", operation_id)
    return value


def _import_transaction_id(account_id: str, source: str, external_id: str) -> str:
    digest = hashlib.sha256(f"{account_id}\0{source}\0{external_id}".encode("utf-8")).hexdigest()[:24]
    return f"import-{digest}"
