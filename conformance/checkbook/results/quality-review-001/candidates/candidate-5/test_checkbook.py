import os
import tempfile
import unittest

from checkbook import Checkbook, CheckbookError


class CheckbookTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tmpdir.name, "checkbook.sqlite3")
        self.book = Checkbook(self.db_path)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_account_creation_and_audit_persist(self):
        account = self.book.create_account("acct-1", "USD", 500, "op-1")
        self.assertEqual(
            account,
            {
                "account_id": "acct-1",
                "currency": "USD",
                "opening_balance_minor": 500,
                "closed_through_date": None,
            },
        )
        reopened = Checkbook(self.db_path)
        self.assertEqual(reopened.get_account("acct-1"), account)
        self.assertEqual(
            reopened.list_audit_events(),
            [
                {
                    "event_id": 1,
                    "operation_id": "op-1",
                    "event_type": "account_created",
                    "account_id": "acct-1",
                }
            ],
        )

    def test_transaction_edit_clear_and_stale_version(self):
        self.book.create_account("acct-1", "USD", 0, "op-1")
        tx = self.book.record_transaction("acct-1", "tx-1", "2026-08-01", -25, "Lunch", "op-2")
        self.assertEqual(tx["version"], 1)
        edited = self.book.edit_transaction("tx-1", 1, "2026-08-02", -30, "Team lunch", "op-3")
        self.assertEqual(edited["version"], 2)
        self.assertEqual(edited["posted_date"], "2026-08-02")
        cleared = self.book.mark_cleared("tx-1", 2, "op-4")
        self.assertTrue(cleared["cleared"])
        self.assertEqual(cleared["version"], 3)
        with self.assertRaises(CheckbookError) as exc:
            self.book.edit_transaction("tx-1", 2, "2026-08-03", -40, "Mismatch", "op-5")
        self.assertEqual(exc.exception.code, "stale_version")
        self.assertEqual(
            [event["event_type"] for event in self.book.list_audit_events()],
            [
                "account_created",
                "transaction_recorded",
                "transaction_edited",
                "transaction_cleared",
            ],
        )

    def test_import_is_atomic_and_detects_duplicate_conflict(self):
        self.book.create_account("acct-1", "USD", 0, "op-1")
        ok_csv = (
            "external_id,posted_date,amount_minor,description\n"
            "e1,2026-08-01,-10,Coffee\n"
            "e1,2026-08-01,-10,Coffee\n"
            "e2,2026-08-02,100,Deposit\n"
        )
        result = self.book.import_csv("acct-1", "bank-a", ok_csv, "op-2")
        self.assertEqual(result, {"inserted": 2, "duplicates": 1})
        imported = self.book.list_transactions("acct-1")
        self.assertEqual([row["external_id"] for row in imported], ["e1", "e2"])
        retry = self.book.import_csv("acct-1", "bank-a", ok_csv, "op-3")
        self.assertEqual(retry, {"inserted": 0, "duplicates": 3})
        conflict_csv = (
            "external_id,posted_date,amount_minor,description\n"
            "e1,2026-08-01,-11,Coffee\n"
        )
        with self.assertRaises(CheckbookError) as exc:
            self.book.import_csv("acct-1", "bank-a", conflict_csv, "import-op")
        self.assertEqual(exc.exception.code, "duplicate_conflict")
        self.assertEqual(exc.exception.operation_id, "import-op")
        self.assertEqual(len(self.book.list_transactions("acct-1")), 2)
        self.assertEqual(len(self.book.list_audit_events()), 2)

    def test_reconcile_reverse_and_close_period_rules(self):
        self.book.create_account("acct-1", "USD", 1000, "op-1")
        self.book.record_transaction("acct-1", "tx-1", "2026-08-01", -100, "Groceries", "op-2")
        self.book.record_transaction("acct-1", "tx-2", "2026-08-03", 250, "Paycheck", "op-3")
        self.book.mark_cleared("tx-1", 1, "op-4")
        self.book.mark_cleared("tx-2", 1, "op-5")
        with self.assertRaises(CheckbookError) as exc:
            self.book.reconcile("acct-1", "2026-08-03", 9999, "recon-op")
        self.assertEqual(exc.exception.code, "reconciliation_mismatch")
        self.assertEqual(exc.exception.operation_id, "recon-op")
        self.book.reconcile("acct-1", "2026-08-03", 1150, "op-6")
        tx1 = self.book.get_transaction("tx-1")
        self.assertTrue(tx1["reconciled"])
        with self.assertRaises(CheckbookError) as exc:
            self.book.edit_transaction("tx-1", tx1["version"], "2026-08-04", -90, "Edit", "op-7")
        self.assertEqual(exc.exception.code, "reconciled_transaction")
        reversal = self.book.reverse_reconciled_transaction("tx-1", "tx-1-rev", "2026-08-04", "op-8")
        self.assertEqual(reversal["reversal_of"], "tx-1")
        self.assertEqual(reversal["amount_minor"], 100)
        with self.assertRaises(CheckbookError) as exc:
            self.book.reverse_reconciled_transaction("tx-1", "tx-1-rev-2", "2026-08-05", "op-9")
        self.assertEqual(exc.exception.code, "duplicate_reversal")
        closed = self.book.close_period("acct-1", "2026-08-03", "op-10")
        self.assertEqual(closed["closed_through_date"], "2026-08-03")
        with self.assertRaises(CheckbookError) as exc:
            self.book.record_transaction("acct-1", "tx-3", "2026-08-03", -5, "Blocked", "op-11")
        self.assertEqual(exc.exception.code, "closed_period")
        with self.assertRaises(CheckbookError) as exc:
            self.book.mark_cleared("tx-2", 2, "op-12")
        self.assertEqual(exc.exception.code, "reconciled_transaction")
        with self.assertRaises(CheckbookError) as exc:
            self.book.close_period("acct-1", "2026-08-02", "op-13")
        self.assertEqual(exc.exception.code, "closed_period_regression")

    def test_invalid_money_rejects_float_and_bool(self):
        self.book.create_account("acct-1", "USD", 0, "op-1")
        for bad in (1.5, True):
            with self.assertRaises(CheckbookError) as exc:
                self.book.record_transaction("acct-1", "tx-bad", "2026-08-01", bad, "Bad", "op-2")
            self.assertEqual(exc.exception.code, "invalid_amount_minor")


if __name__ == "__main__":
    unittest.main()
