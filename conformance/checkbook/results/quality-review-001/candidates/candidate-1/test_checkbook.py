import os
import tempfile
import unittest

from checkbook import Checkbook, CheckbookError


class CheckbookTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tmp.name, "checkbook.sqlite3")
        self.book = Checkbook(self.db_path)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_account_validation_audit_and_persistence(self) -> None:
        with self.assertRaises(CheckbookError) as ctx:
            self.book.create_account("acct", "usd", 100, "op-1")
        self.assertEqual(ctx.exception.code, "invalid_currency")
        self.assertEqual(ctx.exception.operation_id, "op-1")

        with self.assertRaises(CheckbookError) as ctx:
            self.book.create_account("acct", "USD", True, "op-2")
        self.assertEqual(ctx.exception.code, "invalid_opening_balance_minor")
        self.assertEqual(ctx.exception.operation_id, "op-2")

        account = self.book.create_account("acct", "USD", 1250, "op-3")
        self.assertEqual(
            account,
            {
                "account_id": "acct",
                "currency": "USD",
                "opening_balance_minor": 1250,
                "closed_through_date": None,
            },
        )
        self.assertEqual(
            self.book.list_audit_events(),
            [
                {
                    "event_id": 1,
                    "operation_id": "op-3",
                    "event_type": "account_created",
                    "account_id": "acct",
                }
            ],
        )

        reopened = Checkbook(self.db_path)
        self.assertEqual(reopened.get_account("acct"), account)
        self.assertEqual(reopened.list_audit_events()[0]["event_id"], 1)

    def test_transaction_lifecycle_and_close_guards(self) -> None:
        self.book.create_account("acct", "USD", 0, "op-a1")

        tx = self.book.record_transaction("acct", "txn-1", "2026-01-10", 500, "Deposit", "op-a2")
        self.assertEqual(tx["version"], 1)
        self.assertFalse(tx["cleared"])
        self.assertFalse(tx["reconciled"])
        self.assertIsNone(tx["reversal_of"])
        self.assertIsNone(tx["source"])
        self.assertIsNone(tx["external_id"])

        with self.assertRaises(CheckbookError) as ctx:
            self.book.edit_transaction("txn-1", 9, "2026-01-10", 600, "Deposit+", "op-a3")
        self.assertEqual(ctx.exception.code, "stale_version")

        tx = self.book.edit_transaction("txn-1", 1, "2026-01-11", 600, "Deposit+", "op-a4")
        self.assertEqual(tx["version"], 2)
        self.assertEqual(tx["posted_date"], "2026-01-11")
        self.assertEqual(tx["amount_minor"], 600)

        tx = self.book.mark_cleared("txn-1", 2, "op-a5")
        self.assertTrue(tx["cleared"])
        self.assertEqual(tx["version"], 3)

        closed = self.book.close_period("acct", "2026-01-31", "op-a6")
        self.assertEqual(closed["closed_through_date"], "2026-01-31")

        with self.assertRaises(CheckbookError) as ctx:
            self.book.record_transaction("acct", "txn-2", "2026-01-15", -100, "Old debit", "op-a7")
        self.assertEqual(ctx.exception.code, "period_closed")

        with self.assertRaises(CheckbookError) as ctx:
            self.book.edit_transaction("txn-1", 3, "2026-02-01", 700, "Blocked", "op-a8")
        self.assertEqual(ctx.exception.code, "period_closed")

        with self.assertRaises(CheckbookError) as ctx:
            self.book.mark_cleared("txn-1", 3, "op-a9")
        self.assertEqual(ctx.exception.code, "period_closed")

        with self.assertRaises(CheckbookError) as ctx:
            self.book.close_period("acct", "2026-01-01", "op-a10")
        self.assertEqual(ctx.exception.code, "period_close_backwards")

    def test_import_csv_is_atomic_and_deduplicates(self) -> None:
        self.book.create_account("acct", "USD", 0, "op-b1")
        csv_text = (
            "external_id,posted_date,amount_minor,description\n"
            "e-2,2026-02-03,-75,Coffee\n"
            "e-1,2026-02-01,100,Paycheck\n"
            "e-1,2026-02-01,100,Paycheck\n"
        )
        result = self.book.import_csv("acct", "bank-a", csv_text, "op-b2")
        self.assertEqual(result, {"inserted": 2, "duplicates": 1})

        transactions = self.book.list_transactions("acct")
        self.assertEqual([tx["external_id"] for tx in transactions], ["e-1", "e-2"])
        imported_ids = [tx["transaction_id"] for tx in transactions]
        self.assertEqual(len(set(imported_ids)), 2)

        retry = self.book.import_csv("acct", "bank-a", csv_text, "op-b3")
        self.assertEqual(retry, {"inserted": 0, "duplicates": 3})
        self.assertEqual([tx["transaction_id"] for tx in self.book.list_transactions("acct")], imported_ids)

        conflict_csv = (
            "external_id,posted_date,amount_minor,description\n"
            "e-1,2026-02-01,999,Changed\n"
        )
        with self.assertRaises(CheckbookError) as ctx:
            self.book.import_csv("acct", "bank-a", conflict_csv, "op-b4")
        self.assertEqual(ctx.exception.code, "duplicate_conflict")
        self.assertEqual(ctx.exception.operation_id, "op-b4")

        bad_csv = (
            "external_id,posted_date,amount_minor,description\n"
            "e-3,not-a-date,10,Bad row\n"
        )
        before_events = len(self.book.list_audit_events())
        with self.assertRaises(CheckbookError) as ctx:
            self.book.import_csv("acct", "bank-a", bad_csv, "op-b5")
        self.assertEqual(ctx.exception.code, "invalid_date")
        self.assertEqual(len(self.book.list_transactions("acct")), 2)
        self.assertEqual(len(self.book.list_audit_events()), before_events)

    def test_reconcile_reverse_and_reopen(self) -> None:
        self.book.create_account("acct", "USD", 1000, "op-c1")
        self.book.record_transaction("acct", "txn-1", "2026-03-01", 200, "Deposit", "op-c2")
        self.book.record_transaction("acct", "txn-2", "2026-03-02", -50, "Snacks", "op-c3")
        self.book.mark_cleared("txn-1", 1, "op-c4")
        self.book.mark_cleared("txn-2", 1, "op-c5")

        with self.assertRaises(CheckbookError) as ctx:
            self.book.reconcile("acct", "2026-03-31", 1200, "op-c6")
        self.assertEqual(ctx.exception.code, "reconciliation_mismatch")
        self.assertEqual(ctx.exception.operation_id, "op-c6")
        self.assertFalse(self.book.get_transaction("txn-1")["reconciled"])

        summary = self.book.reconcile("acct", "2026-03-31", 1150, "op-c7")
        self.assertEqual(
            summary,
            {
                "account_id": "acct",
                "statement_date": "2026-03-31",
                "ending_balance_minor": 1150,
            },
        )
        self.assertTrue(self.book.get_transaction("txn-1")["reconciled"])
        self.assertTrue(self.book.get_transaction("txn-2")["reconciled"])

        with self.assertRaises(CheckbookError) as ctx:
            self.book.edit_transaction("txn-1", 2, "2026-03-05", 300, "Blocked", "op-c8")
        self.assertEqual(ctx.exception.code, "transaction_reconciled")

        reversal = self.book.reverse_reconciled_transaction("txn-1", "txn-1-r", "2026-04-01", "op-c9")
        self.assertEqual(reversal["amount_minor"], -200)
        self.assertEqual(reversal["reversal_of"], "txn-1")
        self.assertFalse(reversal["reconciled"])

        with self.assertRaises(CheckbookError) as ctx:
            self.book.reverse_reconciled_transaction("txn-1", "txn-1-r2", "2026-04-02", "op-c10")
        self.assertEqual(ctx.exception.code, "duplicate_reversal")

        self.book.mark_cleared("txn-1-r", 1, "op-c11")
        self.book.reconcile("acct", "2026-04-30", 950, "op-c12")
        with self.assertRaises(CheckbookError) as ctx:
            self.book.reverse_reconciled_transaction("txn-1-r", "txn-1-rr", "2026-05-01", "op-c13")
        self.assertEqual(ctx.exception.code, "invalid_reversal")

        reopened = Checkbook(self.db_path)
        self.assertEqual(reopened.get_transaction("txn-1-r")["reversal_of"], "txn-1")
        self.assertEqual(
            [event["event_type"] for event in reopened.list_audit_events()],
            [
                "account_created",
                "transaction_recorded",
                "transaction_recorded",
                "transaction_cleared",
                "transaction_cleared",
                "reconciled",
                "transaction_reversed",
                "transaction_cleared",
                "reconciled",
            ],
        )

    def test_reconcile_is_safe_when_statements_run_out_of_order(self) -> None:
        self.book.create_account("acct", "USD", 1000, "op-d1")
        self.book.record_transaction("acct", "txn-1", "2026-03-01", 200, "March deposit", "op-d2")
        self.book.record_transaction("acct", "txn-2", "2026-04-01", 50, "April deposit", "op-d3")
        self.book.mark_cleared("txn-1", 1, "op-d4")
        self.book.mark_cleared("txn-2", 1, "op-d5")

        self.book.reconcile("acct", "2026-04-30", 1250, "op-d6")
        summary = self.book.reconcile("acct", "2026-03-31", 1200, "op-d7")
        self.assertEqual(
            summary,
            {
                "account_id": "acct",
                "statement_date": "2026-03-31",
                "ending_balance_minor": 1200,
            },
        )


if __name__ == "__main__":
    unittest.main()
