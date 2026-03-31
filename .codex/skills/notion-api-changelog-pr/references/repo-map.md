# Repo Map

Use this map to inspect the likely edit points in `notion-py` without re-discovering the repo structure.

## Core client

- `notion_py_client/notion_client.py`
  - default API version
  - endpoint façade classes
  - request body wiring for pages, blocks, data sources, databases, comments, files

## Parameter and request models

- `notion_py_client/api_types.py`
  - `TypedDict` request parameters and query helpers
- `notion_py_client/requests/common.py`
  - shared request fragments such as icon and file payloads
- `notion_py_client/requests/page_requests.py`
  - page update request fields like `archived` and `in_trash`
- `notion_py_client/requests/property_requests.py`
  - writable page property request types, including verification if added

## Response and model layers

- `notion_py_client/responses/`
  - page, database, datasource, list, property item, file upload models
- `notion_py_client/models/icon.py`
  - icon response support
- `notion_py_client/models/primitives/`
  - custom emoji and rich text primitives

## Block support

- `notion_py_client/blocks/base.py`
  - block type literal list
- `notion_py_client/blocks/__init__.py`
  - discriminated union of all supported block models
- `notion_py_client/blocks/text_blocks.py`
  - headings and text-family block models
- `notion_py_client/blocks/layout_blocks.py`
  - candidate location for `tab` support if it is modeled as a layout block
- `notion_py_client/blocks/special_blocks.py`
  - candidate location for renamed or specialized block payloads

## Documentation

- `README.md`
  - top-level supported API version claims
- `docs/quickstart.md`
  - version and migration guidance
- `docs/api/`
  - endpoint examples
- `docs/types/`
  - request and response shape examples

## Tests

- `test/unit/`
  - request-model, filter, mapper, and response parsing coverage
- `test/integration/test_client.py`
  - integration coverage for endpoint façades when credentials are available

## CI and publish context

- `.github/workflows/test.yml`
  - unit test command used in CI
- `.github/workflows/release-drafter.yml`
  - release handling, which should remain out of scope for automatic changelog patches
