# notion-py-client

Install using pip:

```bash
pip install notion-py-client
```

## Quick Examplehon client library for the Notion API, built with Pydantic v2.

---

## Overview

**notion-py-client** provides a complete type system mirroring Notion's TypeScript API definitions. It offers full coverage of Databases, Data Sources, Pages, Blocks (33 types), Filters, and Request types with strict runtime validation.

## Key Features

- **Type Safety**: Built on Pydantic v2 with strict type validation
- **Complete API Coverage**: All Notion API 2025-09-03 endpoints supported
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
    # Query a data source (2025-09-03 API)
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

This library supports **Notion API version 2025-09-03**, which introduces:

- **Databases**: Containers holding multiple data sources
- **Data Sources**: Entities containing actual data and schema (equivalent to old databases)
- Enhanced file upload capabilities
- Improved type safety

## Next Steps

- [Quick Start Guide](quickstart.md) - Get started with basic usage
- [API Endpoints](api/databases.md) - Detailed endpoint documentation
- [Type Reference](types/index.md) - Complete type system reference
- [Advanced Usage](advanced/mapper.md) - Domain mapping patterns
