# Work packet

In order to comprehensively move forward with this task, the implementer should
first make sure that all of the various boundaries are taken into account and
then proceed to leverage the existing tests so that the end result can be
validated in a robust fashion without accidentally growing the scope.

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
