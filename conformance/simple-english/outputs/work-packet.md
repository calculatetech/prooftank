# Work packet

To continue this task, first identify all boundaries. Then use the existing
tests to validate the result. Do not increase the scope.

Keep the packet ID `WP-009`.
Edit `src/ledger/service.py`.
Run `pytest tests/test_ledger.py -q`.

```yaml
must_do:
  - preserve INV-004
must_not_do:
  - add a queue
stop_when:
  - REQ-017 passes
```
