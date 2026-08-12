# Recovery runbook

If the service is unhealthy, investigate all relevant state before you restart
it. A restart can hide information about the cause.

Use runbook ID `RUN-003`.
Read `/srv/ledger/state/current.json`.
If you see `"recovery marker missing"`, stop.

```bash
ledgerctl status --json
systemctl restart ledger-api
ledgerctl verify --operation op_017
```
