#!/usr/bin/env python3
"""Run the external checkbook suite against one arm implementation."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


IMPLEMENTATION = None


def load_implementation(path: Path):
    spec = importlib.util.spec_from_file_location("benchmark_checkbook", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class CheckbookScenarios(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.database = str(Path(self.temp.name) / "ledger.sqlite3")
        self.book = IMPLEMENTATION.Checkbook(self.database)

    def tearDown(self) -> None:
        connection = getattr(self.book, "connection", None)
        if connection is not None:
            connection.close()
        self.temp.cleanup()

    def account(self, opening: int = 10_000) -> dict:
        return self.book.create_account("acct", "USD", opening, "op-account")

    def transaction(
        self,
        transaction_id: str = "tx-1",
        amount: int = -2_500,
        posted_date: str = "2026-01-10",
    ) -> dict:
        return self.book.record_transaction(
            "acct",
            transaction_id,
            posted_date,
            amount,
            "entry",
            f"op-{transaction_id}",
        )

    def assert_error(
        self,
        code: str | None,
        operation_id: str | None,
        function,
        *args,
    ) -> Exception:
        with self.assertRaises(IMPLEMENTATION.CheckbookError) as caught:
            function(*args)
        if code is not None:
            self.assertEqual(code, caught.exception.code)
        self.assertIsInstance(caught.exception.code, str)
        self.assertTrue(caught.exception.code)
        if function in {self.book.import_csv, self.book.reconcile}:
            self.assertEqual(operation_id, caught.exception.operation_id)
        return caught.exception

    def test_req_01_account_currency_and_opening_balance(self) -> None:
        account = self.account(12_345)
        self.assertEqual("acct", account["account_id"])
        self.assertEqual("USD", account["currency"])
        self.assertEqual(12_345, account["opening_balance_minor"])
        self.assert_error(
            None,
            "bad-currency",
            self.book.create_account,
            "bad",
            "usd",
            0,
            "bad-currency",
        )

    def test_req_02_integer_money_and_signs(self) -> None:
        self.account()
        debit = self.transaction("debit", -250)
        credit = self.transaction("credit", 400)
        self.assertEqual(-250, debit["amount_minor"])
        self.assertEqual(400, credit["amount_minor"])
        for invalid in (1.5, True):
            self.assert_error(
                None,
                None,
                self.book.record_transaction,
                "acct",
                f"bad-{invalid}",
                "2026-01-10",
                invalid,
                "bad",
                "bad-money",
            )

    def test_req_03_transaction_shape_and_deterministic_order(self) -> None:
        self.account()
        self.transaction("z-last")
        record = self.transaction("a-first", 500)
        required = {
            "transaction_id",
            "account_id",
            "posted_date",
            "amount_minor",
            "description",
            "version",
            "cleared",
            "reconciled",
            "reversal_of",
            "source",
            "external_id",
        }
        self.assertTrue(required <= record.keys())
        self.assertEqual(1, record["version"])
        self.assertFalse(record["cleared"])
        self.assertFalse(record["reconciled"])
        self.assertEqual(
            ["a-first", "z-last"],
            [item["transaction_id"] for item in self.book.list_transactions("acct")],
        )

    def test_req_04_edit_clear_and_expected_version(self) -> None:
        self.account()
        self.transaction()
        edited = self.book.edit_transaction(
            "tx-1", 1, "2026-01-11", -2_600, "edited", "op-edit"
        )
        self.assertEqual(2, edited["version"])
        self.assertEqual(-2_600, edited["amount_minor"])
        self.assert_error(
            None,
            "op-stale",
            self.book.mark_cleared,
            "tx-1",
            1,
            "op-stale",
        )
        cleared = self.book.mark_cleared("tx-1", 2, "op-clear")
        self.assertTrue(cleared["cleared"])
        self.assertEqual(3, cleared["version"])

    def test_req_05_import_success_and_idempotent_duplicate(self) -> None:
        self.account()
        statement = (
            "external_id,posted_date,amount_minor,description\n"
            "bank-1,2026-01-12,-100,Lunch\n"
            "bank-2,2026-01-13,500,Deposit\n"
        )
        first = self.book.import_csv("acct", "bank", statement, "op-import-1")
        second = self.book.import_csv("acct", "bank", statement, "op-import-2")
        self.assertEqual({"inserted": 2, "duplicates": 0}, first)
        self.assertEqual({"inserted": 0, "duplicates": 2}, second)
        self.assertEqual(2, len(self.book.list_transactions("acct")))
        ids = [item["transaction_id"] for item in self.book.list_transactions("acct")]
        self.assertEqual(ids, sorted(ids))

    def test_req_06_conflicting_duplicate_is_atomic(self) -> None:
        self.account()
        original = (
            "external_id,posted_date,amount_minor,description\n"
            "same,2026-01-10,-100,Original\n"
        )
        self.book.import_csv("acct", "bank", original, "op-original")
        before_events = len(self.book.list_audit_events())
        conflict = (
            "external_id,posted_date,amount_minor,description\n"
            "new,2026-01-11,50,New row\n"
            "same,2026-01-10,-101,Conflict\n"
        )
        self.assert_error(
            "duplicate_conflict",
            "op-conflict",
            self.book.import_csv,
            "acct",
            "bank",
            conflict,
            "op-conflict",
        )
        rows = self.book.list_transactions("acct")
        self.assertEqual(["same"], [row["external_id"] for row in rows])
        self.assertEqual(before_events, len(self.book.list_audit_events()))

    def test_req_07_malformed_middle_row_and_retry(self) -> None:
        self.account()
        malformed = (
            "external_id,posted_date,amount_minor,description\n"
            "one,2026-01-10,-100,Good\n"
            "two,not-a-date,-200,Bad\n"
            "three,2026-01-12,-300,Good\n"
        )
        self.assert_error(
            None,
            "op-bad-import",
            self.book.import_csv,
            "acct",
            "bank",
            malformed,
            "op-bad-import",
        )
        self.assertEqual([], self.book.list_transactions("acct"))
        retry = (
            "external_id,posted_date,amount_minor,description\n"
            "one,2026-01-10,-100,Good\n"
            "three,2026-01-12,-300,Good\n"
        )
        self.assertEqual(
            {"inserted": 2, "duplicates": 0},
            self.book.import_csv("acct", "bank", retry, "op-retry"),
        )

    def test_req_08_reconcile_and_mismatch_are_atomic(self) -> None:
        self.account()
        self.transaction()
        self.book.mark_cleared("tx-1", 1, "op-clear")
        before_events = len(self.book.list_audit_events())
        self.assert_error(
            "reconciliation_mismatch",
            "op-mismatch",
            self.book.reconcile,
            "acct",
            "2026-01-31",
            7_499,
            "op-mismatch",
        )
        self.assertFalse(self.book.get_transaction("tx-1")["reconciled"])
        self.assertEqual(before_events, len(self.book.list_audit_events()))
        result = self.book.reconcile("acct", "2026-01-31", 7_500, "op-reconcile")
        self.assertEqual("acct", result["account_id"])
        self.assertEqual("2026-01-31", result["statement_date"])
        self.assertTrue(self.book.get_transaction("tx-1")["reconciled"])

    def test_req_09_reconciled_history_uses_one_linked_reversal(self) -> None:
        self.account()
        self.transaction()
        self.book.mark_cleared("tx-1", 1, "op-clear")
        self.book.reconcile("acct", "2026-01-31", 7_500, "op-reconcile")
        self.assert_error(
            None,
            "op-edit-old",
            self.book.edit_transaction,
            "tx-1",
            3,
            "2026-02-01",
            -2_400,
            "mutate",
            "op-edit-old",
        )
        reversal = self.book.reverse_reconciled_transaction(
            "tx-1", "reverse-1", "2026-02-01", "op-reverse"
        )
        self.assertEqual(2_500, reversal["amount_minor"])
        self.assertEqual("tx-1", reversal["reversal_of"])
        self.assert_error(
            None,
            "op-reverse-twice",
            self.book.reverse_reconciled_transaction,
            "tx-1",
            "reverse-2",
            "2026-02-02",
            "op-reverse-twice",
        )

    def test_req_10_closed_period_prevents_historical_mutation(self) -> None:
        self.account()
        self.transaction()
        self.book.close_period("acct", "2026-01-31", "op-close")
        self.assert_error(
            None,
            "op-old-new",
            self.book.record_transaction,
            "acct",
            "old-new",
            "2026-01-31",
            1,
            "old",
            "op-old-new",
        )
        self.assert_error(
            None,
            "op-old-edit",
            self.book.edit_transaction,
            "tx-1",
            1,
            "2026-02-01",
            -2_400,
            "move history",
            "op-old-edit",
        )
        self.assert_error(
            None,
            "op-close-back",
            self.book.close_period,
            "acct",
            "2026-01-30",
            "op-close-back",
        )

    def test_req_11_two_connections_detect_lost_edit(self) -> None:
        self.account()
        self.transaction()
        other = IMPLEMENTATION.Checkbook(self.database)
        first = self.book.edit_transaction(
            "tx-1", 1, "2026-01-10", -2_400, "first", "op-first"
        )
        self.assertEqual(2, first["version"])
        self.assert_error(
            None,
            "op-second",
            other.edit_transaction,
            "tx-1",
            1,
            "2026-01-10",
            -2_300,
            "second",
            "op-second",
        )
        connection = getattr(other, "connection", None)
        if connection is not None:
            connection.close()

    def test_req_12_every_successful_command_is_audited(self) -> None:
        self.account()
        self.transaction()
        self.book.edit_transaction("tx-1", 1, "2026-01-10", -2_400, "edit", "op-edit")
        self.book.mark_cleared("tx-1", 2, "op-clear")
        self.book.reconcile("acct", "2026-01-31", 7_600, "op-reconcile")
        self.book.reverse_reconciled_transaction(
            "tx-1", "reverse", "2026-02-01", "op-reverse"
        )
        self.book.close_period("acct", "2026-01-31", "op-close")
        events = self.book.list_audit_events()
        required = {"event_id", "operation_id", "event_type", "account_id"}
        self.assertTrue(all(required <= event.keys() for event in events))
        self.assertEqual(
            [
                "op-account",
                "op-tx-1",
                "op-edit",
                "op-clear",
                "op-reconcile",
                "op-reverse",
                "op-close",
            ],
            [event["operation_id"] for event in events],
        )
        self.assertEqual(
            sorted(event["event_id"] for event in events),
            [event["event_id"] for event in events],
        )

    def test_req_13_state_survives_restart_after_abort(self) -> None:
        self.account()
        self.transaction()
        bad = (
            "external_id,posted_date,amount_minor,description\n"
            "one,2026-02-01,not-an-int,Bad\n"
        )
        self.assert_error(
            None,
            "op-abort",
            self.book.import_csv,
            "acct",
            "bank",
            bad,
            "op-abort",
        )
        restarted = IMPLEMENTATION.Checkbook(self.database)
        self.assertEqual(
            ["tx-1"],
            [row["transaction_id"] for row in restarted.list_transactions("acct")],
        )
        self.assertEqual(
            ["op-account", "op-tx-1"],
            [event["operation_id"] for event in restarted.list_audit_events()],
        )
        connection = getattr(restarted, "connection", None)
        if connection is not None:
            connection.close()

    def test_req_14_real_calendar_dates(self) -> None:
        self.account()
        leap = self.transaction("leap", 1, "2028-02-29")
        self.assertEqual("2028-02-29", leap["posted_date"])
        self.assert_error(
            None,
            None,
            self.book.record_transaction,
            "acct",
            "bad-date",
            "2027-02-29",
            1,
            "bad",
            "op-date",
        )

    def test_req_15_failure_operation_ids_are_structured(self) -> None:
        self.account()
        bad_csv = "external_id,posted_date,amount_minor,description\nx,bad,1,X\n"
        error = self.assert_error(
            None,
            "import-operation",
            self.book.import_csv,
            "acct",
            "bank",
            bad_csv,
            "import-operation",
        )
        self.assertNotEqual("", str(error))
        error = self.assert_error(
            "reconciliation_mismatch",
            "reconcile-operation",
            self.book.reconcile,
            "acct",
            "2026-01-31",
            999,
            "reconcile-operation",
        )
        self.assertNotEqual("", str(error))


class RecordingResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.passed = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.passed.append(test.id())


def run(path: Path) -> dict:
    global IMPLEMENTATION
    IMPLEMENTATION = load_implementation(path)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CheckbookScenarios)
    runner = unittest.TextTestRunner(
        stream=sys.stderr, verbosity=1, resultclass=RecordingResult
    )
    result = runner.run(suite)
    failures = [
        {"test": test.id(), "detail": detail}
        for test, detail in result.failures + result.errors
    ]
    return {
        "schema_version": "1.0",
        "implementation": str(path.resolve()),
        "tests": result.testsRun,
        "passed": len(result.passed),
        "failed": len(failures),
        "successful": result.wasSuccessful(),
        "passed_tests": sorted(result.passed),
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("implementation", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        summary = run(args.implementation)
    except Exception as error:  # The target can fail during import.
        summary = {
            "schema_version": "1.0",
            "implementation": str(args.implementation.resolve()),
            "tests": 0,
            "passed": 0,
            "failed": 1,
            "successful": False,
            "passed_tests": [],
            "failures": [{"test": "implementation_import", "detail": repr(error)}],
        }
    encoded = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded)
    else:
        print(encoded, end="")
    return 0 if summary["successful"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
