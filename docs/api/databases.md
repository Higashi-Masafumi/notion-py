# Databases API

Databases are containers that hold multiple data sources in Notion API 2025-09-03.

## Overview

The Databases API provides methods to:

- Retrieve database metadata and data sources list
- Create new databases with initial data source
- Update database-level properties (title, icon, cover)

For querying data or managing schema, use the [Data Sources API](datasources.md).

## Methods

### retrieve

Retrieve a database with its metadata and data sources list.

```python
async def retrieve(
    params: RetrieveDatabaseParameters,
    *,
    auth: AuthParam | None = None
) -> NotionDatabase
```

**Parameters**:

- `params.database_id` (str): Database ID
- `auth` (optional): Override authentication token

**Returns**: `NotionDatabase` object containing:

- Database metadata (title, icon, cover, etc.)
- `data_sources` array with IDs and names

**Example**:

```python
from notion_py_client import NotionAsyncClient

async with NotionAsyncClient(auth="secret_xxx") as client:
    db = await client.databases.retrieve(
        {"database_id": "db_abc123"}
    )

    print(f"Title: {db.title}")
    print(f"Created: {db.created_time}")

    # List data sources
    for ds in db.data_sources:
        print(f"- {ds['name']} (ID: {ds['id']})")
```

### create

Create a new database with an initial data source.

```python
async def create(
    params: CreateDatabaseParameters,
    *,
    auth: AuthParam | None = None
) -> NotionDatabase
```

**Parameters**:

- `params.parent`: Parent page or workspace
- `params.title`: Database title (RichText array)
- `params.initial_data_source`: Initial data source configuration
  - `properties`: Schema definition
  - `name` (optional): Data source name

**Returns**: Created `NotionDatabase`

**Example**:

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    db = await client.databases.create({
        "parent": {
            "type": "page_id",
            "page_id": "parent_page_id"
        },
        "title": [
            {"type": "text", "text": {"content": "Project Tracker"}}
        ],
        "initial_data_source": {
            "name": "Main Data",
            "properties": {
                "Name": {
                    "title": {}
                },
                "Status": {
                    "select": {
                        "options": [
                            {"name": "Not Started", "color": "gray"},
                            {"name": "In Progress", "color": "blue"},
                            {"name": "Done", "color": "green"}
                        ]
                    }
                },
                "Due Date": {
                    "date": {}
                }
            }
        }
    })

    print(f"Created database: {db.id}")
```

### update

Update database-level properties.

```python
async def update(
    params: UpdateDatabaseParameters,
    *,
    auth: AuthParam | None = None
) -> NotionDatabase
```

**Parameters**:

- `params.database_id` (str): Database ID to update
- `params.title` (optional): New title
- `params.icon` (optional): New icon
- `params.cover` (optional): New cover image
- `params.is_inline` (optional): Inline display setting
- `params.parent` (optional): New parent

**Note**: To update data source properties, use `dataSources.update()` instead.

**Returns**: Updated `NotionDatabase`

**Example**:

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    db = await client.databases.update({
        "database_id": "db_abc123",
        "title": [
            {"type": "text", "text": {"content": "Updated Title"}}
        ],
        "icon": {
            "type": "emoji",
            "emoji": "📊"
        }
    })

    print(f"Updated: {db.title}")
```

## Common Patterns

### Get Database Schema

To access the schema (properties), retrieve the data source:

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    # 1. Get database and data sources
    db = await client.databases.retrieve(
        {"database_id": "db_abc123"}
    )

    # 2. Get schema from first data source
    if db.data_sources:
        ds = await client.dataSources.retrieve(
            data_source_id=db.data_sources[0]["id"]
        )

        # Access properties
        for name, config in ds.properties.items():
            print(f"{name}: {config.type}")
```

### List All Data Sources

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    db = await client.databases.retrieve(
        {"database_id": "db_abc123"}
    )

    # Retrieve full details for each data source
    for ds_ref in db.data_sources:
        ds = await client.dataSources.retrieve(
            data_source_id=ds_ref["id"]
        )
        print(f"Data Source: {ds_ref['name']}")
        print(f"  Properties: {list(ds.properties.keys())}")
```

## Type Reference

```python
from notion_py_client.responses.database import NotionDatabase

# Database object structure
database: NotionDatabase = {
    "object": "database",
    "id": "db_abc123",
    "title": [...],
    "icon": {...},
    "cover": {...},
    "created_time": "2025-01-01T00:00:00.000Z",
    "created_by": {...},
    "last_edited_time": "2025-01-02T00:00:00.000Z",
    "last_edited_by": {...},
    "parent": {...},
    "archived": false,
    "is_inline": false,
    "public_url": "https://...",
    "data_sources": [
        {"id": "ds_abc123", "name": "Main Data"},
        {"id": "ds_def456", "name": "Archive"}
    ]
}
```

## Related

- [Data Sources API](datasources.md) - Query data and manage schema
- [Pages API](pages.md) - Create pages in databases
- [Type Reference](../types/index.md) - Complete type definitions
