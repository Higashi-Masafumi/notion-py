# notion-py

A type-safe Python client library for the Notion API, built with Pydantic v2.

[![PyPI version](https://badge.fury.io/py/notion-py.svg)](https://pypi.org/project/notion-py-client/0.1.2/)
[![Python Version](https://img.shields.io/pypi/pyversions/notion-py.svg)](https://pypi.org/project/notion-py-client/0.1.2/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **Type-Safe**: Complete type definitions using Pydantic v2
- **Async-First**: Built on httpx for async/await support
- **API 2025-09-03**: Latest Notion API with DataSources support
- **Comprehensive**: All blocks, properties, filters, and request types
- **Domain Mapping**: Built-in mapper for converting to domain models

## Installation

```bash
pip install notion-py-client==0.1.2
```

## Quick Start

```python
import asyncio
from notion_py import NotionAsyncClient

async def main():
    client = NotionAsyncClient(auth="your_notion_api_key")

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
from notion_py.requests import CreatePageParameters, TitlePropertyRequest

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
from notion_py.filters import TextPropertyFilter, CompoundFilter

# Type-safe query filters
filter = CompoundFilter.and_(
    TextPropertyFilter(property="Name", rich_text={"contains": "urgent"}),
    TextPropertyFilter(property="Status", rich_text={"equals": "In Progress"})
)

await client.dataSources.query(
    data_source_id="your_database_id",
    filter=filter
)
```

### Domain Mapping

```python
from notion_py.helpder import NotionMapper, Field
from notion_py.requests.property_requests import (
    TitlePropertyRequest,
    StatusPropertyRequest,
)
from pydantic import BaseModel

class Task(BaseModel):
    id: str
    name: str
    status: str

class TaskMapper(NotionMapper[Task]):
    # Define field descriptors
    name_field = Field(
        notion_name="タスク名",
        parser=lambda p: p.title[0].plain_text if p.title else "",
        request_builder=lambda v: TitlePropertyRequest(
            title=[{"type": "text", "text": {"content": v}}]
        )
    )

    status_field = Field(
        notion_name="ステータス",
        parser=lambda p: p.status.name if p.status else "",
        request_builder=lambda v: StatusPropertyRequest(
            status={"name": v}
        )
    )

    def to_domain(self, notion_page):
        """Convert Notion page to domain model."""
        return Task(
            id=notion_page.id,
            name=self.name_field.parse(notion_page.properties["タスク名"]),
            status=self.status_field.parse(notion_page.properties["ステータス"]),
        )

# Use the mapper
mapper = TaskMapper()
task = mapper.to_domain(notion_page)
```

## Requirements

- Python >= 3.10
- Pydantic >= 2.11.10

## License

MIT License - see [LICENSE](LICENSE) for details.
