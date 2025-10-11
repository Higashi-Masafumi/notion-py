# Utilities

Helper utilities to simplify common Notion client patterns. Import from `notion_py_client.utils`.

```python
from notion_py_client.utils import (
    iterate_paginated_api,
    collect_paginated_api,
    is_full_page,
    is_full_block,
    is_full_page_or_data_source,
    is_text_rich_text_item_response,
    is_equation_rich_text_item_response,
    is_mention_rich_text_item_response,
    extract_notion_id,
    extract_database_id,
    extract_page_id,
    extract_block_id,
)
```

## Pagination Helpers

- `iterate_paginated_api(list_fn, first_page_args)` — Async iterator over any paginated endpoint.
- `collect_paginated_api(list_fn, first_page_args)` — Gather all results into a list.

Examples:

```python
from notion_py_client import NotionAsyncClient
from notion_py_client.utils import iterate_paginated_api, collect_paginated_api

async with NotionAsyncClient(auth="secret_xxx") as client:
    # 1) Iterate blocks.children.list
    async for child in iterate_paginated_api(
        client.blocks.children.list,
        {"block_id": "parent_block_id", "page_size": 100},
    ):
        print(child["id"])  # dict structure from API

    # 2) Iterate dataSources.query
    async for row in iterate_paginated_api(
        client.dataSources.query,
        {"data_source_id": "ds_abc123", "page_size": 100},
    ):
        print(row.id)  # NotionPage or PartialPage

    # 3) Collect all users
    users = await collect_paginated_api(
        client.users.list,
        {"page_size": 100},
    )
    print(len(users))
```

## Type Predicates (Type Guards)

These helpers are implemented with Python's `TypeGuard` so static type checkers
like `mypy` and `pyright` can narrow types after an `if` check — similar to
TypeScript.

Helpers to quickly check object kinds from mixed results (e.g., search or data source queries):

- `is_full_page(obj)` — True if a full page (has `url`).
- `is_full_block(obj)` — True if a block (has `type`).
- `is_full_page_or_data_source(obj)` — True if page or data source.
- `is_text_rich_text_item_response(item)` — True if rich text `type == "text"`.
- `is_equation_rich_text_item_response(item)` — `type == "equation"`.
- `is_mention_rich_text_item_response(item)` — `type == "mention"`.

Example (static narrowing):

```python
from typing import Union
from notion_py_client.responses.page import NotionPage, PartialPage
from notion_py_client.responses.datasource import DataSource, PartialDataSource

mixed: list[Union[NotionPage, PartialPage, DataSource, PartialDataSource]] = (
    await client.dataSources.query(data_source_id="ds_abc123")
).results

for item in mixed:
    if is_full_page(item):
        # item is NotionPage here (TypeGuard)
        print("Page URL:", item.url)
    elif is_full_page_or_data_source(item):
        # item is NotionPage | DataSource here
        print("ID:", item.id)

# Rich text variants
rt_items = (await client.pages.retrieve({"page_id": page_id})).properties["Description"].rich_text
for rt in rt_items:
    if is_text_rich_text_item_response(rt):
        # rt.text is non-None here
        print(rt.text.content)
```

## Notion ID Utilities

Extract IDs from URLs or raw strings. Returns UUIDs in standard hyphenated format.

- `extract_notion_id(url_or_id)` — Generic extractor.
- `extract_database_id(url)` — Convenience alias.
- `extract_page_id(url)` — Convenience alias.
- `extract_block_id(url_with_fragment)` — Extracts `#block-<id>` or `#<id>`.

Examples:

```python
from notion_py_client.utils import (
    extract_database_id, extract_page_id, extract_block_id
)

# From full URLs
db_id = extract_database_id("https://notion.so/work/DB-abc123def456789012345678901234ab?v=viewid")
page_id = extract_page_id("https://notion.so/work/Some-Page-12345678123412341234123456789abc")
block_id = extract_block_id("https://notion.so/Page-aaaa#block-12345678123412341234123456789abc")

# Use with client
db = await client.databases.retrieve({"database_id": db_id})
page = await client.pages.retrieve({"page_id": page_id})
children = await client.blocks.children.list(block_id=block_id)
```
