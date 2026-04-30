# notion-py-client

Install using pip:

```bash
pip install notion-py-client
```

## Quick Example

---

## Overview

**notion-py-client** provides a complete type system mirroring Notion's TypeScript API definitions. It offers full coverage of Databases, Data Sources, Pages, Blocks (35 types), Filters, and Request types with strict runtime validation.

## Key Features

- **Type Safety**: Built on Pydantic v2 with strict type validation
- **Complete API Coverage**: Latest Notion API 2026-03-11 compatibility
- **TypeScript Compatibility**: Mirrors official TypeScript type definitions
- **Async First**: Built with `httpx` for async HTTP operations
- **Developer Friendly**: Intuitive API design with comprehensive type hints

## Installation

Install using pip:

```bash
pip install notion-py-client
```

## Quick Example

```python
from notion_py_client import NotionAsyncClient

async with NotionAsyncClient(auth="secret_xxx") as client:
    # Query a data source (2026-03-11 API)
    response = await client.dataSources.query(
        data_source_id="ds_abc123",
        filter={
            "property": "Status",
            "select": {"equals": "Done"}
        }
    )

    for page in response.results:
        print(f"Page: {page.id}")
```

## API Version

This library supports **Notion API version 2026-03-11**, including:

- **Current breaking changes**: `position`, `in_trash`, and `meeting_notes`
- **Markdown page APIs**: create, retrieve, and update page markdown
- **Custom emoji listing**: workspace custom emoji pagination
- **Data source model**: continued support for the 2025-09-03 split

## Next Steps

- [Quick Start Guide](quickstart.md) - Get started with basic usage
- [API Endpoints](api/databases.md) - Detailed endpoint documentation
- [Type Reference](types/index.md) - Complete type system reference
- [Advanced Usage](advanced/mapper.md) - Domain mapping patterns
