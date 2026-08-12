# Upstream qualification manual

## Purpose

Proofmill distributes third-party components into coding-agent environments. These components can read repositories, write configuration, register hooks, run commands, access the network, and influence agent behavior.

Catalog inclusion, popularity, or an MIT label is not sufficient approval.

## Qualification record

Create one file under `upstream/reviews/<component>.md`.

Record:

- Repository and homepage.
- Exact reviewed commit or release.
- License and copyright notices.
- Maintainer and release activity.
- Capability supplied.
- Installation command.
- Files and directories written.
- Agent configuration changed.
- Hooks and commands registered.
- Processes started.
- Network hosts contacted.
- Credentials or tokens used.
- Persistent data stored.
- Privacy controls.
- Update behavior.
- Disable behavior.
- Uninstall behavior.
- Failure modes.
- Known correctness or stability issues.
- Conformance results.
- Fallback.
- Trust class.
- Approval state.

## Required tests

1. Install from a clean environment.
2. Verify files and configuration before and after.
3. Run the advertised health check.
4. Run a basic success case.
5. Run a provider-unavailable case.
6. Run a malformed-input case where relevant.
7. Interrupt an active operation where relevant.
8. Restart the harness.
9. Disable the component.
10. Uninstall the component.
11. Confirm that repository truth remains usable.
12. Confirm that an optional provider failure does not create false success.

## Approval states

- `unreviewed`
- `researching`
- `pilot`
- `approved`
- `approved-optional`
- `blocked`
- `retired`

## Trust classes

### Advisory

The component proposes research, design, prose, or remembered context.

Examples: ADHD, NeuroArxiv, Cavemem.

### Observational

The component reports structure or runtime behavior that can be incomplete.

Example: CBM.

### Deterministic

The component produces reproducible pass/fail output for a defined input and version.

Examples: compiler, test runner, linter, schema validator.

### Authoritative

The artifact has human approval and repository ownership.

Examples: approved specification, accepted waiver, locked provider manifest.

## Sustainability review

At a regular release-maintenance interval:

- Check for new releases and advisories.
- Check license changes.
- Check archive status and maintainer activity.
- Query best-of-Agent-Harnesses for candidate replacements or risk signals.
- Open a review issue.
- Never change a project pin automatically.
