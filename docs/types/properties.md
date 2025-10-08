# Property Types

Complete reference for all Notion property types.

## Property Type Hierarchy

Properties come in two forms:

1. **Property values** (from pages) - Located in `notion_py.responses.property_types`
2. **Property requests** (for updates) - Located in `notion_py.requests.property_requests`

## Property Values

### TitleProperty

```python
from notion_py_client.responses.property_types import TitleProperty

property: TitleProperty = {
    "id": "title",
    "type": "title",
    "title": [
        {
            "type": "text",
            "text": {"content": "Page Title"},
            "plain_text": "Page Title"
        }
    ]
}

# Access value
title = property.title[0].plain_text if property.title else ""
```

### RichTextProperty

```python
from notion_py_client.responses.property_types import RichTextProperty

property: RichTextProperty = {
    "id": "abc123",
    "type": "rich_text",
    "rich_text": [
        {
            "type": "text",
            "text": {"content": "Some text"},
            "plain_text": "Some text",
            "annotations": {
                "bold": False,
                "italic": False,
                "strikethrough": False,
                "underline": False,
                "code": False,
                "color": "default"
            }
        }
    ]
}

# Access value
text = property.rich_text[0].plain_text if property.rich_text else ""
```

### NumberProperty

```python
from notion_py_client.responses.property_types import NumberProperty

property: NumberProperty = {
    "id": "abc123",
    "type": "number",
    "number": 42.5
}

# Access value
value = property.number or 0
```

### SelectProperty

```python
from notion_py_client.responses.property_types import SelectProperty

property: SelectProperty = {
    "id": "abc123",
    "type": "select",
    "select": {
        "id": "option_id",
        "name": "In Progress",
        "color": "blue"
    }
}

# Access value
status = property.select.name if property.select else None
```

### MultiSelectProperty

```python
from notion_py_client.responses.property_types import MultiSelectProperty

property: MultiSelectProperty = {
    "id": "abc123",
    "type": "multi_select",
    "multi_select": [
        {"id": "opt1", "name": "Tag 1", "color": "red"},
        {"id": "opt2", "name": "Tag 2", "color": "blue"}
    ]
}

# Access values
tags = [opt.name for opt in property.multi_select]
```

### DateProperty

```python
from notion_py_client.responses.property_types import DateProperty

# Single date
property: DateProperty = {
    "id": "abc123",
    "type": "date",
    "date": {
        "start": "2025-01-01",
        "end": None,
        "time_zone": None
    }
}

# Date range
property: DateProperty = {
    "id": "abc123",
    "type": "date",
    "date": {
        "start": "2025-01-01",
        "end": "2025-01-31",
        "time_zone": None
    }
}

# Access value
start_date = property.date.start if property.date else None
```

### PeopleProperty

```python
from notion_py_client.responses.property_types import PeopleProperty

property: PeopleProperty = {
    "id": "abc123",
    "type": "people",
    "people": [
        {
            "object": "user",
            "id": "user_id",
            "type": "person",
            "name": "John Doe",
            "avatar_url": "https://..."
        }
    ]
}

# Access values
assignees = [person.name for person in property.people]
```

### FilesProperty

```python
from notion_py_client.responses.property_types import FilesProperty

property: FilesProperty = {
    "id": "abc123",
    "type": "files",
    "files": [
        {
            "name": "document.pdf",
            "type": "external",
            "external": {"url": "https://example.com/doc.pdf"}
        }
    ]
}

# Access values
file_urls = [f.external.url for f in property.files if f.type == "external"]
```

### CheckboxProperty

```python
from notion_py_client.responses.property_types import CheckboxProperty

property: CheckboxProperty = {
    "id": "abc123",
    "type": "checkbox",
    "checkbox": True
}

# Access value
is_done = property.checkbox
```

### UrlProperty

```python
from notion_py_client.responses.property_types import UrlProperty

property: UrlProperty = {
    "id": "abc123",
    "type": "url",
    "url": "https://example.com"
}

# Access value
url = property.url or ""
```

### EmailProperty

```python
from notion_py_client.responses.property_types import EmailProperty

property: EmailProperty = {
    "id": "abc123",
    "type": "email",
    "email": "user@example.com"
}

# Access value
email = property.email or ""
```

### PhoneNumberProperty

```python
from notion_py_client.responses.property_types import PhoneNumberProperty

property: PhoneNumberProperty = {
    "id": "abc123",
    "type": "phone_number",
    "phone_number": "+1234567890"
}

# Access value
phone = property.phone_number or ""
```

### StatusProperty

```python
from notion_py_client.responses.property_types import StatusProperty

property: StatusProperty = {
    "id": "abc123",
    "type": "status",
    "status": {
        "id": "status_id",
        "name": "In Progress",
        "color": "blue"
    }
}

# Access value
status = property.status.name if property.status else None
```

## Read-Only Properties

### FormulaProperty

```python
from notion_py_client.responses.property_types import FormulaProperty

# Number formula
property: FormulaProperty = {
    "id": "abc123",
    "type": "formula",
    "formula": {
        "type": "number",
        "number": 42.5
    }
}

# String formula
property: FormulaProperty = {
    "id": "abc123",
    "type": "formula",
    "formula": {
        "type": "string",
        "string": "Result text"
    }
}

# Boolean formula
property: FormulaProperty = {
    "id": "abc123",
    "type": "formula",
    "formula": {
        "type": "boolean",
        "boolean": True
    }
}

# Date formula
property: FormulaProperty = {
    "id": "abc123",
    "type": "formula",
    "formula": {
        "type": "date",
        "date": {"start": "2025-01-01", "end": None}
    }
}

# Access value (type guard required)
if property.formula.type == "number":
    value = property.formula.number or 0
elif property.formula.type == "string":
    value = property.formula.string or ""
```

### RelationProperty

```python
from notion_py_client.responses.property_types import RelationProperty

property: RelationProperty = {
    "id": "abc123",
    "type": "relation",
    "relation": [
        {"id": "page_id_1"},
        {"id": "page_id_2"}
    ],
    "has_more": False
}

# Access values
related_ids = [item.id for item in property.relation]
```

### RollupProperty

```python
from notion_py_client.responses.property_types import RollupProperty

# Number rollup
property: RollupProperty = {
    "id": "abc123",
    "type": "rollup",
    "rollup": {
        "type": "number",
        "number": 100.0,
        "function": "sum"
    }
}

# Array rollup
property: RollupProperty = {
    "id": "abc123",
    "type": "rollup",
    "rollup": {
        "type": "array",
        "array": [
            {"type": "number", "number": 10},
            {"type": "number", "number": 20}
        ],
        "function": "show_original"
    }
}

# Access value (type guard required)
if property.rollup.type == "number":
    total = property.rollup.number or 0
```

### CreatedTimeProperty

```python
from notion_py_client.responses.property_types import CreatedTimeProperty

property: CreatedTimeProperty = {
    "id": "abc123",
    "type": "created_time",
    "created_time": "2025-01-01T00:00:00.000Z"
}

# Access value
created = property.created_time
```

### CreatedByProperty

```python
from notion_py_client.responses.property_types import CreatedByProperty

property: CreatedByProperty = {
    "id": "abc123",
    "type": "created_by",
    "created_by": {
        "object": "user",
        "id": "user_id",
        "name": "John Doe"
    }
}

# Access value
creator = property.created_by.name
```

### LastEditedTimeProperty

```python
from notion_py_client.responses.property_types import LastEditedTimeProperty

property: LastEditedTimeProperty = {
    "id": "abc123",
    "type": "last_edited_time",
    "last_edited_time": "2025-01-02T00:00:00.000Z"
}

# Access value
edited = property.last_edited_time
```

### LastEditedByProperty

```python
from notion_py_client.responses.property_types import LastEditedByProperty

property: LastEditedByProperty = {
    "id": "abc123",
    "type": "last_edited_by",
    "last_edited_by": {
        "object": "user",
        "id": "user_id",
        "name": "Jane Doe"
    }
}

# Access value
editor = property.last_edited_by.name
```

### UniqueIdProperty

```python
from notion_py_client.responses.property_types import UniqueIdProperty

property: UniqueIdProperty = {
    "id": "abc123",
    "type": "unique_id",
    "unique_id": {
        "number": 42,
        "prefix": "TASK"
    }
}

# Access value
uid = f"{property.unique_id.prefix}-{property.unique_id.number}"
```

### VerificationProperty

```python
from notion_py_client.responses.property_types import VerificationProperty

property: VerificationProperty = {
    "id": "abc123",
    "type": "verification",
    "verification": {
        "state": "verified",
        "verified_by": {...},
        "date": {...}
    }
}

# Access value
is_verified = property.verification.state == "verified" if property.verification else False
```

## Property Requests

See [Request Types](requests.md) for property request definitions.

## Related

- [Pages API](../api/pages.md) - Using properties
- [Request Types](requests.md) - Property request types
- [Type Reference](index.md) - Overview
