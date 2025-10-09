# Filter Types

Complete reference for database query filters.

## Filter Categories

Filters are located in `notion_py_client.filters` and are expressed as
TypedDicts (not Pydantic models). Build them as plain dicts or by using
the helper functions for AND/OR combinations.

- Property filters - Filter by property values
- Compound filters - Combine multiple filters with AND/OR
- Timestamp filters - Filter by created/edited time

## Property Filters

### Text filters (rich_text)

```python
# Contains
filter = {"property": "Name", "rich_text": {"contains": "urgent"}}

# Does not contain
filter = {"property": "Description", "rich_text": {"does_not_contain": "archived"}}

# Equals
filter = {"property": "Title", "rich_text": {"equals": "Exact Match"}}

# Starts/Ends with
filter = {"property": "Name", "rich_text": {"starts_with": "PROJ"}}
filter = {"property": "Name", "rich_text": {"ends_with": "-2025"}}

# Empty/Not empty
filter = {"property": "Description", "rich_text": {"is_empty": True}}
filter = {"property": "Description", "rich_text": {"is_not_empty": True}}
```

### NumberPropertyFilter

Filter number properties.

```python
from typing import TypedDict

# Equals
filter = {"property": "Price", "number": {"equals": 100}}

# Does not equal
filter = {"property": "Quantity", "number": {"does_not_equal": 0}}

# Greater than
filter = {"property": "Score", "number": {"greater_than": 75}}

# Less than
filter = {"property": "Age", "number": {"less_than": 18}}

# Greater than or equal
filter = {"property": "Points", "number": {"greater_than_or_equal_to": 100}}

# Less than or equal
filter = {"property": "Limit", "number": {"less_than_or_equal_to": 50}}

# Is empty
filter = {"property": "Optional Number", "number": {"is_empty": True}}

# Is not empty
filter = {"property": "Required Number", "number": {"is_not_empty": True}}
```

### CheckboxPropertyFilter

Filter checkbox properties.

```python
# Checked
filter = {"property": "Done", "checkbox": {"equals": True}}

# Unchecked
filter = {"property": "Active", "checkbox": {"equals": False}}
```

### SelectPropertyFilter

Filter select properties.

```python
# Equals
filter = {"property": "Priority", "select": {"equals": "High"}}

# Does not equal
filter = {"property": "Priority", "select": {"does_not_equal": "Low"}}

# Is empty
filter = {"property": "Category", "select": {"is_empty": True}}

# Is not empty
filter = {"property": "Category", "select": {"is_not_empty": True}}
```

### MultiSelectPropertyFilter

```python
# Contains
filter = {"property": "Tags", "multi_select": {"contains": "Important"}}

# Does not contain
filter = {"property": "Labels", "multi_select": {"does_not_contain": "Archived"}}

# Is empty
filter = {"property": "Categories", "multi_select": {"is_empty": True}}

# Is not empty
filter = {"property": "Categories", "multi_select": {"is_not_empty": True}}
```

### StatusPropertyFilter

```python
# Equals
filter = {"property": "Status", "status": {"equals": "In Progress"}}

# Does not equal
filter = {"property": "Status", "status": {"does_not_equal": "Done"}}

# Is empty
filter = {"property": "Workflow", "status": {"is_empty": True}}

# Is not empty
filter = {"property": "Workflow", "status": {"is_not_empty": True}}
```

### DatePropertyFilter

```python
# Equals
filter = {"property": "Due Date", "date": {"equals": "2025-01-01"}}

# Before
filter = {"property": "Start Date", "date": {"before": "2025-12-31"}}

# After
filter = {"property": "End Date", "date": {"after": "2025-01-01"}}

# On or before
filter = {"property": "Deadline", "date": {"on_or_before": "2025-06-30"}}

# On or after
filter = {"property": "Launch", "date": {"on_or_after": "2025-07-01"}}

# Past week
filter = {"property": "Created", "date": {"past_week": {}}}

# Past month
filter = {"property": "Updated", "date": {"past_month": {}}}

# Past year
filter = {"property": "Archive Date", "date": {"past_year": {}}}

from notion_py_client.filters import create_and_filter, create_or_filter

# Next week
filter = {"property": "Upcoming",
    date={"next_week": {}}
}

# Next month
filter = {"property": "Future", "date": {"next_month": {}}}

# Next year
filter = {"property": "Long Term", "date": {"next_year": {}}}

# Is empty
filter = {"property": "Optional Date", "date": {"is_empty": True}}

# Is not empty
filter = {"property": "Required Date", "date": {"is_not_empty": True}}
```

## Compound Filters

Use helpers to build AND/OR groups:

```python
from notion_py_client.filters import create_and_filter, create_or_filter

and_filter = create_and_filter(
    {"property": "Status", "status": {"equals": "In Progress"}},
    {"timestamp": "created_time", "created_time": {"past_week": {}}},
)

or_filter = create_or_filter(
    {"property": "Priority", "select": {"equals": "High"}},
    {"property": "Priority", "select": {"equals": "Urgent"}},
)
```

### PeoplePropertyFilter

Filter people properties.

```python
# Contains
filter = {"property": "Assignee", "people": {"contains": "user_id_123"}}

# Does not contain
filter = {"property": "Collaborators", "people": {"does_not_contain": "user_id_456"}}

# Is empty
filter = {"property": "Reviewer", "people": {"is_empty": True}}

# Is not empty
filter = {"property": "Owner", "people": {"is_not_empty": True}}
```

### FilesPropertyFilter

Filter files properties.

```python
# Is empty
filter = {"property": "Attachments", "files": {"is_empty": True}}

# Is not empty
filter = {"property": "Documents", "files": {"is_not_empty": True}}
```

### RelationPropertyFilter

Filter relation properties.

```python
from typing import Any

# Contains
filter = {"property": "Related Tasks", "relation": {"contains": "page_id_123"}}

# Does not contain
filter = {"property": "Dependencies", "relation": {"does_not_contain": "page_id_456"}}

# Is empty
filter = {"property": "Links", "relation": {"is_empty": True}}
    relation={"is_empty": True}
)

# Is not empty
filter = {"property": "Connections", "relation": {"is_not_empty": True}}
```

### FormulaPropertyFilter

Filter formula properties.

```python
# Number formula
filter = {"property": "Calculated Total", "formula": {"number": {"greater_than": 100}}}

# Text formula
filter = {"property": "Computed Name", "formula": {"string": {"contains": "prefix"}}}

# Checkbox formula
filter = {"property": "Is Valid", "formula": {"checkbox": {"equals": True}}}

# Date formula
filter = {"property": "Deadline", "formula": {"date": {"before": "2025-12-31"}}}
```

### RollupPropertyFilter

Filter rollup properties.

```python
# Number rollup
filter = {"property": "Total Cost", "rollup": {"number": {"greater_than": 1000}}}

# Date rollup
filter = {"property": "Earliest Date", "rollup": {"date": {"before": "2025-06-01"}}}

# Any (array contains)
filter = {"property": "All Tags", "rollup": {"any": {"rich_text": {"contains": "urgent"}}}}

# Every (all items match)
filter = {"property": "All Statuses", "rollup": {"every": {"select": {"equals": "Done"}}}}

# None (no items match)
filter = {"property": "No Blockers", "rollup": {"none": {"checkbox": {"equals": True}}}}
```

## Compound Filters

Combine multiple filters with AND/OR logic using helpers.

```python
from notion_py_client.filters import create_and_filter, create_or_filter

# AND - All conditions must match
and_filter = create_and_filter(
    {"property": "Status", "status": {"equals": "Active"}},
    {"property": "Priority", "number": {"greater_than": 5}},
    {"property": "Due", "date": {"on_or_before": "2025-12-31"}},
)

# OR - Any condition can match
or_filter = create_or_filter(
    {"property": "Status", "status": {"equals": "Urgent"}},
    {"property": "Status", "status": {"equals": "High Priority"}},
)

# Nested combinations
nested = create_and_filter(
    {"property": "Start", "date": {"on_or_after": "2025-01-01"}},
    create_or_filter(
        {"property": "Status", "status": {"equals": "Active"}},
        {"property": "Status", "status": {"equals": "In Progress"}},
    ),
)
```

## Timestamp Filters

Filter by created or last edited time.

```python
from notion_py_client.filters import TimestampFilter

# Created time - before
filter: TimestampFilter = {
    "timestamp": "created_time",
    "created_time": {"before": "2025-01-01T00:00:00.000Z"},
}

# Created time - after
filter = {"timestamp": "created_time", "created_time": {"after": "2024-01-01T00:00:00.000Z"}}

# Last edited time - past week
filter = {"timestamp": "last_edited_time", "last_edited_time": {"past_week": {}}}

# Last edited time - on or after
filter = {"timestamp": "last_edited_time", "last_edited_time": {"on_or_after": "2025-01-01T00:00:00.000Z"}}
```

## Usage with Query

```python
from notion_py_client import NotionAsyncClient
from notion_py_client.filters import create_and_filter

async with NotionAsyncClient(auth="secret_xxx") as client:
    # Single filter (dict)
    response = await client.dataSources.query(
        data_source_id="ds_abc123",
        filter={"property": "Status", "status": {"equals": "Active"}},
    )

    # Compound filter (helpers)
    filter_dict = create_and_filter(
        {"property": "Status", "status": {"equals": "Active"}},
        {"property": "Due", "date": {"on_or_before": "2025-12-31"}},
    )

    response = await client.dataSources.query(
        data_source_id="ds_abc123",
        filter=filter_dict,
    )
```

## Related

- [Data Sources API](../api/datasources.md) - Query with filters
- [Type Reference](index.md) - Overview
