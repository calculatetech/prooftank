import os
import tempfile
import unittest

from checkbook import Checkbook, CheckbookError


class CheckbookTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tempdir.name, "checkbook.sqlite3")
        self.book = Checkbook(self.db_path)
        self.book.create_account("acct-1", "USD", 1000, "op-create-account")

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_create_and_reopen_persists_account_and_transaction(self) -> None:
        transaction = self.book.record_transaction(
            "acct-1",
            "txn-1",
            "2026-08-10",
            -250,
            "Groceries",
            "op-record-1",
        )
        self.assertEqual(transaction["version"], 1)
        self.assertFalse(transaction["cleared"])
        self.assertFalse(transaction["reconciled"])

        reopened = Checkbook(self.db_path)
        self.assertEqual(
            reopened.get_account("acct-1"),
            {
                "account_id": "acct-1",
                "currency": "USD",
                "opening_balance_minor": 1000,
                "closed_through_date": None,
                "current_balance_minor": 750,
            },
        )
        self.assertEqual(reopened.get_transaction("txn-1")["description"], "Groceries")
        self.assertEqual(
            [event["event_type"] for event in reopened.list_audit_events()],
            ["account_created", "transaction_recorded"],
        )

    def test_edit_and_clear_increment_version_and_detect_stale_version(self) -> None:
        self.book.record_transaction("acct-1", "txn-1", "2026-08-10", -250, "Groceries", "op-record-1")
        edited = self.book.edit_transaction(
            "txn-1",
            1,
            "2026-08-11",
            -275,
            "Market",
            "op-edit-1",
        )
        self.assertEqual(edited["version"], 2)
        self.assertEqual(edited["posted_date"], "2026-08-11")

        cleared = self.book.mark_cleared("txn-1", 2, "op-clear-1")
        self.assertEqual(cleared["version"], 3)
        self.assertTrue(cleared["cleared"])

        with self.assertRaises(CheckbookError) as ctx:
            self.book.edit_transaction("txn-1", 2, "2026-08-12", -300, "Late", "op-edit-2")
        self.assertEqual(ctx.exception.code, "stale_version")
        self.assertEqual(ctx.exception.operation_id, "op-edit-2")

    def test_import_csv_is_atomic_and_idempotent_for_identical_duplicates(self) -> None:
        csv_text = (
            "external_id,posted_date,amount_minor,description\n"
            "bank-1,2026-08-09,-100,Coffee\n"
            "bank-2,2026-08-10,500,Deposit\n"
        )
        result = self.book.import_csv("acct-1", "bank", csv_text, "op-import-1")
        self.assertEqual(result, {"inserted": 2, "duplicates": 0})
        repeated = self.book.import_csv("acct-1", "bank", csv_text, "op-import-2")
        self.assertEqual(repeated, {"inserted": 0, "duplicates": 2})

        transactions = self.book.list_transactions("acct-1")
        self.assertEqual([row["transaction_id"] for row in transactions], [
            "import:acct-1:bank:bank-1",
            "import:acct-1:bank:bank-2",
        ])
        self.assertEqual(
            [event["event_type"] for event in self.book.list_audit_events()],
            ["account_created", "transactions_imported"],
        )

    def test_import_csv_rejects_conflict_without_partial_writes(self) -> None:
        self.book.import_csv(
            "acct-1",
            "bank",
            "external_id,posted_date,amount_minor,description\nbank-1,2026-08-09,-100,Coffee\n",
            "op-import-1",
        )

        with self.assertRaises(CheckbookError) as ctx:
            self.book.import_csv(
                "acct-1",
                "bank",
                "external_id,posted_date,amount_minor,description\nbank-1,2026-08-09,-101,Coffee\n",
                "op-import-2",
            )
        self.assertEqual(ctx.exception.code, "duplicate_conflict")
        self.assertEqual(ctx.exception.operation_id, "op-import-2")
        self.assertEqual(len(self.book.list_transactions("acct-1")), 1)
        self.assertEqual(len(self.book.list_audit_events()), 2)

    def test_import_csv_storage_failure_returns_checkbook_error(self) -> None:
        self.book.record_transaction(
            "acct-1",
            "import:acct-1:bank:bank-1",
            "2026-08-08",
            -5,
            "Reserved id",
            "op-record-1",
        )

        with self.assertRaises(CheckbookError) as ctx:
            self.book.import_csv(
                "acct-1",
                "bank",
                "external_id,posted_date,amount_minor,description\nbank-1,2026-08-09,-100,Coffee\n",
                "op-import-1",
            )
        self.assertEqual(ctx.exception.code, "storage_failure")
        self.assertEqual(ctx.exception.operation_id, "op-import-1")
        self.assertEqual(len(self.book.list_transactions("acct-1")), 1)
        self.assertEqual(
            [event["event_type"] for event in self.book.list_audit_events()],
            ["account_created", "transaction_recorded"],
        )

    def test_reconcile_reverse_and_close_period_guards(self) -> None:
        self.book.record_transaction("acct-1", "txn-1", "2026-08-09", -200, "Rent", "op-record-1")
        self.book.record_transaction("acct-1", "txn-2", "2026-08-10", 50, "Refund", "op-record-2")
        self.book.mark_cleared("txn-1", 1, "op-clear-1")
        self.book.mark_cleared("txn-2", 1, "op-clear-2")

        with self.assertRaises(CheckbookError) as mismatch:
            self.book.reconcile("acct-1", "2026-08-10", 999, "op-reconcile-bad")
        self.assertEqual(mismatch.exception.code, "reconciliation_mismatch")
        self.assertEqual(mismatch.exception.operation_id, "op-reconcile-bad")

        result = self.book.reconcile("acct-1", "2026-08-10", 850, "op-reconcile-1")
        self.assertEqual(
            result,
            {
                "account_id": "acct-1",
                "statement_date": "2026-08-10",
                "ending_balance_minor": 850,
            },
        )
        self.assertTrue(self.book.get_transaction("txn-1")["reconciled"])

        reversal = self.book.reverse_reconciled_transaction(
            "txn-1",
            "txn-1-reversal",
            "2026-08-11",
            "op-reverse-1",
        )
        self.assertEqual(reversal["amount_minor"], 200)
        self.assertEqual(reversal["reversal_of"], "txn-1")

        with self.assertRaises(CheckbookError) as duplicate_reversal:
            self.book.reverse_reconciled_transaction(
                "txn-1",
                "txn-1-reversal-2",
                "2026-08-12",
                "op-reverse-2",
            )
        self.assertEqual(duplicate_reversal.exception.code, "duplicate_reversal")

        closed = self.book.close_period("acct-1", "2026-08-10", "op-close-1")
        self.assertEqual(closed["closed_through_date"], "2026-08-10")

        with self.assertRaises(CheckbookError) as closed_record:
            self.book.record_transaction("acct-1", "txn-3", "2026-08-10", -10, "Blocked", "op-record-3")
        self.assertEqual(closed_record.exception.code, "closed_period")

        with self.assertRaises(CheckbookError) as closed_reconcile:
            self.book.reconcile("acct-1", "2026-08-10", 850, "op-reconcile-2")
        self.assertEqual(closed_reconcile.exception.code, "closed_period")

    def test_reversal_date_must_be_later_than_original(self) -> None:
        self.book.record_transaction("acct-1", "txn-1", "2026-08-10", -200, "Rent", "op-record-1")
        self.book.mark_cleared("txn-1", 1, "op-clear-1")
        self.book.reconcile("acct-1", "2026-08-10", 800, "op-reconcile-1")

        with self.assertRaises(CheckbookError) as ctx:
            self.book.reverse_reconciled_transaction(
                "txn-1",
                "txn-1-reversal",
                "2026-08-09",
                "op-reverse-1",
            )
        self.assertEqual(ctx.exception.code, "invalid_reversal_date")
        self.assertEqual(ctx.exception.operation_id, "op-reverse-1")

    def test_reconciled_transaction_rejects_edit(self) -> None:
        self.book.record_transaction("acct-1", "txn-1", "2026-08-09", -200, "Rent", "op-record-1")
        self.book.mark_cleared("txn-1", 1, "op-clear-1")
        self.book.reconcile("acct-1", "2026-08-09", 800, "op-reconcile-1")

        with self.assertRaises(CheckbookError) as ctx:
            self.book.edit_transaction("txn-1", 2, "2026-08-09", -199, "Rent fix", "op-edit-1")
        self.assertEqual(ctx.exception.code, "reconciled_transaction")

    def test_validation_rejects_float_bool_and_invalid_date(self) -> None:
        with self.assertRaises(CheckbookError) as amount_error:
            self.book.record_transaction("acct-1", "txn-1", "2026-08-10", 1.5, "Bad", "op-record-1")
        self.assertEqual(amount_error.exception.code, "invalid_amount_minor")

        with self.assertRaises(CheckbookError) as bool_error:
            self.book.create_account("acct-2", "USD", True, "op-create-2")
        self.assertEqual(bool_error.exception.code, "invalid_amount_minor")

        with self.assertRaises(CheckbookError) as date_error:
            self.book.record_transaction("acct-1", "txn-2", "2026-02-30", -10, "Bad date", "op-record-2")
        self.assertEqual(date_error.exception.code, "invalid_date")


if __name__ == "__main__":
    unittest.main()
