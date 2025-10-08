# Type Reference

notion-py-client provides a complete type system for the Notion API built with Pydantic v2.

## Core Principles

### Enum + Literal Pattern

All type discriminators follow this pattern:

```python
from enum import Enum
from typing import Literal
from pydantic import BaseModel, Field

# Base class uses Enum
class BlockType(str, Enum):
    PARAGRAPH = "paragraph"
    HEADING_1 = "heading_1"

class BaseBlockObject(BaseModel):
    type: BlockType = Field(...)  # Enum

# Subclass overrides with Literal
class ParagraphBlock(BaseBlockObject):
    type: Literal[BlockType.PARAGRAPH] = BlockType.PARAGRAPH
    paragraph: ParagraphBlockContent

class Heading1Block(BaseBlockObject):
    type: Literal[BlockType.HEADING_1] = BlockType.HEADING_1
    heading_1: Heading1BlockContent
```

This pattern ensures:

- Type safety at runtime
- IDE autocomplete support
- Discriminated unions work correctly

### Strict Typing

All models use Pydantic's strict types:

```python
from pydantic import StrictStr, StrictInt, StrictBool

class Example(BaseModel):
    name: StrictStr      # Not str
    count: StrictInt     # Not int
    active: StrictBool   # Not bool
```

This prevents implicit type coercion and catches validation errors early.

## Type Categories

### Response Types

Located in `notion_py.responses`:

- `NotionPage` - Full page object with properties
- `PartialPage` - Page without properties (e.g., in search results)
- `NotionDatabase` - Database container with data sources
- `PartialDatabase` - Database without full details
- `DataSource` - Data source with schema (properties)
- `PartialDataSource` - Data source without schema

### Request Types

Located in `notion_py.requests`:

- `CreatePageParameters` - Page creation parameters
- `UpdatePageParameters` - Page update parameters
- `CreateDatabaseParameters` - Database creation
- `UpdateDatabaseParameters` - Database update

### Property Types

Located in `notion_py.responses.property_types`:

- `TitleProperty` - Title property value
- `RichTextProperty` - Rich text value
- `NumberProperty` - Numeric value
- `SelectProperty` - Select option
- `MultiSelectProperty` - Multiple select options
- `DateProperty` - Date or date range
- `PeopleProperty` - User references
- `FilesProperty` - File attachments
- `CheckboxProperty` - Boolean value
- `UrlProperty` - URL string
- `EmailProperty` - Email address
- `PhoneNumberProperty` - Phone number
- `FormulaProperty` - Computed value (read-only)
- `RelationProperty` - Page relations
- `RollupProperty` - Aggregated values (read-only)
- `CreatedTimeProperty` - Creation timestamp (read-only)
- `CreatedByProperty` - Creator (read-only)
- `LastEditedTimeProperty` - Last edit timestamp (read-only)
- `LastEditedByProperty` - Last editor (read-only)
- `StatusProperty` - Status value
- `UniqueIdProperty` - Unique identifier (read-only)
- `VerificationProperty` - Verification state (read-only)

### Property Requests

Located in `notion_py.requests.property_requests`:

- `TitlePropertyRequest`
- `RichTextPropertyRequest`
- `NumberPropertyRequest`
- `SelectPropertyRequest`
- `MultiSelectPropertyRequest`
- `DatePropertyRequest`
- `PeoplePropertyRequest`
- `FilesPropertyRequest`
- `CheckboxPropertyRequest`
- `UrlPropertyRequest`
- `EmailPropertyRequest`
- `PhoneNumberPropertyRequest`
- `RelationPropertyRequest`
- `StatusPropertyRequest`

### Block Types

Located in `notion_py.blocks`:

#### Text Blocks

- `ParagraphBlock`
- `Heading1Block`, `Heading2Block`, `Heading3Block`
- `BulletedListItemBlock`, `NumberedListItemBlock`
- `QuoteBlock`
- `ToDoBlock`
- `ToggleBlock`
- `TemplateBlock`

#### Special Blocks

- `SyncedBlockBlock`
- `ChildPageBlock`, `ChildDatabaseBlock`
- `EquationBlock`
- `CodeBlock`
- `CalloutBlock`

#### Layout Blocks

- `DividerBlock`
- `BreadcrumbBlock`
- `TableOfContentsBlock`
- `ColumnListBlock`, `ColumnBlock`
- `LinkToPageBlock`
- `TableBlock`, `TableRowBlock`

#### Media Blocks

- `EmbedBlock`
- `BookmarkBlock`
- `ImageBlock`
- `VideoBlock`
- `PdfBlock`
- `FileBlock`
- `AudioBlock`
- `LinkPreviewBlock`

#### Other

- `UnsupportedBlock`

### Filter Types

Located in `notion_py.filters`:

- `TextPropertyFilter` - Text/rich text filtering
- `NumberPropertyFilter` - Numeric filtering
- `CheckboxPropertyFilter` - Boolean filtering
- `SelectPropertyFilter` - Select option filtering
- `MultiSelectPropertyFilter` - Multi-select filtering
- `StatusPropertyFilter` - Status filtering
- `DatePropertyFilter` - Date filtering
- `PeoplePropertyFilter` - People filtering
- `FilesPropertyFilter` - Files filtering
- `RelationPropertyFilter` - Relation filtering
- `FormulaPropertyFilter` - Formula filtering
- `RollupPropertyFilter` - Rollup filtering
- `CompoundFilter` - AND/OR combinations
- `TimestampFilter` - created_time/last_edited_time filtering

### Model Types

Located in `notion_py.models`:

- `NotionIcon` - Icon configurations (emoji, file, external)
- `NotionCover` - Cover image configurations
- `PartialUser` - User reference
- `NotionParent` - Parent reference (page, database, workspace, block)
- `RichTextItem` - Rich text element with annotations
- `SelectOption` - Select option configuration
- `StatusOption` - Status option configuration
- `FileObject` - File reference
- `DateInfo` - Date or date range
- `FormulaResult` - Formula computation result
- `UniqueId` - Unique ID value
- `Verification` - Verification state

## Usage Examples

### Import Types

```python
# Response types
from notion_py_client import (
    NotionPage,
    NotionDatabase,
    DataSource,
)

# Request types
from notion_py_client.requests.page_requests import (
    CreatePageParameters,
    UpdatePageParameters,
)
from notion_py_client.requests.property_requests import (
    TitlePropertyRequest,
    StatusPropertyRequest,
)

# Filters
from notion_py_client.filters import (
    TextPropertyFilter,
    CompoundFilter,
)

# Blocks
from notion_py_client import (
    ParagraphBlock,
    Heading1Block,
)
```

### Type Guards

```python
from notion_py_client import NotionPage

async with NotionAsyncClient(auth="secret_xxx") as client:
    page = await client.pages.retrieve({"page_id": "page_id"})

    # Check property type
    name_prop = page.properties["Name"]
    if name_prop.type == "title":
        # TypeScript-style type narrowing
        title = name_prop.title[0].plain_text if name_prop.title else ""
```

### Model Validation

```python
from notion_py_client import NotionPage
from pydantic import ValidationError

try:
    # Validate API response
    page = NotionPage(**api_response)
except ValidationError as e:
    print(f"Invalid response: {e}")
```

### Serialization

```python
from notion_py_client.requests.page_requests import CreatePageParameters

params = CreatePageParameters(
    parent={"type": "database_id", "database_id": "db_id"},
    properties={...}
)

# Convert to dict for API request
data = params.model_dump(by_alias=True, exclude_none=True)

# Convert to JSON
json_str = params.model_dump_json(by_alias=True, exclude_none=True)
```

## Related

- [Blocks](blocks.md) - Block type details
- [Properties](properties.md) - Property type details
- [Filters](filters.md) - Filter type details
- [Requests](requests.md) - Request type details
