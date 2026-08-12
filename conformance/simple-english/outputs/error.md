# Error guidance

When a ledger conflict occurs, the application must tell the user what
happened. The message must also tell the user how to correct the error.

Keep the error code `LEDGER_CONFLICT`.
Keep the field `expectedVersion`.
Keep the log path `/var/log/proofmill/ledger.log`.
Keep the exact error `"ledger version mismatch"`.
Keep the command `ledgerctl show --operation op_017`.
