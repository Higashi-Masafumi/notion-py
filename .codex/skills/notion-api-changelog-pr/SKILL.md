---
name: notion-api-changelog-pr
description: Check the Notion API changelog and upgrade guides for the notion-py repository, decide whether bounded library updates are needed, implement patches against the latest official Notion API spec, run repo validation, and prepare a draft PR when the scope is clean and GitHub auth is valid. Use when asked to review Notion API updates, compare notion-py against the latest Notion API, align notion-py with current Notion API behavior, patch breaking or thin additive gaps, or open a PR for required notion-py updates. 「Notion API の changelog を確認して notion-py の更新要否を見たい」「Notion API 更新に合わせて notion-py の差分を埋めて PR を作りたい」ときに使う。
---

# Notion API Changelog PR

## Overview

Use this skill only for `/Users/higa4/dev/notion-py` or an equivalent checkout of the same repository.

Track the latest official Notion API changes, classify the impact on `notion-py`, implement only bounded fixes against the current official spec, validate the repo, and publish a draft PR only when the scope and GitHub state are safe.

## Workflow

### 1. Confirm the target repo

- Work only when the current repo is `notion-py`.
- Stop if the checkout is a different project or if the worktree contains unrelated changes.
- Before any publish step, run `git status --short`, `git branch --show-current`, `git remote -v`, and `gh auth status`.

### 2. Read official upstream sources only

- Start with the Notion changelog and the relevant upgrade guide for the latest breaking version.
- Read linked API docs only for the specific capability being patched.
- If SDK behavior matters, use the official JS/TS SDK release notes or source as the compatibility reference.
- Do not use blog posts, community posts, or secondary summaries as the source of truth.
- Treat the latest official Notion API spec as the correct behavior target for the PR.
- Do not preserve old request or response shapes unless the user explicitly asks for backward compatibility.

Current high-signal upstream baseline:

- `2026-03-11` is a breaking API version.
- The upgrade guide says to replace `after` with `position`, `archived` with `in_trash`, and `transcription` with `meeting_notes`.
- The upgrade guide says `@notionhq/client` `v5.12.0` or later supports opt-in use of `2026-03-11`.

### 3. Scan the repo before deciding what to patch

- Read [references/change-rubric.md](./references/change-rubric.md) to keep the classification consistent.
- Run `python3 scripts/repo_gap_scan.py --repo-root .. --format markdown`.
- Use [references/repo-map.md](./references/repo-map.md) to jump straight to likely edit points.
- Treat the scanner output as the initial worklist, then confirm each candidate in code before editing.

### 4. Classify every upstream change

Classify each item into exactly one bucket:

- `auto-fix`: bounded work that fits existing repo patterns and aligns the library to the current official Notion API.
- `report-only`: too large or too open-ended for a safe automatic patch.
- `no-op`: already supported or not relevant to the repo.

Bounded auto-fix scope:

- update the client to the latest breaking API version and make that version the repo's source of truth
- replace `after` with `position`
- replace request-side or response-side `archived` handling with `in_trash`
- replace `transcription` with `meeting_notes`
- add small enum, literal, union, request, response, or thin endpoint-facade support
- update docs and unit tests that directly cover the changed surface

Report-only scope:

- large new API groups such as Views when the repo has no existing equivalent façade
- schema-heavy additions that would require broad modeling beyond a bounded patch
- release management, package version bumps, or semver decisions

Never bump the package version automatically as part of this workflow.

### 5. Patch only bounded fixes

- Follow existing repo conventions before introducing any new abstraction.
- Prefer the same public shape the repo already uses: `TypedDict` for API parameter dictionaries, Pydantic models for structured requests and responses, thin API façade methods in `notion_client.py`, and corresponding docs under `docs/`.
- Implement against the latest official spec first, not against backward compatibility shims.
- Prefer replacing legacy fields and behavior over supporting both old and new paths in parallel.
- Update only the minimal set of docs and tests needed to keep examples and current-spec behavior honest.

### 6. Validate before publish

Run the smallest meaningful set of checks first, then widen only if needed:

- `uv run pytest test/unit -v`
- a focused dry run of the scanner:
  `python3 scripts/repo_gap_scan.py --repo-root .. --format markdown`

Expect the scanner to flag these kinds of items when still missing:

- `2026-03-11` compatibility changes as `auto-fix`
- `views` support as `report-only`

### 7. Publish only when the repo is safe

Do not publish when any of these are false:

- the worktree scope is clean
- the intended patch has passing validation
- `gh auth status` succeeds
- the remote is GitHub

When publish is allowed:

- delegate branch, commit, push, and draft PR creation to the GitHub `yeet` skill
- keep the PR as draft by default
- summarize `auto-fix`, `report-only`, and any deferred follow-up in the PR body

When publish is blocked:

- stop cleanly
- report the exact blocker
- if `gh auth status` is invalid, instruct the user to re-authenticate before retrying PR creation

## Resources

### `scripts/repo_gap_scan.py`

Scan `notion-py` for the highest-signal Notion API compatibility anchors and classify each one as `auto-fix`, `report-only`, or `no-op`.

Use it to detect:

- `2026-03-11` version support
- `after` vs `position`
- `archived` vs `in_trash`
- `transcription` vs `meeting_notes`
- `heading_4`
- `tab`
- `custom_emojis`
- Views API support
- markdown endpoint support
- writable verification support
- native icon request/response support

### `references/change-rubric.md`

Read this first when deciding whether a changelog item stays inside bounded scope.

### `references/repo-map.md`

Use this as the fast path to the files most likely to require edits.

## Output expectations

- Start with a short impact summary grounded in the official changelog.
- List the worklist grouped by `auto-fix`, `report-only`, and `no-op`.
- If patches were made, report the validation commands you ran and whether they passed.
- If a PR was not created, explain why in one sentence and stop instead of improvising around the blocker.
