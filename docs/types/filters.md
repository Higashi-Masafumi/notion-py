# Filter Types

Complete reference for database query filters.

## Filter Categories

Filters are located in `notion_py.filters`:

- Property filters - Filter by property values
- Compound filters - Combine multiple filters with AND/OR
- Timestamp filters - Filter by created/edited time

## Property Filters

### TextPropertyFilter

Filter text and rich text properties.

```python
from notion_py_client.filters import TextPropertyFilter

# Contains
filter = TextPropertyFilter(
    property="Name",
    rich_text={"contains": "urgent"}
)

# Does not contain
filter = TextPropertyFilter(
    property="Description",
    rich_text={"does_not_contain": "archived"}
)

# Equals
filter = TextPropertyFilter(
    property="Title",
    rich_text={"equals": "Exact Match"}
)

# Does not equal
filter = TextPropertyFilter(
    property="Title",
    rich_text={"does_not_equal": "Skip"}
)

# Starts with
filter = TextPropertyFilter(
    property="Name",
    rich_text={"starts_with": "PROJ"}
)

# Ends with
filter = TextPropertyFilter(
    property="Name",
    rich_text={"ends_with": "-2025"}
)

# Is empty
filter = TextPropertyFilter(
    property="Description",
    rich_text={"is_empty": True}
)

# Is not empty
filter = TextPropertyFilter(
    property="Description",
    rich_text={"is_not_empty": True}
)
```

### NumberPropertyFilter

Filter number properties.

```python
from notion_py_client.filters import NumberPropertyFilter

# Equals
filter = NumberPropertyFilter(
    property="Price",
    number={"equals": 100}
)

# Does not equal
filter = NumberPropertyFilter(
    property="Quantity",
    number={"does_not_equal": 0}
)

# Greater than
filter = NumberPropertyFilter(
    property="Score",
    number={"greater_than": 75}
)

# Less than
filter = NumberPropertyFilter(
    property="Age",
    number={"less_than": 18}
)

# Greater than or equal
filter = NumberPropertyFilter(
    property="Points",
    number={"greater_than_or_equal_to": 100}
)

# Less than or equal
filter = NumberPropertyFilter(
    property="Limit",
    number={"less_than_or_equal_to": 50}
)

# Is empty
filter = NumberPropertyFilter(
    property="Optional Number",
    number={"is_empty": True}
)

# Is not empty
filter = NumberPropertyFilter(
    property="Required Number",
    number={"is_not_empty": True}
)
```

### CheckboxPropertyFilter

Filter checkbox properties.

```python
from notion_py_client.filters import CheckboxPropertyFilter

# Checked
filter = CheckboxPropertyFilter(
    property="Done",
    checkbox={"equals": True}
)

# Unchecked
filter = CheckboxPropertyFilter(
    property="Active",
    checkbox={"equals": False}
)
```

### SelectPropertyFilter

Filter select properties.

```python
from notion_py_client.filters import SelectPropertyFilter

# Equals
filter = SelectPropertyFilter(
    property="Priority",
    select={"equals": "High"}
)

# Does not equal
filter = SelectPropertyFilter(
    property="Priority",
    select={"does_not_equal": "Low"}
)

# Is empty
filter = SelectPropertyFilter(
    property="Category",
    select={"is_empty": True}
)

# Is not empty
filter = SelectPropertyFilter(
    property="Category",
    select={"is_not_empty": True}
)
```

### MultiSelectPropertyFilter

Filter multi-select properties.

```python
from notion_py_client.filters import MultiSelectPropertyFilter

# Contains
filter = MultiSelectPropertyFilter(
    property="Tags",
    multi_select={"contains": "Important"}
)

# Does not contain
filter = MultiSelectPropertyFilter(
    property="Labels",
    multi_select={"does_not_contain": "Archived"}
)

# Is empty
filter = MultiSelectPropertyFilter(
    property="Categories",
    multi_select={"is_empty": True}
)

# Is not empty
filter = MultiSelectPropertyFilter(
    property="Categories",
    multi_select={"is_not_empty": True}
)
```

### StatusPropertyFilter

Filter status properties.

```python
from notion_py_client.filters import StatusPropertyFilter

# Equals
filter = StatusPropertyFilter(
    property="Status",
    status={"equals": "In Progress"}
)

# Does not equal
filter = StatusPropertyFilter(
    property="Status",
    status={"does_not_equal": "Done"}
)

# Is empty
filter = StatusPropertyFilter(
    property="Workflow",
    status={"is_empty": True}
)

# Is not empty
filter = StatusPropertyFilter(
    property="Workflow",
    status={"is_not_empty": True}
)
```

### DatePropertyFilter

Filter date properties.

```python
from notion_py_client.filters import DatePropertyFilter

# Equals
filter = DatePropertyFilter(
    property="Due Date",
    date={"equals": "2025-01-01"}
)

# Before
filter = DatePropertyFilter(
    property="Start Date",
    date={"before": "2025-12-31"}
)

# After
filter = DatePropertyFilter(
    property="End Date",
    date={"after": "2025-01-01"}
)

# On or before
filter = DatePropertyFilter(
    property="Deadline",
    date={"on_or_before": "2025-06-30"}
)

# On or after
filter = DatePropertyFilter(
    property="Launch",
    date={"on_or_after": "2025-07-01"}
)

# Past week
filter = DatePropertyFilter(
    property="Created",
    date={"past_week": {}}
)

# Past month
filter = DatePropertyFilter(
    property="Updated",
    date={"past_month": {}}
)

# Past year
filter = DatePropertyFilter(
    property="Archive Date",
    date={"past_year": {}}
)

# Next week
filter = DatePropertyFilter(
    property="Upcoming",
    date={"next_week": {}}
)

# Next month
filter = DatePropertyFilter(
    property="Future",
    date={"next_month": {}}
)

# Next year
filter = DatePropertyFilter(
    property="Long Term",
    date={"next_year": {}}
)

# Is empty
filter = DatePropertyFilter(
    property="Optional Date",
    date={"is_empty": True}
)

# Is not empty
filter = DatePropertyFilter(
    property="Required Date",
    date={"is_not_empty": True}
)
```

### PeoplePropertyFilter

Filter people properties.

```python
from notion_py_client.filters import PeoplePropertyFilter

# Contains
filter = PeoplePropertyFilter(
    property="Assignee",
    people={"contains": "user_id_123"}
)

# Does not contain
filter = PeoplePropertyFilter(
    property="Collaborators",
    people={"does_not_contain": "user_id_456"}
)

# Is empty
filter = PeoplePropertyFilter(
    property="Reviewer",
    people={"is_empty": True}
)

# Is not empty
filter = PeoplePropertyFilter(
    property="Owner",
    people={"is_not_empty": True}
)
```

### FilesPropertyFilter

Filter files properties.

```python
from notion_py_client.filters import FilesPropertyFilter

# Is empty
filter = FilesPropertyFilter(
    property="Attachments",
    files={"is_empty": True}
)

# Is not empty
filter = FilesPropertyFilter(
    property="Documents",
    files={"is_not_empty": True}
)
```

### RelationPropertyFilter

Filter relation properties.

```python
from notion_py_client.filters import RelationPropertyFilter

# Contains
filter = RelationPropertyFilter(
    property="Related Tasks",
    relation={"contains": "page_id_123"}
)

# Does not contain
filter = RelationPropertyFilter(
    property="Dependencies",
    relation={"does_not_contain": "page_id_456"}
)

# Is empty
filter = RelationPropertyFilter(
    property="Links",
    relation={"is_empty": True}
)

# Is not empty
filter = RelationPropertyFilter(
    property="Connections",
    relation={"is_not_empty": True}
)
```

### FormulaPropertyFilter

Filter formula properties.

```python
from notion_py_client.filters import FormulaPropertyFilter

# Number formula
filter = FormulaPropertyFilter(
    property="Calculated Total",
    formula={"number": {"greater_than": 100}}
)

# Text formula
filter = FormulaPropertyFilter(
    property="Computed Name",
    formula={"string": {"contains": "prefix"}}
)

# Checkbox formula
filter = FormulaPropertyFilter(
    property="Is Valid",
    formula={"checkbox": {"equals": True}}
)

# Date formula
filter = FormulaPropertyFilter(
    property="Deadline",
    formula={"date": {"before": "2025-12-31"}}
)
```

### RollupPropertyFilter

Filter rollup properties.

```python
from notion_py_client.filters import RollupPropertyFilter

# Number rollup
filter = RollupPropertyFilter(
    property="Total Cost",
    rollup={"number": {"greater_than": 1000}}
)

# Date rollup
filter = RollupPropertyFilter(
    property="Earliest Date",
    rollup={"date": {"before": "2025-06-01"}}
)

# Any (array contains)
filter = RollupPropertyFilter(
    property="All Tags",
    rollup={"any": {"rich_text": {"contains": "urgent"}}}
)

# Every (all items match)
filter = RollupPropertyFilter(
    property="All Statuses",
    rollup={"every": {"select": {"equals": "Done"}}}
)

# None (no items match)
filter = RollupPropertyFilter(
    property="No Blockers",
    rollup={"none": {"checkbox": {"equals": True}}}
)
```

## Compound Filters

Combine multiple filters with AND/OR logic.

```python
from notion_py_client.filters import CompoundFilter

# AND - All conditions must match
filter = CompoundFilter.and_(
    StatusPropertyFilter(property="Status", status={"equals": "Active"}),
    NumberPropertyFilter(property="Priority", number={"greater_than": 5}),
    DatePropertyFilter(property="Due", date={"on_or_before": "2025-12-31"}),
)

# OR - Any condition can match
filter = CompoundFilter.or_(
    StatusPropertyFilter(property="Status", status={"equals": "Urgent"}),
    StatusPropertyFilter(property="Status", status={"equals": "High Priority"}),
)

# Nested combinations
filter = CompoundFilter.and_(
    DatePropertyFilter(property="Start", date={"on_or_after": "2025-01-01"}),
    CompoundFilter.or_(
        StatusPropertyFilter(property="Status", status={"equals": "Active"}),
        StatusPropertyFilter(property="Status", status={"equals": "In Progress"}),
    ),
)
```

## Timestamp Filters

Filter by created or last edited time.

```python
from notion_py_client.filters import TimestampFilter

# Created time - before
filter = TimestampFilter(
    timestamp="created_time",
    created_time={"before": "2025-01-01T00:00:00.000Z"}
)

# Created time - after
filter = TimestampFilter(
    timestamp="created_time",
    created_time={"after": "2024-01-01T00:00:00.000Z"}
)

# Last edited time - past week
filter = TimestampFilter(
    timestamp="last_edited_time",
    last_edited_time={"past_week": {}}
)

# Last edited time - on or after
filter = TimestampFilter(
    timestamp="last_edited_time",
    last_edited_time={"on_or_after": "2025-01-01T00:00:00.000Z"}
)
```

## Usage with Query

```python
from notion_py_client import NotionAsyncClient
from notion_py_client.filters import (
    StatusPropertyFilter,
    DatePropertyFilter,
    CompoundFilter,
)

async with NotionAsyncClient(auth="secret_xxx") as client:
    # Single filter
    response = await client.dataSources.query(
        data_source_id="ds_abc123",
        filter=StatusPropertyFilter(
            property="Status",
            status={"equals": "Active"}
        ).model_dump(by_alias=True, exclude_none=True)
    )

    # Compound filter
    filter = CompoundFilter.and_(
        StatusPropertyFilter(property="Status", status={"equals": "Active"}),
        DatePropertyFilter(property="Due", date={"on_or_before": "2025-12-31"}),
    )

    response = await client.dataSources.query(
        data_source_id="ds_abc123",
        filter=filter.model_dump(by_alias=True, exclude_none=True)
    )
```

## Related

- [Data Sources API](../api/datasources.md) - Query with filters
- [Type Reference](index.md) - Overview
