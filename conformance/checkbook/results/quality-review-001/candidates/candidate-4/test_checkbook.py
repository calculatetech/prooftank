import tempfile
import unittest
from pathlib import Path

from checkbook import Checkbook, CheckbookError


class CheckbookTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self.tempdir.name) / "checkbook.sqlite3")
        self.book = Checkbook(self.db_path)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_account_and_transaction_lifecycle_persists_across_reopen(self) -> None:
        account = self.book.create_account("acct-1", "USD", 5000, "op-1")
        self.assertEqual(
            account,
            {
                "account_id": "acct-1",
                "currency": "USD",
                "opening_balance_minor": 5000,
                "closed_through_date": None,
                "current_balance_minor": 5000,
            },
        )

        first = self.book.record_transaction("acct-1", "txn-2", "2026-08-11", -250, "Coffee", "op-2")
        second = self.book.record_transaction("acct-1", "txn-1", "2026-08-10", 1200, "Deposit", "op-3")
        self.assertEqual(first["version"], 1)
        self.assertFalse(first["cleared"])
        self.assertFalse(first["reconciled"])

        edited = self.book.edit_transaction("txn-2", 1, "2026-08-11", -300, "Lunch", "op-4")
        self.assertEqual(edited["amount_minor"], -300)
        self.assertEqual(edited["description"], "Lunch")
        self.assertEqual(edited["version"], 2)

        cleared = self.book.mark_cleared("txn-2", 2, "op-5")
        self.assertTrue(cleared["cleared"])
        self.assertEqual(cleared["version"], 3)

        listed = self.book.list_transactions("acct-1")
        self.assertEqual([row["transaction_id"] for row in listed], ["txn-1", "txn-2"])
        self.assertEqual(self.book.get_account("acct-1")["current_balance_minor"], 5900)

        reopened = Checkbook(self.db_path)
        self.assertEqual(reopened.get_transaction("txn-2"), cleared)
        self.assertEqual(
            [row["event_id"] for row in reopened.list_audit_events()],
            ["evt-000001", "evt-000002", "evt-000003", "evt-000004", "evt-000005"],
        )

    def test_validation_and_stale_version_errors_are_machine_readable(self) -> None:
        self.book.create_account("acct-1", "USD", 0, "op-1")
        with self.assertRaises(CheckbookError) as ctx:
            self.book.record_transaction("acct-1", "txn-1", "2026-02-30", 10, "Bad", "op-2")
        self.assertEqual(ctx.exception.code, "invalid_posted_date")
        self.assertEqual(ctx.exception.operation_id, "op-2")

        with self.assertRaises(CheckbookError) as noncanonical:
            self.book.record_transaction("acct-1", "txn-1", "20260811", 10, "Bad", "op-2b")
        self.assertEqual(noncanonical.exception.code, "invalid_posted_date")
        self.assertEqual(noncanonical.exception.operation_id, "op-2b")

        txn = self.book.record_transaction("acct-1", "txn-1", "2026-02-28", 10, "Good", "op-3")
        with self.assertRaises(CheckbookError) as stale:
            self.book.edit_transaction("txn-1", txn["version"] + 1, "2026-02-28", 11, "Edit", "op-4")
        self.assertEqual(stale.exception.code, "stale_version")
        self.assertEqual(stale.exception.operation_id, "op-4")

        with self.assertRaises(CheckbookError) as amount:
            self.book.create_account("acct-2", "USD", True, "op-5")
        self.assertEqual(amount.exception.code, "invalid_amount_minor")

    def test_import_csv_is_atomic_and_idempotent(self) -> None:
        self.book.create_account("acct-1", "USD", 0, "op-1")
        result = self.book.import_csv(
            "acct-1",
            "bank-a",
            "\n".join(
                [
                    "external_id,posted_date,amount_minor,description",
                    "e-1,2026-08-01,100,Paycheck",
                    "e-2,2026-08-02,-25,Snacks",
                ]
            ),
            "op-2",
        )
        self.assertEqual(result, {"inserted": 2, "duplicates": 0})
        transaction_ids = [row["transaction_id"] for row in self.book.list_transactions("acct-1")]
        self.assertEqual(len(transaction_ids), 2)
        self.assertTrue(all(tid.startswith("import-") for tid in transaction_ids))

        duplicate = self.book.import_csv(
            "acct-1",
            "bank-a",
            "\n".join(
                [
                    "external_id,posted_date,amount_minor,description",
                    "e-1,2026-08-01,100,Paycheck",
                    "e-2,2026-08-02,-25,Snacks",
                ]
            ),
            "op-3",
        )
        self.assertEqual(duplicate, {"inserted": 0, "duplicates": 2})
        self.assertEqual(len(self.book.list_transactions("acct-1")), 2)

        before_events = len(self.book.list_audit_events())
        with self.assertRaises(CheckbookError) as conflict:
            self.book.import_csv(
                "acct-1",
                "bank-a",
                "\n".join(
                    [
                        "external_id,posted_date,amount_minor,description",
                        "e-1,2026-08-01,999,Changed",
                    ]
                ),
                "op-4",
            )
        self.assertEqual(conflict.exception.code, "duplicate_conflict")
        self.assertEqual(conflict.exception.operation_id, "op-4")
        self.assertEqual(len(self.book.list_transactions("acct-1")), 2)
        self.assertEqual(len(self.book.list_audit_events()), before_events)

        with self.assertRaises(CheckbookError) as malformed:
            self.book.import_csv(
                "acct-1",
                "bank-a",
                "\n".join(
                    [
                        "external_id,posted_date,amount_minor,description",
                        "bad,2026-08-03,5",
                    ]
                ),
                "op-5",
            )
        self.assertEqual(malformed.exception.code, "invalid_csv_row")
        self.assertEqual(malformed.exception.operation_id, "op-5")

    def test_reconcile_reverse_and_close_period_rules(self) -> None:
        self.book.create_account("acct-1", "USD", 1000, "op-1")
        t1 = self.book.record_transaction("acct-1", "txn-1", "2026-08-01", 500, "Deposit", "op-2")
        self.book.record_transaction("acct-1", "txn-2", "2026-08-02", -100, "Groceries", "op-3")
        self.book.mark_cleared("txn-1", t1["version"], "op-4")

        with self.assertRaises(CheckbookError) as mismatch:
            self.book.reconcile("acct-1", "2026-08-31", 1000, "op-5")
        self.assertEqual(mismatch.exception.code, "reconciliation_mismatch")
        self.assertEqual(mismatch.exception.operation_id, "op-5")
        self.assertFalse(self.book.get_transaction("txn-1")["reconciled"])

        reconciled = self.book.reconcile("acct-1", "2026-08-31", 1500, "op-6")
        self.assertEqual(
            reconciled,
            {
                "account_id": "acct-1",
                "statement_date": "2026-08-31",
                "ending_balance_minor": 1500,
            },
        )
        self.assertTrue(self.book.get_transaction("txn-1")["reconciled"])
        self.assertFalse(self.book.get_transaction("txn-2")["reconciled"])

        reversal = self.book.reverse_reconciled_transaction("txn-1", "txn-3", "2026-09-01", "op-7")
        self.assertEqual(reversal["reversal_of"], "txn-1")
        self.assertEqual(reversal["amount_minor"], -500)

        with self.assertRaises(CheckbookError) as duplicate:
            self.book.reverse_reconciled_transaction("txn-1", "txn-4", "2026-09-02", "op-8")
        self.assertEqual(duplicate.exception.code, "duplicate_reversal")

        closed = self.book.close_period("acct-1", "2026-08-31", "op-9")
        self.assertEqual(closed["closed_through_date"], "2026-08-31")

        with self.assertRaises(CheckbookError) as closed_record:
            self.book.record_transaction("acct-1", "txn-5", "2026-08-15", -20, "Blocked", "op-10")
        self.assertEqual(closed_record.exception.code, "closed_period")

        with self.assertRaises(CheckbookError) as closed_clear:
            self.book.mark_cleared("txn-2", 1, "op-11")
        self.assertEqual(closed_clear.exception.code, "closed_period")

        with self.assertRaises(CheckbookError) as backwards:
            self.book.close_period("acct-1", "2026-08-15", "op-12")
        self.assertEqual(backwards.exception.code, "period_close_backwards")

        with self.assertRaises(CheckbookError) as closed_import:
            self.book.import_csv(
                "acct-1",
                "bank-a",
                "\n".join(
                    [
                        "external_id,posted_date,amount_minor,description",
                        "e-1,2026-08-20,5,Blocked",
                    ]
                ),
                "op-13",
            )
        self.assertEqual(closed_import.exception.code, "closed_period")
        self.assertEqual(closed_import.exception.operation_id, "op-13")


if __name__ == "__main__":
    unittest.main()
