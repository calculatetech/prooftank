# Recovery runbook

In the event that the service has been observed to be unhealthy, the operator
should carefully and comprehensively investigate the relevant state before
proceeding to restart it, since doing so may potentially make it harder to
understand what happened under the hood.

Use runbook ID `RUN-003`.
Read `/srv/ledger/state/current.json`.
If you see `"recovery marker missing"`, stop.

```bash
ledgerctl status --json
systemctl restart ledger-api
ledgerctl verify --operation op_017
```
