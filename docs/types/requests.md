# Request Types

Complete reference for request parameter types.

## Page Requests

### CreatePageParameters

Create a new page in a database or as a child page.

```python
from notion_py_client.requests.page_requests import CreatePageParameters
from notion_py_client.requests.property_requests import (
    TitlePropertyRequest,
    StatusPropertyRequest,
)

# Create in database
params = CreatePageParameters(
    parent={
        "type": "database_id",
        "database_id": "db_abc123"
    },
    properties={
        "Name": TitlePropertyRequest(
            title=[{"type": "text", "text": {"content": "New Page"}}]
        ),
        "Status": StatusPropertyRequest(
            status={"name": "In Progress"}
        ),
    },
    icon={
        "type": "emoji",
        "emoji": "📝"
    },
    cover={
        "type": "external",
        "external": {"url": "https://example.com/cover.jpg"}
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

# Create as child page
params = CreatePageParameters(
    parent={
        "type": "page_id",
        "page_id": "parent_page_id"
    },
    properties={
        "title": TitlePropertyRequest(
            title=[{"type": "text", "text": {"content": "Subpage"}}]
        )
    }
)
```

### UpdatePageParameters

Update an existing page.

```python
from notion_py_client.requests.page_requests import UpdatePageParameters

params = UpdatePageParameters(
    page_id="page_abc123",
    properties={
        "Status": StatusPropertyRequest(
            status={"name": "Done"}
        ),
        "Priority": SelectPropertyRequest(
            select={"name": "High"}
        ),
    },
    icon={
        "type": "emoji",
        "emoji": "✅"
    },
    cover=None,  # Remove cover
    archived=False
)

# Archive page
params = UpdatePageParameters(
    page_id="page_abc123",
    archived=True
)
```

## Property Requests

All property request types are located in `notion_py.requests.property_requests`.

### TitlePropertyRequest

```python
from notion_py_client.requests.property_requests import TitlePropertyRequest

request = TitlePropertyRequest(
    title=[
        {"type": "text", "text": {"content": "Page Title"}}
    ]
)

# With formatting
request = TitlePropertyRequest(
    title=[
        {
            "type": "text",
            "text": {"content": "Bold Title"},
            "annotations": {"bold": True}
        }
    ]
)
```

### RichTextPropertyRequest

```python
from notion_py_client.requests.property_requests import RichTextPropertyRequest

request = RichTextPropertyRequest(
    rich_text=[
        {"type": "text", "text": {"content": "Some text"}}
    ]
)

# With multiple styles
request = RichTextPropertyRequest(
    rich_text=[
        {
            "type": "text",
            "text": {"content": "Normal "},
        },
        {
            "type": "text",
            "text": {"content": "bold "},
            "annotations": {"bold": True}
        },
        {
            "type": "text",
            "text": {"content": "italic"},
            "annotations": {"italic": True}
        }
    ]
)
```

### NumberPropertyRequest

```python
from notion_py_client.requests.property_requests import NumberPropertyRequest

request = NumberPropertyRequest(number=42.5)

# Clear value
request = NumberPropertyRequest(number=None)
```

### SelectPropertyRequest

```python
from notion_py_client.requests.property_requests import SelectPropertyRequest

request = SelectPropertyRequest(
    select={"name": "Option Name"}
)

# Clear value
request = SelectPropertyRequest(select=None)
```

### MultiSelectPropertyRequest

```python
from notion_py_client.requests.property_requests import MultiSelectPropertyRequest

request = MultiSelectPropertyRequest(
    multi_select=[
        {"name": "Tag 1"},
        {"name": "Tag 2"}
    ]
)

# Clear values
request = MultiSelectPropertyRequest(multi_select=[])
```

### DatePropertyRequest

```python
from notion_py_client.requests.property_requests import DatePropertyRequest

# Single date
request = DatePropertyRequest(
    date={"start": "2025-01-01"}
)

# Date range
request = DatePropertyRequest(
    date={
        "start": "2025-01-01",
        "end": "2025-01-31"
    }
)

# With time
request = DatePropertyRequest(
    date={
        "start": "2025-01-01T09:00:00",
        "time_zone": "America/New_York"
    }
)

# Clear value
request = DatePropertyRequest(date=None)
```

### PeoplePropertyRequest

```python
from notion_py_client.requests.property_requests import PeoplePropertyRequest

request = PeoplePropertyRequest(
    people=[
        {"id": "user_id_1"},
        {"id": "user_id_2"}
    ]
)

# Clear values
request = PeoplePropertyRequest(people=[])
```

### FilesPropertyRequest

```python
from notion_py_client.requests.property_requests import FilesPropertyRequest

request = FilesPropertyRequest(
    files=[
        {
            "name": "document.pdf",
            "type": "external",
            "external": {"url": "https://example.com/doc.pdf"}
        }
    ]
)

# Clear values
request = FilesPropertyRequest(files=[])
```

### CheckboxPropertyRequest

```python
from notion_py_client.requests.property_requests import CheckboxPropertyRequest

# Check
request = CheckboxPropertyRequest(checkbox=True)

# Uncheck
request = CheckboxPropertyRequest(checkbox=False)
```

### UrlPropertyRequest

```python
from notion_py_client.requests.property_requests import UrlPropertyRequest

request = UrlPropertyRequest(url="https://example.com")

# Clear value
request = UrlPropertyRequest(url=None)
```

### EmailPropertyRequest

```python
from notion_py_client.requests.property_requests import EmailPropertyRequest

request = EmailPropertyRequest(email="user@example.com")

# Clear value
request = EmailPropertyRequest(email=None)
```

### PhoneNumberPropertyRequest

```python
from notion_py_client.requests.property_requests import PhoneNumberPropertyRequest

request = PhoneNumberPropertyRequest(phone_number="+1234567890")

# Clear value
request = PhoneNumberPropertyRequest(phone_number=None)
```

### RelationPropertyRequest

```python
from notion_py_client.requests.property_requests import RelationPropertyRequest

request = RelationPropertyRequest(
    relation=[
        {"id": "page_id_1"},
        {"id": "page_id_2"}
    ]
)

# Clear values
request = RelationPropertyRequest(relation=[])
```

### StatusPropertyRequest

```python
from notion_py_client.requests.property_requests import StatusPropertyRequest

request = StatusPropertyRequest(
    status={"name": "In Progress"}
)

# Clear value (if allowed by database)
request = StatusPropertyRequest(status=None)
```

## Database Requests

### CreateDatabaseParameters

```python
from notion_py_client.api_types import CreateDatabaseParameters

params: CreateDatabaseParameters = {
    "parent": {
        "type": "page_id",
        "page_id": "parent_page_id"
    },
    "title": [
        {"type": "text", "text": {"content": "New Database"}}
    ],
    "initial_data_source": {
        "name": "Main Data",
        "properties": {
            "Name": {"title": {}},
            "Status": {
                "select": {
                    "options": [
                        {"name": "Todo", "color": "gray"},
                        {"name": "Done", "color": "green"}
                    ]
                }
            }
        }
    },
    "icon": {
        "type": "emoji",
        "emoji": "📊"
    }
}
```

### UpdateDatabaseParameters

```python
from notion_py_client.api_types import UpdateDatabaseParameters

params: UpdateDatabaseParameters = {
    "database_id": "db_abc123",
    "title": [
        {"type": "text", "text": {"content": "Updated Title"}}
    ],
    "icon": {
        "type": "emoji",
        "emoji": "📈"
    }
}
```

## Common Patterns

### Building Requests Dynamically

```python
from notion_py_client.requests.page_requests import CreatePageParameters
from notion_py_client.requests.property_requests import PropertyRequest

def build_task_create_request(
    database_id: str,
    title: str,
    status: str,
    priority: str | None = None
) -> CreatePageParameters:
    properties: dict[str, PropertyRequest] = {
        "Name": TitlePropertyRequest(
            title=[{"type": "text", "text": {"content": title}}]
        ),
        "Status": StatusPropertyRequest(
            status={"name": status}
        ),
    }

    if priority:
        properties["Priority"] = SelectPropertyRequest(
            select={"name": priority}
        )

    return CreatePageParameters(
        parent={"type": "database_id", "database_id": database_id},
        properties=properties
    )
```

### Partial Updates

```python
from notion_py_client.requests.page_requests import UpdatePageParameters

# Only update specific properties
params = UpdatePageParameters(
    page_id="page_abc123",
    properties={
        "Status": StatusPropertyRequest(status={"name": "Done"})
        # Other properties remain unchanged
    }
)
```

### Clearing Values

```python
# Clear different property types
params = UpdatePageParameters(
    page_id="page_abc123",
    properties={
        "Number": NumberPropertyRequest(number=None),
        "Select": SelectPropertyRequest(select=None),
        "Multi-select": MultiSelectPropertyRequest(multi_select=[]),
        "Date": DatePropertyRequest(date=None),
        "People": PeoplePropertyRequest(people=[]),
        "Files": FilesPropertyRequest(files=[]),
        "Url": UrlPropertyRequest(url=None),
        "Email": EmailPropertyRequest(email=None),
        "Phone": PhoneNumberPropertyRequest(phone_number=None),
        "Relation": RelationPropertyRequest(relation=[]),
    }
)
```

## Serialization

Convert requests to API format:

```python
from notion_py_client.requests.page_requests import CreatePageParameters

params = CreatePageParameters(...)

# Convert to dict for API
data = params.model_dump(by_alias=True, exclude_none=True)

# Use in client
page = await client.pages.create(params)
```

## Related

- [Pages API](../api/pages.md) - Page operations
- [Property Types](properties.md) - Property value types
- [Type Reference](index.md) - Overview
