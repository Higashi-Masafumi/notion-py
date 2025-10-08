# Data Sources API

Data sources contain actual data (pages) and schema (properties). They are equivalent to databases in the old Notion API.

## Overview

The Data Sources API provides methods to:

- Query pages (data rows) with filters and sorting
- Retrieve schema (property configurations)
- Create new data sources in existing databases
- Update schema and settings

## Methods

### query

Query pages from a data source.

```python
async def query(
    *,
    data_source_id: str,
    filter: dict[str, Any] | None = None,
    sorts: list[dict[str, Any]] | None = None,
    start_cursor: str | None = None,
    page_size: int | None = None,
    auth: AuthParam | None = None
) -> QueryDataSourceResponse
```

**Parameters**:

- `data_source_id` (str): Data source ID
- `filter` (optional): Filter conditions
- `sorts` (optional): Sort criteria
- `start_cursor` (optional): Pagination cursor
- `page_size` (optional): Results per page (max 100)

**Returns**: `QueryDataSourceResponse` with:

- `results`: List of `NotionPage` or `PartialPage`
- `has_more`: Whether more results exist
- `next_cursor`: Cursor for next page

**Example**:

```python
from notion_py_client import NotionAsyncClient

async with NotionAsyncClient(auth="secret_xxx") as client:
    # Basic query
    response = await client.dataSources.query(
        data_source_id="ds_abc123",
        page_size=50
    )

    for page in response.results:
        print(f"Page: {page.id}")

    # With filter
    response = await client.dataSources.query(
        data_source_id="ds_abc123",
        filter={
            "property": "Status",
            "select": {"equals": "Done"}
        }
    )

    # With sorting
    response = await client.dataSources.query(
        data_source_id="ds_abc123",
        sorts=[
            {
                "property": "Created",
                "direction": "descending"
            }
        ]
    )
```

### retrieve

Retrieve a data source with its schema.

```python
async def retrieve(
    *,
    data_source_id: str,
    auth: AuthParam | None = None
) -> DataSource
```

**Parameters**:

- `data_source_id` (str): Data source ID

**Returns**: `DataSource` object with properties schema

**Example**:

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    ds = await client.dataSources.retrieve(
        data_source_id="ds_abc123"
    )

    # Access schema
    for name, config in ds.properties.items():
        print(f"{name}: {config.type}")

        if config.type == "select":
            print(f"  Options: {[opt.name for opt in config.select.options]}")
```

### create

Create a new data source in an existing database.

```python
async def create(
    *,
    parent: dict[str, Any],
    title: list[dict[str, Any]] | None = None,
    properties: dict[str, Any],
    auth: AuthParam | None = None
) -> DataSource
```

**Parameters**:

- `parent`: Parent database (`{"type": "database_id", "database_id": "..."}`)
- `title` (optional): Data source title
- `properties`: Schema definition

**Returns**: Created `DataSource`

**Example**:

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    ds = await client.dataSources.create(
        parent={
            "type": "database_id",
            "database_id": "db_abc123"
        },
        title=[
            {"type": "text", "text": {"content": "Q4 Data"}}
        ],
        properties={
            "Task": {"title": {}},
            "Priority": {
                "select": {
                    "options": [
                        {"name": "High", "color": "red"},
                        {"name": "Medium", "color": "yellow"},
                        {"name": "Low", "color": "gray"}
                    ]
                }
            },
            "Assignee": {"people": {}}
        }
    )

    print(f"Created data source: {ds.id}")
```

### update

Update data source schema or title.

```python
async def update(
    *,
    data_source_id: str,
    title: list[dict[str, Any]] | None = None,
    properties: dict[str, Any] | None = None,
    auth: AuthParam | None = None
) -> DataSource
```

**Parameters**:

- `data_source_id` (str): Data source ID
- `title` (optional): New title
- `properties` (optional): Properties to add/update/delete

**Note**: To delete a property, set it to `None`

**Returns**: Updated `DataSource`

**Example**:

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    # Add new property
    ds = await client.dataSources.update(
        data_source_id="ds_abc123",
        properties={
            "Deadline": {"date": {}}
        }
    )

    # Remove property
    ds = await client.dataSources.update(
        data_source_id="ds_abc123",
        properties={
            "Old Field": None
        }
    )

    # Update select options
    ds = await client.dataSources.update(
        data_source_id="ds_abc123",
        properties={
            "Status": {
                "select": {
                    "options": [
                        {"name": "Todo", "color": "gray"},
                        {"name": "Done", "color": "green"}
                    ]
                }
            }
        }
    )
```

## Filtering

### Type-Safe Filters

Use filter builders for type safety:

```python
from notion_py_client.filters import (
    TextPropertyFilter,
    StatusPropertyFilter,
    DatePropertyFilter,
    CompoundFilter,
)

# Text filter
filter = TextPropertyFilter(
    property="Name",
    rich_text={"contains": "urgent"}
)

# Status filter
filter = StatusPropertyFilter(
    property="Status",
    status={"equals": "In Progress"}
)

# Date filter
filter = DatePropertyFilter(
    property="Due Date",
    date={"on_or_after": "2025-01-01"}
)

# Combine filters
filter = CompoundFilter.and_(
    StatusPropertyFilter(property="Status", status={"equals": "In Progress"}),
    DatePropertyFilter(property="Due Date", date={"on_or_before": "2025-12-31"}),
)

# Use in query
response = await client.dataSources.query(
    data_source_id="ds_abc123",
    filter=filter.model_dump(by_alias=True, exclude_none=True)
)
```

### Raw Filter Format

Alternatively, use raw dictionaries:

```python
# Property filter
filter = {
    "property": "Status",
    "select": {"equals": "Done"}
}

# Compound filter
filter = {
    "and": [
        {"property": "Status", "select": {"equals": "In Progress"}},
        {"property": "Priority", "select": {"equals": "High"}}
    ]
}
```

## Sorting

```python
# Single sort
response = await client.dataSources.query(
    data_source_id="ds_abc123",
    sorts=[
        {"property": "Created", "direction": "descending"}
    ]
)

# Multiple sorts
response = await client.dataSources.query(
    data_source_id="ds_abc123",
    sorts=[
        {"property": "Priority", "direction": "ascending"},
        {"property": "Created", "direction": "descending"}
    ]
)

# Sort by timestamp
response = await client.dataSources.query(
    data_source_id="ds_abc123",
    sorts=[
        {"timestamp": "last_edited_time", "direction": "descending"}
    ]
)
```

## Pagination

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    all_pages = []
    cursor = None

    while True:
        response = await client.dataSources.query(
            data_source_id="ds_abc123",
            start_cursor=cursor,
            page_size=100
        )

        all_pages.extend(response.results)

        if not response.has_more:
            break

        cursor = response.next_cursor

    print(f"Total pages: {len(all_pages)}")
```

## Property Types

Common property configurations:

```python
properties = {
    # Text
    "Title": {"title": {}},
    "Description": {"rich_text": {}},

    # Number
    "Price": {"number": {"format": "dollar"}},

    # Select
    "Status": {
        "select": {
            "options": [
                {"name": "Todo", "color": "gray"},
                {"name": "Done", "color": "green"}
            ]
        }
    },

    # Multi-select
    "Tags": {
        "multi_select": {
            "options": [
                {"name": "Important", "color": "red"},
                {"name": "Review", "color": "blue"}
            ]
        }
    },

    # Date
    "Due Date": {"date": {}},

    # People
    "Assignee": {"people": {}},

    # Files
    "Attachments": {"files": {}},

    # Checkbox
    "Done": {"checkbox": {}},

    # URL
    "Website": {"url": {}},

    # Email
    "Contact": {"email": {}},

    # Phone
    "Phone": {"phone_number": {}},

    # Relation
    "Related Tasks": {
        "relation": {
            "database_id": "db_other",
            "type": "dual_property",
            "dual_property": {"synced_property_name": "Back Reference"}
        }
    },

    # Rollup
    "Total Cost": {
        "rollup": {
            "relation_property_name": "Related Items",
            "rollup_property_name": "Price",
            "function": "sum"
        }
    },
}
```

## Type Reference

```python
from notion_py_client.responses.datasource import DataSource

# Data source object
data_source: DataSource = {
    "object": "data_source",
    "id": "ds_abc123",
    "name": "Main Data",
    "properties": {
        "Name": {
            "id": "title",
            "type": "title",
            "title": {}
        },
        "Status": {
            "id": "abc123",
            "type": "select",
            "select": {
                "options": [...]
            }
        }
    }
}
```

## Related

- [Databases API](databases.md) - Manage database containers
- [Pages API](pages.md) - Create and update pages
- [Filters](../types/filters.md) - Filter type reference
