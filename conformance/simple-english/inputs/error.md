# Error guidance

When it comes to the failure scenario, the application should ideally provide
the user with a helpful and robust message that clearly communicates what has
gone wrong and what they might potentially want to do in order to successfully
address the issue without creating additional confusion.

Keep the error code `LEDGER_CONFLICT`.
Keep the field `expectedVersion`.
Keep the log path `/var/log/proofmill/ledger.log`.
Keep the exact error `"ledger version mismatch"`.
Keep the command `ledgerctl show --operation op_017`.
