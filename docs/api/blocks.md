# Blocks API

Manage block content in Notion pages.

## Overview

Blocks are the building blocks of Notion pages. The Blocks API provides methods to:

- Retrieve block details
- Update block content
- Delete (archive) blocks
- List and append child blocks

## Methods

### retrieve

Retrieve a block by ID.

```python
async def retrieve(
    *,
    block_id: str,
    auth: AuthParam | None = None
) -> dict[str, Any]
```

**Example**:

```python
from notion_py_client import NotionAsyncClient

async with NotionAsyncClient(auth="secret_xxx") as client:
    block = await client.blocks.retrieve(block_id="block_abc123")

    print(f"Type: {block['type']}")
    print(f"Has children: {block['has_children']}")
```

### update

Update a block's content.

```python
async def update(
    *,
    block_id: str,
    **body
) -> dict[str, Any]
```

**Example**:

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    # Update paragraph text
    block = await client.blocks.update(
        block_id="block_abc123",
        paragraph={
            "rich_text": [
                {"type": "text", "text": {"content": "Updated text"}}
            ]
        }
    )
```

### delete

Delete (archive) a block.

```python
async def delete(
    *,
    block_id: str,
    auth: AuthParam | None = None
) -> dict[str, Any]
```

**Example**:

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    block = await client.blocks.delete(block_id="block_abc123")
    print(f"Archived: {block['archived']}")
```

### children.list

List child blocks of a block or page.

```python
async def children.list(
    *,
    block_id: str,
    start_cursor: str | None = None,
    page_size: int | None = None,
    auth: AuthParam | None = None
) -> dict[str, Any]
```

**Example**:

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    response = await client.blocks.children.list(
        block_id="page_abc123",
        page_size=100
    )

    for block in response["results"]:
        print(f"{block['type']}: {block['id']}")
```

### children.append

Append child blocks to a block or page.

```python
async def children.append(
    *,
    block_id: str,
    children: list[dict[str, Any]],
    after: str | None = None,
    auth: AuthParam | None = None
) -> dict[str, Any]
```

**Example**:

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    response = await client.blocks.children.append(
        block_id="page_abc123",
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "First paragraph"}}
                    ]
                }
            },
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Section Title"}}
                    ]
                }
            }
        ]
    )
```

## Block Types

### Text Blocks

```python
# Paragraph
{
    "type": "paragraph",
    "paragraph": {
        "rich_text": [
            {"type": "text", "text": {"content": "Text content"}}
        ],
        "color": "default"
    }
}

# Headings
{
    "type": "heading_1",  # or heading_2, heading_3
    "heading_1": {
        "rich_text": [
            {"type": "text", "text": {"content": "Heading"}}
        ],
        "color": "default",
        "is_toggleable": false
    }
}

# Lists
{
    "type": "bulleted_list_item",  # or numbered_list_item
    "bulleted_list_item": {
        "rich_text": [
            {"type": "text", "text": {"content": "List item"}}
        ],
        "color": "default"
    }
}

# To-do
{
    "type": "to_do",
    "to_do": {
        "rich_text": [
            {"type": "text", "text": {"content": "Task"}}
        ],
        "checked": false,
        "color": "default"
    }
}

# Toggle
{
    "type": "toggle",
    "toggle": {
        "rich_text": [
            {"type": "text", "text": {"content": "Toggle"}}
        ],
        "color": "default"
    }
}

# Quote
{
    "type": "quote",
    "quote": {
        "rich_text": [
            {"type": "text", "text": {"content": "Quoted text"}}
        ],
        "color": "default"
    }
}

# Code
{
    "type": "code",
    "code": {
        "rich_text": [
            {"type": "text", "text": {"content": "console.log('hello')"}}
        ],
        "language": "javascript",
        "caption": []
    }
}

# Callout
{
    "type": "callout",
    "callout": {
        "rich_text": [
            {"type": "text", "text": {"content": "Important note"}}
        ],
        "icon": {"type": "emoji", "emoji": "💡"},
        "color": "gray_background"
    }
}
```

### Media Blocks

```python
# Image
{
    "type": "image",
    "image": {
        "type": "external",
        "external": {"url": "https://example.com/image.png"}
    }
}

# Video
{
    "type": "video",
    "video": {
        "type": "external",
        "external": {"url": "https://youtube.com/watch?v=..."}
    }
}

# File
{
    "type": "file",
    "file": {
        "type": "external",
        "external": {"url": "https://example.com/file.pdf"},
        "caption": []
    }
}

# Bookmark
{
    "type": "bookmark",
    "bookmark": {
        "url": "https://example.com",
        "caption": []
    }
}

# Embed
{
    "type": "embed",
    "embed": {
        "url": "https://example.com/embed"
    }
}
```

### Layout Blocks

```python
# Divider
{
    "type": "divider",
    "divider": {}
}

# Table of Contents
{
    "type": "table_of_contents",
    "table_of_contents": {
        "color": "default"
    }
}

# Breadcrumb
{
    "type": "breadcrumb",
    "breadcrumb": {}
}

# Column List
{
    "type": "column_list",
    "column_list": {}
}

# Column (child of column_list)
{
    "type": "column",
    "column": {}
}
```

### Special Blocks

```python
# Equation
{
    "type": "equation",
    "equation": {
        "expression": "E = mc^2"
    }
}

# Table
{
    "type": "table",
    "table": {
        "table_width": 3,
        "has_column_header": true,
        "has_row_header": false
    }
}

# Table Row (child of table)
{
    "type": "table_row",
    "table_row": {
        "cells": [
            [{"type": "text", "text": {"content": "Cell 1"}}],
            [{"type": "text", "text": {"content": "Cell 2"}}],
            [{"type": "text", "text": {"content": "Cell 3"}}]
        ]
    }
}

# Child Page
{
    "type": "child_page",
    "child_page": {
        "title": "Subpage Title"
    }
}

# Child Database
{
    "type": "child_database",
    "child_database": {
        "title": "Database Title"
    }
}
```

## Common Patterns

### Build Page Content

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    await client.blocks.children.append(
        block_id="page_abc123",
        children=[
            # Title
            {
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Article Title"}}
                    ]
                }
            },
            # Introduction
            {
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Introduction paragraph."}}
                    ]
                }
            },
            # Section
            {
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Section 1"}}
                    ]
                }
            },
            # List
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "First item"}}
                    ]
                }
            },
            # Code
            {
                "type": "code",
                "code": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "print('hello')"}}
                    ],
                    "language": "python"
                }
            }
        ]
    )
```

### Get All Blocks (Recursively)

```python
async def get_all_blocks(client, block_id, blocks=[]):
    response = await client.blocks.children.list(
        block_id=block_id,
        page_size=100
    )

    for block in response["results"]:
        blocks.append(block)

        if block.get("has_children"):
            await get_all_blocks(client, block["id"], blocks)

    if response.get("has_more"):
        # Handle pagination
        pass

    return blocks

async with NotionAsyncClient(auth="secret_xxx") as client:
    all_blocks = await get_all_blocks(client, "page_abc123")
    print(f"Total blocks: {len(all_blocks)}")
```

### Update Multiple Blocks

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    block_ids = ["block1", "block2", "block3"]

    for block_id in block_ids:
        await client.blocks.update(
            block_id=block_id,
            paragraph={
                "rich_text": [
                    {"type": "text", "text": {"content": "Updated"}}
                ]
            }
        )
```

## Rich Text Formatting

```python
# Bold
{"type": "text", "text": {"content": "bold"}, "annotations": {"bold": true}}

# Italic
{"type": "text", "text": {"content": "italic"}, "annotations": {"italic": true}}

# Strikethrough
{"type": "text", "text": {"content": "strike"}, "annotations": {"strikethrough": true}}

# Underline
{"type": "text", "text": {"content": "underline"}, "annotations": {"underline": true}}

# Code
{"type": "text", "text": {"content": "code"}, "annotations": {"code": true}}

# Color
{"type": "text", "text": {"content": "colored"}, "annotations": {"color": "red"}}

# Link
{"type": "text", "text": {"content": "link", "link": {"url": "https://example.com"}}}

# Mention
{"type": "mention", "mention": {"type": "user", "user": {"id": "user_id"}}}

# Equation
{"type": "equation", "equation": {"expression": "x^2"}}
```

## Related

- [Pages API](pages.md) - Create pages to add blocks to
- [Block Types](../types/blocks.md) - Complete block type reference
