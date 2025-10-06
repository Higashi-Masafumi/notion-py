# notion-py

A type-safe Python client library for the Notion API, built with Pydantic v2.

[![PyPI version](https://badge.fury.io/py/notion-py.svg)](https://badge.fury.io/py/notion-py)
[![Python Version](https://img.shields.io/pypi/pyversions/notion-py.svg)](https://pypi.org/project/notion-py/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **Type-Safe**: Complete type definitions using Pydantic v2
- **Async-First**: Built on httpx for async/await support
- **API 2025-09-03**: Latest Notion API with DataSources support
- **Comprehensive**: All blocks, properties, filters, and request types
- **Domain Mapping**: Built-in mapper for converting to domain models

## Installation

```bash
pip install notion-py
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
from pydantic import BaseModel

class Task(BaseModel):
    name: str
    status: str

class TaskMapper(NotionMapper[Task]):
    name = Field("タスク名", "title")
    status = Field("ステータス", "status")

# Convert Notion page to domain model
task = TaskMapper.to_model(notion_page)
```

## Requirements

- Python >= 3.13
- Pydantic >= 2.11.10

## License

MIT License - see [LICENSE](LICENSE) for details.
