# Type Reference

notion-py-client provides a complete type system for the Notion API built with Pydantic v2.

## Core Principles

### String Literal Types

All type discriminators use string literals for natural type checking:

```python
from typing import Literal
from pydantic import BaseModel, Field

# Type is a union of all possible string literals
NotionPropertyType = Literal[
    "title",
    "rich_text",
    "number",
    "select",
    "multi_select",
    "date",
    "people",
    "files",
    "checkbox",
    "url",
    "email",
    "phone_number",
    "formula",
    "relation",
    "rollup",
    "created_time",
    "created_by",
    "last_edited_time",
    "last_edited_by",
    "status",
    # ... and more
]

class BaseProperty(BaseModel):
    id: str
    type: NotionPropertyType

# Subclass uses specific string literal
class TitleProperty(BaseProperty):
    type: Literal["title"] = "title"
    title: list[RichTextItem]

class NumberProperty(BaseProperty):
    type: Literal["number"] = "number"
    number: int | float | None
```

This pattern enables:

- **Natural string comparison**: `if property.type == "title":`
- **No Enum imports needed**: Direct string literals
- **IDE autocomplete**: Type hints work seamlessly
- **TypeScript SDK alignment**: Matches official Notion API patterns

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

Located in `notion_py_client.filters`:

- `PropertyFilter` - Union of all property filters (TypedDict)
- `TimestampFilter` - created_time / last_edited_time (TypedDict)
- `FilterCondition` - `PropertyFilter | TimestampFilter | {and: [...] } | {or: [...]}`
- Helpers: `create_and_filter`, `create_or_filter`

Common concrete filter dict shapes:

- `Text (rich_text)`: `{ "property": "Name", "rich_text": {"contains": "..."} }`
- `Number`: `{ "property": "Score", "number": {"greater_than": 80} }`
- `Select`: `{ "property": "Priority", "select": {"equals": "High"} }`
- `Multi-select`: `{ "property": "Tags", "multi_select": {"contains": "Important"} }`
- `Status`: `{ "property": "Status", "status": {"does_not_equal": "Done"} }`
- `Date`: `{ "property": "Due", "date": {"on_or_after": "2025-01-01"} }`
- `People`: `{ "property": "Assignee", "people": {"is_not_empty": True} }`

Use helpers to combine:

```python
from notion_py_client.filters import create_and_filter

filter_dict = create_and_filter(
    {"property": "Status", "status": {"equals": "In Progress"}},
    {"timestamp": "created_time", "created_time": {"past_week": {}}},
)
```

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
    FilterCondition,
    create_and_filter,
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

    # Check property type with string literal
    name_prop = page.properties["Name"]
    if name_prop.type == "title":
        # Type narrowing works automatically
        title = name_prop.title[0].plain_text if name_prop.title else ""

    # Multiple type checks
    status_prop = page.properties.get("Status")
    if status_prop and status_prop.type == "status":
        current_status = status_prop.status.name if status_prop.status else None

    # Pattern matching (Python 3.10+)
    match page.properties["Priority"].type:
        case "select":
            priority = page.properties["Priority"].select.name
        case "multi_select":
            tags = [opt.name for opt in page.properties["Priority"].multi_select]
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
