# Pages API

Create, retrieve, and update Notion pages.

## Overview

The Pages API provides methods to:

- Create new pages in databases or as child pages
- Retrieve page content and properties
- Update page properties and content
- Access individual property values

## Methods

### create

Create a new page.

```python
async def create(
    params: CreatePageParameters,
    *,
    auth: AuthParam | None = None
) -> NotionPage
```

**Parameters**:

- `params.parent`: Parent database or page
- `params.properties`: Page properties
- `params.icon` (optional): Page icon
- `params.cover` (optional): Cover image
- `params.children` (optional): Child blocks

**Returns**: Created `NotionPage`

**Example**:

```python
from notion_py_client import NotionAsyncClient
from notion_py_client.requests.page_requests import CreatePageParameters
from notion_py_client.requests.property_requests import (
    TitlePropertyRequest,
    StatusPropertyRequest,
    DatePropertyRequest,
)

async with NotionAsyncClient(auth="secret_xxx") as client:
    # Create in database
    params = CreatePageParameters(
        parent={
            "type": "database_id",
            "database_id": "db_abc123"
        },
        properties={
            "Name": TitlePropertyRequest(
                title=[
                    {"type": "text", "text": {"content": "New Task"}}
                ]
            ),
            "Status": StatusPropertyRequest(
                status={"name": "In Progress"}
            ),
            "Due Date": DatePropertyRequest(
                date={"start": "2025-12-31"}
            ),
        },
        icon={
            "type": "emoji",
            "emoji": "📝"
        }
    )

    page = await client.pages.create(params)
    print(f"Created: {page.id}")
```

### retrieve

Retrieve a page.

```python
async def retrieve(
    params: RetrievePageParameters,
    *,
    auth: AuthParam | None = None
) -> NotionPage
```

**Parameters**:

- `params.page_id` (str): Page ID
- `params.filter_properties` (optional): Property IDs to include

**Returns**: `NotionPage` with all properties

**Example**:

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    page = await client.pages.retrieve(
        {"page_id": "page_abc123"}
    )

    # Access properties
    title_prop = page.properties.get("Name")
    if title_prop and title_prop.type == "title":
        title = title_prop.title[0].plain_text if title_prop.title else ""
        print(f"Title: {title}")

    status_prop = page.properties.get("Status")
    if status_prop and status_prop.type == "status":
        print(f"Status: {status_prop.status.name}")
```

### update

Update a page.

```python
async def update(
    params: UpdatePageParameters,
    *,
    auth: AuthParam | None = None
) -> NotionPage
```

**Parameters**:

- `params.page_id` (str): Page ID
- `params.properties` (optional): Properties to update
- `params.icon` (optional): New icon
- `params.cover` (optional): New cover
- `params.archived` (optional): Archive status

**Returns**: Updated `NotionPage`

**Example**:

```python
from notion_py_client.requests.page_requests import UpdatePageParameters

async with NotionAsyncClient(auth="secret_xxx") as client:
    params = UpdatePageParameters(
        page_id="page_abc123",
        properties={
            "Status": StatusPropertyRequest(
                status={"name": "Done"}
            ),
        }
    )

    page = await client.pages.update(params)
    print(f"Updated: {page.id}")
```

### properties.retrieve

Retrieve a specific property value (useful for paginated properties like relations).

```python
async def properties.retrieve(
    *,
    page_id: str,
    property_id: str,
    start_cursor: str | None = None,
    page_size: int | None = None,
    auth: AuthParam | None = None
) -> dict[str, Any]
```

**Parameters**:

- `page_id` (str): Page ID
- `property_id` (str): Property ID
- `start_cursor` (optional): Pagination cursor
- `page_size` (optional): Results per page

**Returns**: Property item object

**Example**:

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    # Get property ID from page
    page = await client.pages.retrieve({"page_id": "page_abc123"})
    relation_prop_id = page.properties["Related Items"].id

    # Retrieve paginated property
    prop_value = await client.pages.properties.retrieve(
        page_id="page_abc123",
        property_id=relation_prop_id
    )
```

## Property Requests

### Using Type-Safe Requests

```python
from notion_py_client.requests.property_requests import (
    TitlePropertyRequest,
    RichTextPropertyRequest,
    NumberPropertyRequest,
    SelectPropertyRequest,
    MultiSelectPropertyRequest,
    DatePropertyRequest,
    PeoplePropertyRequest,
    FilesPropertyRequest,
    CheckboxPropertyRequest,
    UrlPropertyRequest,
    EmailPropertyRequest,
    PhoneNumberPropertyRequest,
    RelationPropertyRequest,
    StatusPropertyRequest,
)

properties = {
    # Title
    "Name": TitlePropertyRequest(
        title=[{"type": "text", "text": {"content": "Task Name"}}]
    ),

    # Rich Text
    "Description": RichTextPropertyRequest(
        rich_text=[
            {"type": "text", "text": {"content": "Description here"}}
        ]
    ),

    # Number
    "Price": NumberPropertyRequest(number=99.99),

    # Select
    "Priority": SelectPropertyRequest(select={"name": "High"}),

    # Multi-select
    "Tags": MultiSelectPropertyRequest(
        multi_select=[
            {"name": "Important"},
            {"name": "Review"}
        ]
    ),

    # Date
    "Due": DatePropertyRequest(
        date={"start": "2025-12-31", "end": "2026-01-01"}
    ),

    # People
    "Assignee": PeoplePropertyRequest(
        people=[{"id": "user_abc123"}]
    ),

    # Files
    "Attachments": FilesPropertyRequest(
        files=[
            {"name": "file.pdf", "url": "https://..."}
        ]
    ),

    # Checkbox
    "Done": CheckboxPropertyRequest(checkbox=True),

    # URL
    "Website": UrlPropertyRequest(url="https://example.com"),

    # Email
    "Contact": EmailPropertyRequest(email="user@example.com"),

    # Phone
    "Phone": PhoneNumberPropertyRequest(phone_number="+1234567890"),

    # Relation
    "Related": RelationPropertyRequest(
        relation=[{"id": "page_def456"}]
    ),

    # Status
    "Status": StatusPropertyRequest(status={"name": "In Progress"}),
}
```

### Reading Properties

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    page = await client.pages.retrieve({"page_id": "page_abc123"})

    # Title property
    if page.properties["Name"].type == "title":
        title = page.properties["Name"].title[0].plain_text

    # Number property
    if page.properties["Price"].type == "number":
        price = page.properties["Price"].number

    # Select property
    if page.properties["Status"].type == "select":
        status = page.properties["Status"].select.name

    # Date property
    if page.properties["Due Date"].type == "date":
        due = page.properties["Due Date"].date.start

    # People property
    if page.properties["Assignee"].type == "people":
        assignees = [p.name for p in page.properties["Assignee"].people]

    # Formula (read-only)
    if page.properties["Calculated"].type == "formula":
        if page.properties["Calculated"].formula.type == "number":
            value = page.properties["Calculated"].formula.number
```

## Creating Child Pages

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    # Create as child of another page
    params = CreatePageParameters(
        parent={
            "type": "page_id",
            "page_id": "parent_page_id"
        },
        properties={
            "title": TitlePropertyRequest(
                title=[
                    {"type": "text", "text": {"content": "Subpage"}}
                ]
            )
        },
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Content"}}
                    ]
                }
            }
        ]
    )

    page = await client.pages.create(params)
```

## Archiving Pages

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    # Archive a page
    params = UpdatePageParameters(
        page_id="page_abc123",
        archived=True
    )

    page = await client.pages.update(params)
    print(f"Archived: {page.archived}")
```

## Common Patterns

### Bulk Update

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    page_ids = ["page1", "page2", "page3"]

    for page_id in page_ids:
        await client.pages.update(
            UpdatePageParameters(
                page_id=page_id,
                properties={
                    "Status": StatusPropertyRequest(
                        status={"name": "Done"}
                    )
                }
            )
        )
```

### Copy Page Properties

```python
async with NotionAsyncClient(auth="secret_xxx") as client:
    # Read from source
    source = await client.pages.retrieve({"page_id": "source_id"})

    # Extract properties (excluding read-only)
    title = source.properties["Name"].title
    status = source.properties["Status"].status

    # Create duplicate
    params = CreatePageParameters(
        parent={"type": "database_id", "database_id": "db_abc123"},
        properties={
            "Name": TitlePropertyRequest(title=title),
            "Status": StatusPropertyRequest(status={"name": status.name}),
        }
    )

    duplicate = await client.pages.create(params)
```

## Type Reference

```python
from notion_py_client.responses.page import NotionPage

# Page object structure
page: NotionPage = {
    "object": "page",
    "id": "page_abc123",
    "created_time": "2025-01-01T00:00:00.000Z",
    "last_edited_time": "2025-01-02T00:00:00.000Z",
    "created_by": {...},
    "last_edited_by": {...},
    "parent": {...},
    "archived": false,
    "icon": {...},
    "cover": {...},
    "properties": {
        "Name": {
            "id": "title",
            "type": "title",
            "title": [...]
        }
    },
    "url": "https://www.notion.so/...",
    "public_url": null
}
```

## Related

- [Data Sources API](datasources.md) - Query pages from databases
- [Blocks API](blocks.md) - Add content to pages
- [Property Types](../types/properties.md) - Property reference
