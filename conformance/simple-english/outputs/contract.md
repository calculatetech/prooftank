# Contract review

The system must handle stale ledger writes consistently. The API behavior must
be clear to all consumers.

The stable requirement is `REQ-017`.
The invariant is `INV-004`.
The endpoint is `POST /v1/ledger`.
The governing file is `specs/017-ledger/spec.md`.
The exact error is `"ledger version mismatch"`.

```python
if version != expected_version:
    raise ConflictError("ledger version mismatch")
```
