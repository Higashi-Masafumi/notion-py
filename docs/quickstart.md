# Quick Start

This guide will help you get started with notion-py-client.

## Installation

Install the package:

```bash
pip install notion-py-client
```

## Authentication

Get your Notion integration token from [Notion Integrations](https://www.notion.so/my-integrations).

```python
from notion_py_client import NotionAsyncClient

# Initialize the client
client = NotionAsyncClient(auth="secret_xxx")

# Or with options
client = NotionAsyncClient(
    auth="secret_xxx",
    options={
        "timeout_ms": 30000,
        "notion_version": "2025-09-03"
    }
)
```

## Basic Usage

### Query a Data Source

In Notion API 2025-09-03, databases are containers for data sources. To query data:

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    # Query a data source
    response = await client.dataSources.query(
        data_source_id="ds_abc123",
        page_size=50
    )

    for page in response.results:
        print(f"Page ID: {page.id}")
```

### Create a Page

```python
from notion_py_client.requests.page_requests import CreatePageParameters
from notion_py_client.requests.property_requests import (
    TitlePropertyRequest,
    StatusPropertyRequest,
)

async with NotionAsyncClient(auth="secret_xxx") as client:
    params = CreatePageParameters(
        parent={"type": "database_id", "database_id": "db_abc123"},
        properties={
            "Name": TitlePropertyRequest(
                title=[{"type": "text", "text": {"content": "New Page"}}]
            ),
            "Status": StatusPropertyRequest(
                status={"name": "In Progress"}
            ),
        }
    )

    page = await client.pages.create(params)
    print(f"Created page: {page.id}")
```

### Update a Page

```python
from notion_py_client.requests.page_requests import UpdatePageParameters

async with NotionAsyncClient(auth="secret_xxx") as client:
    params = UpdatePageParameters(
        page_id="page_abc123",
        properties={
            "Status": StatusPropertyRequest(
                status={"name": "Done"}
            ),
        }
    )

    page = await client.pages.update(params)
    print(f"Updated page: {page.id}")
```

### Retrieve a Database

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    # Get database metadata and data sources list
    db = await client.databases.retrieve(
        {"database_id": "db_abc123"}
    )

    print(f"Database: {db.title}")
    print(f"Data sources: {len(db.data_sources)}")

    # Get schema from first data source
    if db.data_sources:
        ds = await client.dataSources.retrieve(
            data_source_id=db.data_sources[0]["id"]
        )

        for name, config in ds.properties.items():
            print(f"{name}: {config.type}")
```

## Understanding 2025-09-03 API Changes

The key concept change in API 2025-09-03:

**Old API (before 2025-09-03)**:

- Database = data + schema

**New API (2025-09-03+)**:

- Database = container with multiple data sources
- Data Source = data + schema (equivalent to old database)

**Migration guide**:

| Old API                             | New API                               |
| ----------------------------------- | ------------------------------------- |
| `databases.query()`                 | `dataSources.query()`                 |
| `databases.retrieve()` → properties | `dataSources.retrieve()` → properties |
| `databases.retrieve()` → metadata   | `databases.retrieve()` → metadata     |

## Type-Safe Filtering

Use typed filter builders for database queries:

```python
from notion_py_client.filters import (
    TextPropertyFilter,
    StatusPropertyFilter,
    CompoundFilter,
)

# Single filter
filter = TextPropertyFilter(
    property="Name",
    rich_text={"contains": "urgent"}
)

# Compound filter
filter = CompoundFilter.and_(
    StatusPropertyFilter(
        property="Status",
        status={"equals": "In Progress"}
    ),
    TextPropertyFilter(
        property="Name",
        rich_text={"is_not_empty": True}
    ),
)

response = await client.dataSources.query(
    data_source_id="ds_abc123",
    filter=filter.model_dump(by_alias=True, exclude_none=True)
)
```

## Error Handling

```python
from notion_py_client.notion_client import (
    APIResponseError,
    RequestTimeoutError,
    UnknownHTTPResponseError,
)

async with NotionAsyncClient(auth="secret_xxx") as client:
    try:
        page = await client.pages.retrieve({"page_id": "page_id"})
    except APIResponseError as e:
        print(f"API Error: {e.code} - {e.message}")
    except RequestTimeoutError:
        print("Request timed out")
    except UnknownHTTPResponseError as e:
        print(f"HTTP Error: {e.status}")
```

## Next Steps

- [Databases API](api/databases.md) - Work with database containers
- [Data Sources API](api/datasources.md) - Query and manage data
- [Pages API](api/pages.md) - Create and update pages
- [Type Reference](types/index.md) - Explore available types
