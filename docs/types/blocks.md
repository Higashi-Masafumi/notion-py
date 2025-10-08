# Block Types

Complete reference for all 33 block types supported by notion-py-client.

## Base Block

All blocks inherit from `BaseBlockObject`:

```python
from notion_py_client.blocks.base import BaseBlockObject, BlockType

class BaseBlockObject(BaseModel):
    object: Literal["block"] = "block"
    id: str
    type: BlockType
    created_time: str
    created_by: PartialUser
    last_edited_time: str
    last_edited_by: PartialUser
    parent: NotionParent
    has_children: bool = False
    archived: bool = False
```

## Text Blocks

### ParagraphBlock

```python
from notion_py_client import ParagraphBlock

block = ParagraphBlock(
    id="block_id",
    type="paragraph",
    paragraph={
        "rich_text": [
            {"type": "text", "text": {"content": "Paragraph text"}}
        ],
        "color": "default"
    },
    # ... base fields
)
```

### Heading Blocks

```python
from notion_py_client import Heading1Block, Heading2Block, Heading3Block

heading = Heading1Block(
    id="block_id",
    type="heading_1",
    heading_1={
        "rich_text": [
            {"type": "text", "text": {"content": "Heading"}}
        ],
        "color": "default",
        "is_toggleable": False
    },
    # ... base fields
)
```

### List Blocks

```python
from notion_py_client import BulletedListItemBlock, NumberedListItemBlock

bullet = BulletedListItemBlock(
    id="block_id",
    type="bulleted_list_item",
    bulleted_list_item={
        "rich_text": [
            {"type": "text", "text": {"content": "Item"}}
        ],
        "color": "default"
    },
    # ... base fields
)
```

### ToDoBlock

```python
from notion_py_client import ToDoBlock

todo = ToDoBlock(
    id="block_id",
    type="to_do",
    to_do={
        "rich_text": [
            {"type": "text", "text": {"content": "Task"}}
        ],
        "checked": False,
        "color": "default"
    },
    # ... base fields
)
```

### QuoteBlock

```python
from notion_py_client import QuoteBlock

quote = QuoteBlock(
    id="block_id",
    type="quote",
    quote={
        "rich_text": [
            {"type": "text", "text": {"content": "Quoted text"}}
        ],
        "color": "default"
    },
    # ... base fields
)
```

### ToggleBlock

```python
from notion_py_client import ToggleBlock

toggle = ToggleBlock(
    id="block_id",
    type="toggle",
    toggle={
        "rich_text": [
            {"type": "text", "text": {"content": "Toggle content"}}
        ],
        "color": "default"
    },
    has_children=True,
    # ... base fields
)
```

## Special Blocks

### CodeBlock

```python
from notion_py_client import CodeBlock

code = CodeBlock(
    id="block_id",
    type="code",
    code={
        "rich_text": [
            {"type": "text", "text": {"content": "print('hello')"}}
        ],
        "language": "python",
        "caption": []
    },
    # ... base fields
)
```

**Supported languages**: `python`, `javascript`, `typescript`, `java`, `c`, `cpp`, `csharp`, `go`, `rust`, `ruby`, `php`, `sql`, `shell`, `yaml`, `json`, `xml`, `html`, `css`, `markdown`, etc.

### CalloutBlock

```python
from notion_py_client import CalloutBlock

callout = CalloutBlock(
    id="block_id",
    type="callout",
    callout={
        "rich_text": [
            {"type": "text", "text": {"content": "Important note"}}
        ],
        "icon": {"type": "emoji", "emoji": "💡"},
        "color": "gray_background"
    },
    # ... base fields
)
```

### EquationBlock

```python
from notion_py_client import EquationBlock

equation = EquationBlock(
    id="block_id",
    type="equation",
    equation={
        "expression": "E = mc^2"
    },
    # ... base fields
)
```

### ChildPageBlock

```python
from notion_py_client import ChildPageBlock

child_page = ChildPageBlock(
    id="block_id",
    type="child_page",
    child_page={
        "title": "Subpage Title"
    },
    # ... base fields
)
```

### ChildDatabaseBlock

```python
from notion_py_client import ChildDatabaseBlock

child_db = ChildDatabaseBlock(
    id="block_id",
    type="child_database",
    child_database={
        "title": "Database Title"
    },
    # ... base fields
)
```

## Media Blocks

### ImageBlock

```python
from notion_py_client import ImageBlock

image = ImageBlock(
    id="block_id",
    type="image",
    image={
        "type": "external",
        "external": {"url": "https://example.com/image.png"},
        "caption": []
    },
    # ... base fields
)
```

### VideoBlock

```python
from notion_py_client import VideoBlock

video = VideoBlock(
    id="block_id",
    type="video",
    video={
        "type": "external",
        "external": {"url": "https://youtube.com/watch?v=..."},
        "caption": []
    },
    # ... base fields
)
```

### FileBlock

```python
from notion_py_client import FileBlock

file = FileBlock(
    id="block_id",
    type="file",
    file={
        "type": "external",
        "external": {"url": "https://example.com/document.pdf"},
        "caption": []
    },
    # ... base fields
)
```

### BookmarkBlock

```python
from notion_py_client import BookmarkBlock

bookmark = BookmarkBlock(
    id="block_id",
    type="bookmark",
    bookmark={
        "url": "https://example.com",
        "caption": []
    },
    # ... base fields
)
```

### EmbedBlock

```python
from notion_py_client import EmbedBlock

embed = EmbedBlock(
    id="block_id",
    type="embed",
    embed={
        "url": "https://example.com/embed"
    },
    # ... base fields
)
```

## Layout Blocks

### DividerBlock

```python
from notion_py_client import DividerBlock

divider = DividerBlock(
    id="block_id",
    type="divider",
    divider={},
    # ... base fields
)
```

### TableOfContentsBlock

```python
from notion_py_client import TableOfContentsBlock

toc = TableOfContentsBlock(
    id="block_id",
    type="table_of_contents",
    table_of_contents={
        "color": "default"
    },
    # ... base fields
)
```

### BreadcrumbBlock

```python
from notion_py_client import BreadcrumbBlock

breadcrumb = BreadcrumbBlock(
    id="block_id",
    type="breadcrumb",
    breadcrumb={},
    # ... base fields
)
```

### ColumnListBlock & ColumnBlock

```python
from notion_py_client import ColumnListBlock, ColumnBlock

column_list = ColumnListBlock(
    id="block_id",
    type="column_list",
    column_list={},
    has_children=True,
    # ... base fields
)

column = ColumnBlock(
    id="block_id",
    type="column",
    column={},
    parent={"type": "block_id", "block_id": "column_list_id"},
    # ... base fields
)
```

### TableBlock & TableRowBlock

```python
from notion_py_client import TableBlock, TableRowBlock

table = TableBlock(
    id="block_id",
    type="table",
    table={
        "table_width": 3,
        "has_column_header": True,
        "has_row_header": False
    },
    has_children=True,
    # ... base fields
)

table_row = TableRowBlock(
    id="block_id",
    type="table_row",
    table_row={
        "cells": [
            [{"type": "text", "text": {"content": "Cell 1"}}],
            [{"type": "text", "text": {"content": "Cell 2"}}],
            [{"type": "text", "text": {"content": "Cell 3"}}]
        ]
    },
    # ... base fields
)
```

## Block Colors

Available colors for text blocks:

```python
from notion_py_client.blocks.base import ApiColor

# Text colors
ApiColor.DEFAULT
ApiColor.GRAY
ApiColor.BROWN
ApiColor.ORANGE
ApiColor.YELLOW
ApiColor.GREEN
ApiColor.BLUE
ApiColor.PURPLE
ApiColor.PINK
ApiColor.RED

# Background colors
ApiColor.DEFAULT_BACKGROUND
ApiColor.GRAY_BACKGROUND
ApiColor.BROWN_BACKGROUND
ApiColor.ORANGE_BACKGROUND
ApiColor.YELLOW_BACKGROUND
ApiColor.GREEN_BACKGROUND
ApiColor.BLUE_BACKGROUND
ApiColor.PURPLE_BACKGROUND
ApiColor.PINK_BACKGROUND
ApiColor.RED_BACKGROUND
```

## Union Types

### BlockObject

Union of all block types:

```python
from notion_py_client import BlockObject

# Can be any block type
block: BlockObject = ...

# Type narrowing
if block.type == "paragraph":
    # block is ParagraphBlock
    text = block.paragraph.rich_text[0].plain_text
elif block.type == "code":
    # block is CodeBlock
    language = block.code.language
```

### PartialBlock

Minimal block representation (without type-specific content):

```python
from notion_py_client import PartialBlock

partial: PartialBlock = {
    "object": "block",
    "id": "block_id",
    "type": "paragraph",
    "created_time": "2025-01-01T00:00:00.000Z",
    # ... no paragraph field
}
```

## Related

- [Blocks API](../api/blocks.md) - Block operations
- [Rich Text](#) - Text formatting reference
- [Type Reference](index.md) - Overview
