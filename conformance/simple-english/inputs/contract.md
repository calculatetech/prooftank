# Contract review

It is worth noting that this functionality should ultimately facilitate a
robust flow in which the system is capable of dealing with stale ledger writes
in a graceful way, while also making sure that the API behavior is highly clear
for every possible consumer who might potentially call it.

The stable requirement is `REQ-017`.
The invariant is `INV-004`.
The endpoint is `POST /v1/ledger`.
The governing file is `specs/017-ledger/spec.md`.
The exact error is `"ledger version mismatch"`.

```python
if version != expected_version:
    raise ConflictError("ledger version mismatch")
```
