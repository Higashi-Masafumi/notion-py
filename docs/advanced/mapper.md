# Domain Mapping

The domain mapping pattern helps you work with Notion data using your own domain models instead of raw Notion API types.

## Overview

`NotionMapper` provides a structured way to:

- Convert Notion pages to domain models
- Build property requests from domain models
- Centralize mapping logic in one place
- Maintain type safety throughout

## Core Concepts

### NotionPropertyDescriptor

A descriptor that handles bidirectional conversion between Notion properties and domain values.

```python
from notion_py_client.helper import NotionPropertyDescriptor

descriptor = NotionPropertyDescriptor(
    notion_name="Status",  # Property name in Notion
    parser=lambda p: p.select.name if p.select else "",  # Notion -> Domain
    request_builder=lambda v: StatusPropertyRequest(select={"name": v})  # Domain -> Notion
)
```

### Field Factory

The `Field()` function creates property descriptors with type inference:

```python
from notion_py_client.helper import Field
from notion_py_client.requests.property_requests import TitlePropertyRequest

# Read-write field
title_field = Field(
    notion_name="Name",
    parser=lambda p: p.title[0].plain_text if p.title else "",
    request_builder=lambda v: TitlePropertyRequest(
        title=[{"type": "text", "text": {"content": v}}]
    )
)

# Read-only field (e.g., Formula)
duration_field = Field(
    notion_name="Duration",
    parser=lambda p: p.formula.number or 0
    # No request_builder = read-only
)
```

### NotionMapper

Abstract base class for creating mappers:

```python
from notion_py_client.helper import NotionMapper
from pydantic import BaseModel

class Task(BaseModel):
    id: str
    name: str
    status: str
    priority: int

class TaskMapper(NotionMapper[Task]):
    # Define fields
    name_field = Field(...)
    status_field = Field(...)

    def to_domain(self, notion_page: NotionPage) -> Task:
        # Convert Notion page to domain model
        pass

    def build_update_properties(self, model: Task) -> UpdatePageParameters:
        # Build update request from domain model
        pass

    def build_create_properties(
        self, datasource_id: str, model: Task
    ) -> CreatePageParameters:
        # Build create request from domain model
        pass
```

## Complete Example

### Define Domain Model

```python
from pydantic import BaseModel
from datetime import date

class ProjectTask(BaseModel):
    id: str
    title: str
    status: str
    priority: str
    due_date: date | None
    assignee: str | None
    estimated_hours: float
    actual_hours: float | None
```

### Create Mapper

```python
from notion_py_client.helper import NotionMapper, NotionPropertyDescriptor, Field
from notion_py_client import NotionPage
from notion_py_client.requests.page_requests import (
    CreatePageParameters,
    UpdatePageParameters,
)
from notion_py_client.requests.property_requests import (
    TitlePropertyRequest,
    SelectPropertyRequest,
    DatePropertyRequest,
    PeoplePropertyRequest,
    NumberPropertyRequest,
    StatusPropertyRequest,
)
from notion_py_client.responses.property_types import (
    TitleProperty,
    SelectProperty,
    DateProperty,
    PeopleProperty,
    NumberProperty,
    StatusProperty,
    FormulaProperty,
)
from typing_extensions import Never

class ProjectTaskMapper(NotionMapper[ProjectTask]):
    # Define field descriptors with type annotations
    title_field: NotionPropertyDescriptor[TitleProperty, TitlePropertyRequest, str] = Field(
        notion_name="Task Name",
        parser=lambda p: p.title[0].plain_text if p.title else "",
        request_builder=lambda v: TitlePropertyRequest(
            title=[{"type": "text", "text": {"content": v}}]
        )
    )

    status_field: NotionPropertyDescriptor[StatusProperty, StatusPropertyRequest, str] = Field(
        notion_name="Status",
        parser=lambda p: p.status.name if p.status else "Not Started",
        request_builder=lambda v: StatusPropertyRequest(
            status={"name": v}
        )
    )

    priority_field: NotionPropertyDescriptor[SelectProperty, SelectPropertyRequest, str] = Field(
        notion_name="Priority",
        parser=lambda p: p.select.name if p.select else "Medium",
        request_builder=lambda v: SelectPropertyRequest(
            select={"name": v}
        )
    )

    due_date_field: NotionPropertyDescriptor[DateProperty, DatePropertyRequest, date | None] = Field(
        notion_name="Due Date",
        parser=lambda p: date.fromisoformat(p.date.start) if p.date else None,
        request_builder=lambda v: DatePropertyRequest(
            date={"start": v.isoformat()} if v else None
        )
    )

    assignee_field: NotionPropertyDescriptor[PeopleProperty, PeoplePropertyRequest, str | None] = Field(
        notion_name="Assignee",
        parser=lambda p: p.people[0].name if p.people else None,
        request_builder=lambda v: PeoplePropertyRequest(
            people=[{"id": v}] if v else []
        )
    )

    estimated_hours_field: NotionPropertyDescriptor[NumberProperty, NumberPropertyRequest, float] = Field(
        notion_name="Estimated Hours",
        parser=lambda p: p.number or 0.0,
        request_builder=lambda v: NumberPropertyRequest(number=v)
    )

    # Read-only formula field (Never for request type)
    actual_hours_field: NotionPropertyDescriptor[FormulaProperty, Never, float] = Field(
        notion_name="Actual Hours",
        parser=lambda p: p.formula.number or 0.0
        # No request_builder = read-only
    )

    def to_domain(self, notion_page: NotionPage) -> ProjectTask:
        """Convert Notion page to domain model."""
        props = notion_page.properties

        return ProjectTask(
            id=notion_page.id,
            title=self.title_field.parse(props["Task Name"]),
            status=self.status_field.parse(props["Status"]),
            priority=self.priority_field.parse(props["Priority"]),
            due_date=self.due_date_field.parse(props["Due Date"]),
            assignee=self.assignee_field.parse(props["Assignee"]),
            estimated_hours=self.estimated_hours_field.parse(props["Estimated Hours"]),
            actual_hours=self.actual_hours_field.parse(props["Actual Hours"]),
        )

    def build_update_properties(
        self, model: ProjectTask
    ) -> UpdatePageParameters:
        """Build update request from domain model."""
        return UpdatePageParameters(
            page_id=model.id,
            properties={
                self.title_field.notion_name: self.title_field.build_request(model.title),
                self.status_field.notion_name: self.status_field.build_request(model.status),
                self.priority_field.notion_name: self.priority_field.build_request(model.priority),
                self.due_date_field.notion_name: self.due_date_field.build_request(model.due_date),
                self.assignee_field.notion_name: self.assignee_field.build_request(model.assignee),
                self.estimated_hours_field.notion_name: self.estimated_hours_field.build_request(model.estimated_hours),
            }
        )

    def build_create_properties(
        self, datasource_id: str, model: ProjectTask
    ) -> CreatePageParameters:
        """Build create request from domain model."""
        return CreatePageParameters(
            parent={"type": "database_id", "database_id": datasource_id},
            properties={
                self.title_field.notion_name: self.title_field.build_request(model.title),
                self.status_field.notion_name: self.status_field.build_request(model.status),
                self.priority_field.notion_name: self.priority_field.build_request(model.priority),
                self.due_date_field.notion_name: self.due_date_field.build_request(model.due_date),
                self.assignee_field.notion_name: self.assignee_field.build_request(model.assignee),
                self.estimated_hours_field.notion_name: self.estimated_hours_field.build_request(model.estimated_hours),
            }
        )
```

### Use the Mapper

```python
from notion_py_client import NotionAsyncClient
from datetime import date

async with NotionAsyncClient(auth="secret_xxx") as client:
    mapper = ProjectTaskMapper()

    # Query pages and convert to domain models
    response = await client.dataSources.query(
        data_source_id="ds_abc123"
    )

    tasks = [mapper.to_domain(page) for page in response.results]

    # Work with domain models
    for task in tasks:
        print(f"{task.title}: {task.status} (Priority: {task.priority})")

    # Update a task
    task = tasks[0]
    task.status = "In Progress"
    task.estimated_hours = 8.0

    update_params = mapper.build_update_properties(task)
    await client.pages.update(update_params)

    # Create a new task
    new_task = ProjectTask(
        id="",  # Will be set by Notion
        title="New Task",
        status="Not Started",
        priority="High",
        due_date=date(2025, 12, 31),
        assignee="user_abc123",
        estimated_hours=4.0,
        actual_hours=None,
    )

    create_params = mapper.build_create_properties("ds_abc123", new_task)
    created_page = await client.pages.create(create_params)

    # Convert back to domain model
    created_task = mapper.to_domain(created_page)
    print(f"Created task ID: {created_task.id}")
```

## Benefits

### Type Safety

Domain models provide compile-time type checking:

```python
task = ProjectTask(
    id="123",
    title="Task",
    status="Done",
    priority="High",
    due_date=date.today(),
    assignee="user_id",
    estimated_hours=5.0,
    actual_hours=4.5,
)

# IDE autocomplete works
print(task.status)  # IDE knows this is str
print(task.due_date.year)  # IDE knows this is date
```

### Centralized Logic

All mapping logic lives in one place:

```python
# Easy to update when Notion schema changes
class TaskMapper(NotionMapper[Task]):
    # Just update the field definitions
    status_field = Field(
        notion_name="Status",  # Changed property name
        parser=lambda p: p.select.name if p.select else "Todo",
        request_builder=lambda v: SelectPropertyRequest(select={"name": v})
    )
```

### Testability

Domain models and mappers are easy to test:

```python
def test_task_mapper():
    mapper = ProjectTaskMapper()

    # Create test data
    task = ProjectTask(
        id="test_id",
        title="Test Task",
        status="Done",
        # ...
    )

    # Test mapping
    params = mapper.build_update_properties(task)
    assert params.page_id == "test_id"
    assert params.properties["Status"].status.name == "Done"
```

### Business Logic

Domain models can contain business logic:

```python
class ProjectTask(BaseModel):
    id: str
    title: str
    status: str
    estimated_hours: float
    actual_hours: float | None

    @property
    def is_overdue(self) -> bool:
        return self.due_date < date.today() if self.due_date else False

    @property
    def is_over_budget(self) -> bool:
        if self.actual_hours is None:
            return False
        return self.actual_hours > self.estimated_hours

    def mark_complete(self):
        self.status = "Done"
```

## Advanced Patterns

### Nested Models

```python
class Assignee(BaseModel):
    id: str
    name: str
    email: str

class Task(BaseModel):
    id: str
    title: str
    assignee: Assignee | None

class TaskMapper(NotionMapper[Task]):
    assignee_field = Field(
        notion_name="Assignee",
        parser=lambda p: Assignee(
            id=p.people[0].id,
            name=p.people[0].name,
            email=p.people[0].person.email
        ) if p.people else None,
        request_builder=lambda v: PeoplePropertyRequest(
            people=[{"id": v.id}] if v else []
        )
    )
```

### Computed Properties

```python
class Task(BaseModel):
    id: str
    start_date: date
    end_date: date

    @property
    def duration_days(self) -> int:
        return (self.end_date - self.start_date).days

# Map from Notion formula
duration_field = Field(
    notion_name="Duration",
    parser=lambda p: p.formula.number or 0
)
```

### Validation

```python
from pydantic import field_validator

class Task(BaseModel):
    id: str
    title: str
    priority: str

    @field_validator('priority')
    @classmethod
    def validate_priority(cls, v: str) -> str:
        allowed = ["Low", "Medium", "High", "Critical"]
        if v not in allowed:
            raise ValueError(f"Priority must be one of {allowed}")
        return v
```

## Related

- [Pages API](../api/pages.md) - Page operations
- [Data Sources API](../api/datasources.md) - Query operations
- [Type Reference](../types/index.md) - Type system overview
