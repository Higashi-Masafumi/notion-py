# Copilot Instructions for notion-py-client

## Project Overview

**notion-py-client** is a type-safe Python client library for the Notion API, built with Pydantic v2. It provides a complete type system mirroring Notion's TypeScript API definitions, covering Databases, DataSources, Pages, Blocks (33 types), Filters, and Request types.

## Notion API Reference

- [Notion API Documentation](https://developers.notion.com/reference/intro)
- [Blocks](https://developers.notion.com/reference/block)
- [Databases](https://developers.notion.com/reference/database)
- [Pages](https://developers.notion.com/reference/page)
- [Users](https://developers.notion.com/reference/user)
- [Properties](https://developers.notion.com/reference/property)

## Architecture & Design Patterns

### 1. Enum + Literal Pattern (Core Convention)

All type discriminators follow this pattern:

- **Base class**: Uses `Enum` for the `type` field
- **Subclasses**: Override with `Literal` for specific types

```python
# Base class (blocks/base.py)
class BaseBlockObject(BaseModel):
    type: BlockType = Field(...)  # Enum

# Subclass (blocks/text_blocks.py)
class ParagraphBlock(BaseBlockObject):
    type: Literal[BlockType.PARAGRAPH] = BlockType.PARAGRAPH  # Literal override
    paragraph: ParagraphBlockContent
```

This pattern is used throughout: `BlockType`, `PropertyType`, `FilterType`, etc.

### 2. Module Organization

```
notion_py_client/
├── blocks/          # 33 block types (text, layout, media, special)
├── filters/         # Query filters (property, compound, date, timestamp)
├── models/          # Shared models (icon, cover, user, parent, rich_text)
├── properties/      # Property types (relation, rollup, base_properties/)
├── requests/        # Request types for create/update operations
├── responses/       # API response types (page, database, datasource)
└── schema/          # Database schema definitions
```

**Key Files**:

- `notion_py_client/__init__.py` - Public API surface (all exports)
- `blocks/base.py` - `BlockType` enum + `BaseBlockObject`
- `responses/page.py` - `NotionPage` (main entity)
- `requests/page_requests.py` - `CreatePageParameters`, `UpdatePageParameters`

### 3. Property Request System

For page creation/updates, use typed property requests (not raw dicts):

```python
from notion_py_client.requests.property_requests import (
    TitlePropertyRequest,
    StatusPropertyRequest,
)

properties = {
    "タスク名": TitlePropertyRequest(
        title=[{"type": "text", "text": {"content": "My Task"}}]
    ),
    "ステータス": StatusPropertyRequest(
        status={"name": "In Progress"}
    ),
}
```

**14 property request types** defined in `requests/property_requests.py`.

### 4. Filter System

Build type-safe database queries with filter builders:

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
    StatusPropertyFilter(property="Status", status={"equals": "In Progress"}),
    TextPropertyFilter(property="Name", rich_text={"is_not_empty": True}),
)
```

## Development Workflow

### Package Management (uv)

```bash
# Install dependencies
uv sync

# Add dependency
uv add <package>

# Run with Python environment
uv run python main.py
```

### Building & Publishing

```bash
# Build package (using hatchling)
python -m build

# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Upload to PyPI
python -m twine upload dist/*
```

**Note**: No `setup.py` required - `pyproject.toml` only (PEP 517/518/621).

### Documentation (MkDocs Material)

```bash
# Install docs dependencies
uv add mkdocs mkdocs-material mkdocstrings[python]

# Serve locally
mkdocs serve

# Build
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

**Documentation structure** (`docs/`):

- `index.md` - Landing page
- `quickstart.md` - Getting started guide
- `api/` - Endpoint documentation (databases, datasources, pages, blocks, users, comments, search)
- `types/` - Type reference (blocks, properties, filters, requests)
- `advanced/` - Advanced patterns (mapper for domain models)

**Style**: FastAPI-like documentation (no emoji decorations, clean technical style)

## Code Conventions

### Strict Typing

- Use Pydantic `StrictStr`, `StrictInt`, `StrictBool` (not `str`, `int`, `bool`)
- All models inherit from `BaseModel`
- Use `Field(...)` for required fields, `Field(default)` for optional

### Import Style

```python
from __future__ import annotations  # Top of file for forward refs

from typing import Literal, Union
from pydantic import BaseModel, Field, StrictStr
```

### Naming Conventions

- **Classes**: PascalCase (`NotionPage`, `ParagraphBlock`)
- **Enums**: PascalCase for class, UPPER_SNAKE_CASE for values
- **Files**: snake_case (`text_blocks.py`, `property_requests.py`)
- **Module names**: Match import usage (`notion_py_client`, not `notion-py-client`)

## Testing & Quality

Currently no test suite. When adding tests:

- Use `pytest` (add to `[project.optional-dependencies]`)
- Test property request validation
- Test filter query building
- Mock Notion API responses

## Key Integration Points

### External Dependencies

- **Pydantic v2**: Core validation engine (required `>=2.11.10`)
- **Notion API**: This library provides types only - pair with HTTP client:

  ```python
  import httpx
  from notion_py_client import NotionPage, CreatePageParameters

  # Use with your preferred HTTP client
  async with httpx.AsyncClient() as client:
      response = await client.post(
          "https://api.notion.com/v1/pages",
          json=CreatePageParameters(...).model_dump(by_alias=True)
      )
      page = NotionPage.model_validate(response.json())
  ```

### Package Structure

- **Package name**: `notion-py-client` (PyPI, with hyphen)
- **Import name**: `notion_py_client` (Python, with underscore)
- **Build backend**: `hatchling` (auto-detects `notion_py_client/` directory)

## Common Tasks

**Add a new block type**:

1. Define in appropriate file (`blocks/text_blocks.py`, etc.)
2. Use Enum+Literal pattern for `type` field
3. Export in `blocks/__init__.py`
4. Export in `notion_py_client/__init__.py`

**Add a new property request**:

1. Define in `requests/property_requests.py`
2. Inherit from base or create new union type
3. Add to `PropertyRequest` union type

**Add a new filter**:

1. Define in appropriate filter file (`filters/property_filters.py`, etc.)
2. Follow existing filter patterns (existence, comparison, etc.)
3. Export in `filters/__init__.py`
