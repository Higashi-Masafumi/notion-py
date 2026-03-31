# Change Rubric

Use this rubric to decide whether a Notion changelog item should be patched automatically in `notion-py`.

Current policy: treat the latest official Notion API spec as the source of truth for generated PRs. Do not optimize for backward compatibility unless the user explicitly asks for it.

## Decision buckets

### `auto-fix`

Use `auto-fix` when the work is bounded, local, and matches existing repo patterns.

Typical examples:

- update the repo to the latest official API version and current field names
- rename or remap existing request and response fields
- rename block types that already fit the existing model layout
- add small enum, literal, union, or model fields
- add a thin endpoint façade where the request and response shape are already well understood
- update unit tests and docs that directly cover the changed area

### `report-only`

Use `report-only` when the change is real but too large or underspecified for a safe automatic patch.

Typical examples:

- a new major API group such as Views
- broad schema additions that would touch many files and require product judgment
- release/versioning policy
- follow-up work that depends on user priorities rather than straightforward compatibility

### `no-op`

Use `no-op` when the repo already supports the capability well enough or the changelog item does not apply to this client.

## Fixed policy for this skill

- Implement against the latest official Notion API spec first.
- Prefer replacing legacy fields and behaviors over adding backward compatibility shims.
- Do not bump `project.version` automatically.
- Do not treat docs-only changes as sufficient when code is still missing.
- Do not create a PR when validation fails or GitHub auth is invalid.

## Known Notion API signals

The latest breaking upgrade guide verified for this skill is `2026-03-11`.

Its required current-spec actions are:

- replace `after` with `position`
- replace `archived` with `in_trash`
- replace `transcription` with `meeting_notes`

High-likelihood bounded additions to watch:

- `heading_4`
- `tab`
- `custom_emojis`
- markdown endpoints
- writable verification
- native icon support improvements

High-likelihood report-only additions to watch:

- Views API
