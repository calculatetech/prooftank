import os
import tempfile
import unittest

from checkbook import Checkbook, CheckbookError


class CheckbookTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "checkbook.sqlite3")
        self.book = Checkbook(self.path)

    def tearDown(self):
        self.tmp.cleanup()

    def test_account_transaction_and_persistence(self):
        created = self.book.create_account("acct", "USD", 1000, "op-1")
        self.assertEqual(
            created,
            {
                "account_id": "acct",
                "currency": "USD",
                "opening_balance_minor": 1000,
                "closed_through_date": None,
            },
        )
        tx = self.book.record_transaction("acct", "tx-1", "2026-08-01", -250, "Lunch", "op-2")
        self.assertEqual(tx["version"], 1)
        self.assertFalse(tx["cleared"])
        reopened = Checkbook(self.path)
        self.assertEqual(reopened.get_transaction("tx-1")["amount_minor"], -250)
        self.assertEqual([e["event_type"] for e in reopened.list_audit_events()], ["account_created", "transaction_recorded"])

    def test_edit_and_clear_version_rules(self):
        self.book.create_account("acct", "USD", 0, "op-1")
        self.book.record_transaction("acct", "tx-1", "2026-08-01", -100, "A", "op-2")
        edited = self.book.edit_transaction("tx-1", 1, "2026-08-02", -150, "B", "op-3")
        self.assertEqual((edited["version"], edited["posted_date"], edited["amount_minor"]), (2, "2026-08-02", -150))
        with self.assertRaises(CheckbookError) as stale:
            self.book.mark_cleared("tx-1", 1, "op-4")
        self.assertEqual(stale.exception.code, "stale_version")
        cleared = self.book.mark_cleared("tx-1", 2, "op-5")
        self.assertEqual((cleared["version"], cleared["cleared"]), (3, True))

    def test_import_is_atomic_and_idempotent(self):
        self.book.create_account("acct", "USD", 0, "op-1")
        csv_text = (
            "external_id,posted_date,amount_minor,description\n"
            "e1,2026-08-01,100,Paycheck\n"
            "e2,2026-08-02,-25,Coffee\n"
        )
        result = self.book.import_csv("acct", "bank", csv_text, "op-2")
        self.assertEqual(result, {"inserted": 2, "duplicates": 0})
        again = self.book.import_csv("acct", "bank", csv_text, "op-3")
        self.assertEqual(again, {"inserted": 0, "duplicates": 2})
        conflict_csv = (
            "external_id,posted_date,amount_minor,description\n"
            "e1,2026-08-01,101,Paycheck\n"
        )
        with self.assertRaises(CheckbookError) as err:
            self.book.import_csv("acct", "bank", conflict_csv, "import-op")
        self.assertEqual((err.exception.code, err.exception.operation_id), ("duplicate_conflict", "import-op"))
        bad_csv = (
            "external_id,posted_date,amount_minor,description\n"
            "e3,2026-08-03,abc,Bad\n"
        )
        with self.assertRaises(CheckbookError):
            self.book.import_csv("acct", "bank", bad_csv, "op-4")
        self.assertEqual(len(self.book.list_transactions("acct")), 2)
        self.assertEqual(
            [e["event_type"] for e in self.book.list_audit_events()],
            ["account_created", "transaction_imported", "transaction_imported"],
        )

    def test_reconcile_reverse_and_close_period(self):
        self.book.create_account("acct", "USD", 1000, "op-1")
        self.book.record_transaction("acct", "tx-1", "2026-08-01", 500, "Deposit", "op-2")
        self.book.record_transaction("acct", "tx-2", "2026-08-03", -100, "Groceries", "op-3")
        self.book.mark_cleared("tx-1", 1, "op-4")
        self.book.mark_cleared("tx-2", 1, "op-5")
        with self.assertRaises(CheckbookError) as mismatch:
            self.book.reconcile("acct", "2026-08-31", 2000, "reconcile-op")
        self.assertEqual((mismatch.exception.code, mismatch.exception.operation_id), ("reconciliation_mismatch", "reconcile-op"))
        result = self.book.reconcile("acct", "2026-08-31", 1400, "op-6")
        self.assertEqual(result["ending_balance_minor"], 1400)
        self.assertTrue(self.book.get_transaction("tx-1")["reconciled"])
        with self.assertRaises(CheckbookError) as edit_err:
            self.book.edit_transaction("tx-1", 2, "2026-08-01", 600, "Nope", "op-7")
        self.assertEqual(edit_err.exception.code, "reconciled_transaction")
        reversal = self.book.reverse_reconciled_transaction("tx-1", "tx-1-rev", "2026-09-01", "op-8")
        self.assertEqual((reversal["amount_minor"], reversal["reversal_of"]), (-500, "tx-1"))
        with self.assertRaises(CheckbookError) as dup_rev:
            self.book.reverse_reconciled_transaction("tx-1", "tx-1-rev-2", "2026-09-02", "op-9")
        self.assertEqual(dup_rev.exception.code, "reversal_exists")
        closed = self.book.close_period("acct", "2026-08-31", "op-10")
        self.assertEqual(closed["closed_through_date"], "2026-08-31")
        with self.assertRaises(CheckbookError) as closed_err:
            self.book.record_transaction("acct", "tx-3", "2026-08-15", -10, "Blocked", "op-11")
        self.assertEqual(closed_err.exception.code, "closed_period")
        allowed = self.book.record_transaction("acct", "tx-4", "2026-09-02", -10, "Allowed", "op-12")
        self.assertEqual(allowed["transaction_id"], "tx-4")

    def test_reconciliation_uses_prior_reconciled_balance(self):
        self.book.create_account("acct", "USD", 1000, "op-1")
        self.book.record_transaction("acct", "tx-1", "2026-08-01", 100, "A", "op-2")
        self.book.record_transaction("acct", "tx-2", "2026-08-10", 200, "B", "op-3")
        self.book.mark_cleared("tx-1", 1, "op-4")
        self.book.reconcile("acct", "2026-08-05", 1100, "op-5")
        self.book.mark_cleared("tx-2", 1, "op-6")
        second = self.book.reconcile("acct", "2026-08-31", 1300, "op-7")
        self.assertEqual(second["ending_balance_minor"], 1300)


if __name__ == "__main__":
    unittest.main()
