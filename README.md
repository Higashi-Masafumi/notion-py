# notion-py-client

A type-safe Python client library for the Notion API, built with Pydantic v2.

[![PyPI version](https://badge.fury.io/py/notion-py-client.svg)](https://pypi.org/project/notion-py-client/)
[![Python Version](https://img.shields.io/pypi/pyversions/notion-py-client.svg)](https://pypi.org/project/notion-py-client/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **Type-Safe**: Complete type definitions using Pydantic v2
- **Async-First**: Built on httpx for async/await support
- **API 2025-09-03**: Latest Notion API with DataSources support
- **Comprehensive**: All blocks, properties, filters, and request types
- **Domain Mapping**: Built-in mapper for converting to domain models

## Installation

```bash
pip install notion-py-client
```

## Quick Start

```python
import asyncio
from notion_py_client import NotionAsyncClient

async def main():
    client = NotionAsyncClient(auth="your_NOTION_API_TOKEN")

    # Query a database (API 2025-09-03)
    response = await client.dataSources.query(
        data_source_id="your_database_id"
    )

    for page in response.results:
        print(page.id, page.properties)

asyncio.run(main())
```

## Notion API 2025-09-03

This library supports the latest Notion API version `2025-09-03`, which introduces:

- **DataSources**: New paradigm replacing the legacy databases endpoint
- **Backward Compatibility**: Legacy `databases` endpoint still supported
- **Migration Path**: Seamless transition from databases to dataSources

### DataSources vs Databases

```python
# New DataSources API (recommended)
await client.dataSources.query(data_source_id="...")

# Legacy Databases API (still supported)
await client.databases.query(database_id="...")
```

Both endpoints work identically, but `dataSources` is the future-proof choice.

## Documentation

Full documentation is available at: [https://higashi-masafumi.github.io/notion-py/](https://higashi-masafumi.github.io/notion-py/)

- [Quick Start Guide](https://higashi-masafumi.github.io/notion-py/quickstart/)
- [API Reference](https://higashi-masafumi.github.io/notion-py/api/databases/)
- [Type Reference](https://higashi-masafumi.github.io/notion-py/types/)
- [Advanced Usage](https://higashi-masafumi.github.io/notion-py/advanced/mapper/)

## Core Capabilities

### Pages

```python
# Create a page
from notion_py_client.requests import CreatePageParameters, TitlePropertyRequest

await client.pages.create(
    parameters=CreatePageParameters(
        parent={"database_id": "your_database_id"},
        properties={
            "Name": TitlePropertyRequest(
                title=[{"type": "text", "text": {"content": "New Page"}}]
            )
        }
    )
)
```

### Filters

```python
from notion_py_client import NotionAsyncClient
from notion_py_client.filters import create_and_filter, create_or_filter

client = NotionAsyncClient(auth="your_NOTION_API_TOKEN")

# Simple filter (直接辞書 - IDE補完が効く)
response = await client.dataSources.query(
    data_source_id="your_database_id",
    filter={"property": "Status", "status": {"equals": "Active"}}
)

# AND filter with helper function (型安全 - IDE補完が効く)
filter = create_and_filter(
    {"property": "Name", "rich_text": {"contains": "urgent"}},
    {"property": "Status", "status": {"equals": "In Progress"}}
)

# OR filter with helper function
filter = create_or_filter(
    {"property": "Priority", "select": {"equals": "High"}},
    {"property": "Priority", "select": {"equals": "Medium"}}
)

# Nested filters (AND + OR)
filter = create_and_filter(
    {"property": "Team", "select": {"equals": "Engineering"}},
    create_or_filter(
        {"property": "Status", "status": {"equals": "Active"}},
        {"property": "Status", "status": {"equals": "Pending"}}
    )
)

await client.dataSources.query(
    data_source_id="your_database_id",
    filter=filter
)
```

**Key Benefits:**

- **IDE Completion**: Type hints work correctly with dictionary literals
- **Type Safety**: TypedDict definitions match official TypeScript SDK
- **No `.model_dump()`**: Use filters directly without conversion
- **Public API Compatible**: Follows official Notion API specification

### Domain Mapping

```python
from notion_py_client.helper import NotionMapper, NotionPropertyDescriptor, Field
from notion_py_client.requests.property_requests import (
    TitlePropertyRequest,
    StatusPropertyRequest,
)
from notion_py_client.responses.property_types import TitleProperty, StatusProperty
from pydantic import BaseModel

class Task(BaseModel):
    id: str
    name: str
    status: str

class TaskMapper(NotionMapper[Task]):
    # Define field descriptors with type annotations
    name_field: NotionPropertyDescriptor[TitleProperty, TitlePropertyRequest, str] = Field(
        notion_name="Name",
        parser=lambda p: p.title[0].plain_text if p.title else "",
        request_builder=lambda v: TitlePropertyRequest(
            title=[{"type": "text", "text": {"content": v}}]
        )
    )

    status_field: NotionPropertyDescriptor[StatusProperty, StatusPropertyRequest, str] = Field(
        notion_name="Status",
        parser=lambda p: p.status.name if p.status else "",
        request_builder=lambda v: StatusPropertyRequest(
            status={"name": v}
        )
    )

    def to_domain(self, notion_page):
        """Convert Notion page to domain model."""
        props = notion_page.properties
        return Task(
            id=notion_page.id,
            name=self.name_field.parse(props["Name"]),
            status=self.status_field.parse(props["Status"]),
        )

# Use the mapper
mapper = TaskMapper()
tasks = [mapper.to_domain(page) for page in response.results]
```

## Requirements

- Python >= 3.10
- Pydantic >= 2.11.10

## License

MIT License - see [LICENSE](LICENSE) for details.
