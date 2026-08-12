# Frozen product brief: Checkbook

Build a small local checkbook ledger. Implement the complete public contract in
one repository.

## Fixed stack

Use Python 3.12 or newer and only the Python standard library. Store durable
state in SQLite. Put the public implementation in `checkbook.py` at the
repository root. Tests can use `unittest`.

Do not add a network service, background process, framework, external package,
plugin system, or user interface. The application must remain inspectable and
run locally.

## Value rules

- Money is an integer number of minor units. Reject `float` and `bool` values.
- A positive transaction amount is a credit. A negative amount is a debit.
- Currency is one uppercase three-letter code per account.
- A date is a real ISO `YYYY-MM-DD` calendar date.
- An identifier is a non-empty string.
- Every state-changing method requires a non-empty `operation_id`.
- Every returned record is a plain `dict` with stable string keys.
- Results from list methods have deterministic order.

## Public module

`checkbook.py` must export:

```python
class CheckbookError(Exception):
    code: str
    operation_id: str | None

class Checkbook:
    def __init__(self, database_path: str): ...

    def create_account(
        self, account_id: str, currency: str,
        opening_balance_minor: int, operation_id: str,
    ) -> dict: ...

    def record_transaction(
        self, account_id: str, transaction_id: str, posted_date: str,
        amount_minor: int, description: str, operation_id: str,
    ) -> dict: ...

    def edit_transaction(
        self, transaction_id: str, expected_version: int,
        posted_date: str, amount_minor: int, description: str,
        operation_id: str,
    ) -> dict: ...

    def mark_cleared(
        self, transaction_id: str, expected_version: int,
        operation_id: str,
    ) -> dict: ...

    def import_csv(
        self, account_id: str, source: str, csv_text: str,
        operation_id: str,
    ) -> dict: ...

    def reconcile(
        self, account_id: str, statement_date: str,
        ending_balance_minor: int, operation_id: str,
    ) -> dict: ...

    def reverse_reconciled_transaction(
        self, original_transaction_id: str, reversal_transaction_id: str,
        posted_date: str, operation_id: str,
    ) -> dict: ...

    def close_period(
        self, account_id: str, through_date: str, operation_id: str,
    ) -> dict: ...

    def get_account(self, account_id: str) -> dict: ...
    def get_transaction(self, transaction_id: str) -> dict: ...
    def list_transactions(self, account_id: str) -> list[dict]: ...
    def list_audit_events(self) -> list[dict]: ...
```

`CheckbookError` must set `code` and `operation_id` as public attributes. Every
import or reconciliation error must carry the exact supplied `operation_id`.
Use stable machine-readable error codes. Do not require callers to parse the
message.

## Account and transaction behavior

An account has one currency, an opening balance, and an optional closed-through
date. Account creation is audited.

A new transaction starts at version `1`. It is uncleared, unreconciled, and has
no reversal link. Editing or clearing increments its version. Reject an edit
when the supplied version is stale. Reject edits to reconciled transactions and
transactions on or before the account's closed-through date.

`get_transaction` and `list_transactions` must expose at least:
`transaction_id`, `account_id`, `posted_date`, `amount_minor`, `description`,
`version`, `cleared`, `reconciled`, `reversal_of`, `source`, and `external_id`.

## CSV import

`csv_text` has this exact header:

```text
external_id,posted_date,amount_minor,description
```

The pair `(source, external_id)` identifies an imported transaction within an
account. The implementation chooses the internal transaction identifier, but it
must be stable across retries.

An identical existing identity is an idempotent duplicate. Count it in
`duplicates` and do not insert or audit another transaction. If the date,
amount, or description differs, raise `CheckbookError` with code
`duplicate_conflict`.

Validate the complete CSV before publishing any row. A malformed row, duplicate
conflict, closed-period row, or storage failure leaves no imported row or audit
event from that call. Return `{"inserted": int, "duplicates": int}`.

## Reconciliation, reversal, and close

Reconciliation considers cleared, unreconciled transactions on or before the
statement date. Add their amounts to the opening balance and all previously
reconciled transaction amounts. The result must equal `ending_balance_minor`.
If it does not, raise `CheckbookError` with code `reconciliation_mismatch` and
change nothing.

On success, mark the considered transactions reconciled and return a record
that includes `account_id`, `statement_date`, and `ending_balance_minor`.
Reconciliation is audited.

Do not edit or delete reconciled history. A reconciled transaction can be
reversed once. The reversal is a new linked transaction with the opposite
amount, the same account, and `reversal_of` set to the original identifier.
Reject a duplicate reversal. Audit the reversal.

Closing a period sets the account's closed-through date. Reject new, imported,
edited, cleared, reversed, or reconciled transaction effects on or before that
date. A later close can move the date forward but never backward. Audit the
close.

## Audit behavior

Every successful state-changing method writes at least one audit event in the
same SQLite transaction as its state change. Each event must expose at least
`event_id`, `operation_id`, `event_type`, and `account_id`.

Event identifiers and list order must be deterministic. A failed operation must
not leave a success audit event. Reopening `Checkbook` with the same database
path must preserve all committed state and events.

## Required delivery

- Implement all public behavior in `checkbook.py`.
- Add focused repository tests.
- Run the repository tests and Python compilation checks.
- Keep the source small and direct.
- Do not implement behavior outside this brief.
