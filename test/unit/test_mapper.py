"""Unit tests for NotionMapper and Field."""

import pytest
from datetime import date
from typing import cast
from pydantic import BaseModel, Field as PydanticField, StrictStr
from notion_py_client.helper import NotionMapper, NotionPropertyDescriptor, Field
from notion_py_client.requests.property_requests import (
    TitlePropertyRequest,
    StatusPropertyRequest,
    NumberPropertyRequest,
)
from notion_py_client.requests.common import SelectPropertyItemRequest
from notion_py_client.responses.property_types import (
    TitleProperty,
    StatusProperty,
    NumberProperty,
)
from notion_py_client.properties.base_properties._base_property import (
    NotionPropertyType,
)
from notion_py_client.requests.page_requests import (
    CreatePageParameters,
    UpdatePageParameters,
)
from notion_py_client.responses.page import NotionPage
from notion_py_client.models import RichTextItem, PartialUser, StatusOption
from notion_py_client.models.primitives import Text, Annotations


class Task(BaseModel):
    """Test domain model."""

    id: StrictStr
    name: StrictStr
    status: StrictStr
    priority: int


class TaskMapper(NotionMapper[Task]):
    """Test mapper implementation."""

    name_field: NotionPropertyDescriptor[TitleProperty, TitlePropertyRequest, str] = (
        Field(
            notion_name="Name",
            parser=lambda p: p.title[0].plain_text if p.title else "",
            request_builder=lambda v: TitlePropertyRequest(
                title=[{"type": "text", "text": {"content": v}}]
            ),
        )
    )

    status_field: NotionPropertyDescriptor[
        StatusProperty, StatusPropertyRequest, str
    ] = Field(
        notion_name="Status",
        parser=lambda p: p.status.name if p.status else "",
        request_builder=lambda v: StatusPropertyRequest(
            status=SelectPropertyItemRequest(name=v)
        ),
    )

    priority_field: NotionPropertyDescriptor[
        NumberProperty, NumberPropertyRequest, int
    ] = Field(
        notion_name="Priority",
        parser=lambda p: int(p.number) if p.number else 0,
        request_builder=lambda v: NumberPropertyRequest(number=v),
    )

    def to_domain(self, notion_page: NotionPage) -> Task:
        """Convert Notion page to domain model."""
        props = notion_page.properties
        return Task(
            id=notion_page.id,
            name=self.name_field.parse(cast(TitleProperty, props["Name"])),
            status=self.status_field.parse(cast(StatusProperty, props["Status"])),
            priority=self.priority_field.parse(cast(NumberProperty, props["Priority"])),
        )

    def build_update_properties(self, model: Task) -> UpdatePageParameters:
        """Build update parameters from domain model."""
        return UpdatePageParameters(
            page_id=model.id,
            properties={
                self.name_field.notion_name: self.name_field.build_request(model.name),
                self.status_field.notion_name: self.status_field.build_request(
                    model.status
                ),
                self.priority_field.notion_name: self.priority_field.build_request(
                    model.priority
                ),
            },
        )

    def build_create_properties(
        self, datasource_id: str, model: Task
    ) -> CreatePageParameters:
        """Build create parameters from domain model."""
        return CreatePageParameters(
            parent={"type": "database_id", "database_id": datasource_id},
            properties={
                self.name_field.notion_name: self.name_field.build_request(model.name),
                self.status_field.notion_name: self.status_field.build_request(
                    model.status
                ),
                self.priority_field.notion_name: self.priority_field.build_request(
                    model.priority
                ),
            },
        )


class TestField:
    """Test Field factory function."""

    def test_field_creation_parser_only(self):
        """Test Field creates NotionPropertyDescriptor with parser only."""
        field = Field(
            notion_name="Test",
            parser=lambda p: "test",
        )

        assert isinstance(field, NotionPropertyDescriptor)
        assert field.notion_name == "Test"
        assert field.parser is not None
        assert field.request_builder is not None  # Default lambda

    def test_field_creation_with_both(self):
        """Test Field with both parser and request_builder."""
        field = Field(
            notion_name="Title",
            parser=lambda p: "test",
            request_builder=lambda v: TitlePropertyRequest(
                title=[{"type": "text", "text": {"content": v}}]
            ),
        )

        assert field.notion_name == "Title"
        assert field.parser is not None
        assert field.request_builder is not None

    def test_field_request_builder_works(self):
        """Test that request_builder produces correct output."""
        field = Field(
            notion_name="Status",
            parser=lambda p: getattr(p, "status", None) and getattr(p.status, "name", ""),  # type: ignore
            request_builder=lambda v: StatusPropertyRequest(
                status=SelectPropertyItemRequest(name=v)
            ),
        )

        request = field.build_request("In Progress")
        assert isinstance(request, StatusPropertyRequest)
        result = request.model_dump(by_alias=True, exclude_none=True)
        assert result["status"]["name"] == "In Progress"

    def test_field_parser_readonly(self):
        """Test read-only field (parser only, no request_builder)."""
        field = Field(
            notion_name="Formula",
            parser=lambda p: getattr(getattr(p, "formula", None), "number", 0),  # type: ignore
        )

        assert field.notion_name == "Formula"
        # Default request_builder should exist but return None
        result = field.build_request(100)
        assert result is None

    def test_field_writeonly(self):
        """Test write-only field (request_builder only, no parser)."""
        field = Field(
            notion_name="WriteOnly",
            request_builder=lambda v: NumberPropertyRequest(number=v),  # type: ignore
        )

        assert field.notion_name == "WriteOnly"
        # Default parser should exist but return None
        # (Cannot test parse without actual property object)


class TestNotionPropertyDescriptor:
    """Test NotionPropertyDescriptor class."""

    def test_descriptor_initialization(self):
        """Test descriptor can be initialized."""
        descriptor = NotionPropertyDescriptor(
            notion_name="Test",
            parser=lambda p: "value",
            request_builder=lambda v: TitlePropertyRequest(
                title=[{"type": "text", "text": {"content": v}}]
            ),
        )

        assert descriptor.notion_name == "Test"

    def test_descriptor_parse_method(self):
        """Test parse method works."""
        descriptor = NotionPropertyDescriptor(
            notion_name="Title",
            parser=lambda p: p.title[0].plain_text if p.title else "",  # type: ignore
            request_builder=lambda v: TitlePropertyRequest(
                title=[{"type": "text", "text": {"content": v}}]
            ),
        )

        # Create mock TitleProperty
        mock_property = TitleProperty(
            id="test-id",
            type=NotionPropertyType.TITLE,
            title=[
                RichTextItem(
                    type="text",
                    text=Text(content="Test Title", link=None),
                    plain_text="Test Title",
                    href=None,
                    mention=None,
                    equation=None,
                    annotations=Annotations(
                        bold=False,
                        italic=False,
                        strikethrough=False,
                        underline=False,
                        code=False,
                        color="default",
                    ),
                )
            ],
        )

        result = descriptor.parse(mock_property)
        assert result == "Test Title"

    def test_descriptor_build_request_method(self):
        """Test build_request method works."""
        descriptor = NotionPropertyDescriptor(
            notion_name="Priority",
            parser=lambda p: int(p.number) if p.number else 0,  # type: ignore
            request_builder=lambda v: NumberPropertyRequest(number=v),  # type: ignore
        )

        request = descriptor.build_request(5)
        assert isinstance(request, NumberPropertyRequest)
        assert request.number == 5


class TestNotionMapper:
    """Test NotionMapper abstract base class."""

    def test_mapper_initialization(self):
        """Test mapper can be initialized."""
        mapper = TaskMapper()

        assert mapper.name_field.notion_name == "Name"
        assert mapper.status_field.notion_name == "Status"
        assert mapper.priority_field.notion_name == "Priority"

    def test_field_descriptors_accessible(self):
        """Test field descriptors are accessible as class attributes."""
        mapper = TaskMapper()

        # Fields should be accessible
        assert hasattr(mapper, "name_field")
        assert hasattr(mapper, "status_field")
        assert hasattr(mapper, "priority_field")

        # Check notion_name values
        assert mapper.name_field.notion_name == "Name"
        assert mapper.status_field.notion_name == "Status"
        assert mapper.priority_field.notion_name == "Priority"

    def test_mapper_with_mock_page(self):
        """Test to_domain conversion with mock NotionPage."""
        from notion_py_client.models import StatusOption

        # Create mock properties
        mock_properties = {
            "Name": TitleProperty(
                id="title-id",
                type=NotionPropertyType.TITLE,
                title=[
                    RichTextItem(
                        type="text",
                        text=Text(content="Test Task", link=None),
                        plain_text="Test Task",
                        href=None,
                        mention=None,
                        equation=None,
                        annotations=Annotations(
                            bold=False,
                            italic=False,
                            strikethrough=False,
                            underline=False,
                            code=False,
                            color="default",
                        ),
                    )
                ],
            ),
            "Status": StatusProperty(
                id="status-id",
                type=NotionPropertyType.STATUS,
                status=StatusOption(
                    id="status-opt-id",
                    name="In Progress",
                    color="blue",
                    description=None,
                ),
            ),
            "Priority": NumberProperty(
                id="number-id", type=NotionPropertyType.NUMBER, number=3
            ),
        }

        # Create mock NotionPage
        mock_page = NotionPage(
            object="page",
            id="test-page-id",
            created_time="2024-01-01T00:00:00.000Z",
            created_by=PartialUser(object="user", id="user-123"),
            last_edited_time="2024-01-01T00:00:00.000Z",
            last_edited_by=PartialUser(object="user", id="user-123"),
            archived=False,
            in_trash=False,
            is_locked=False,
            icon=None,
            cover=None,
            properties=mock_properties,
            parent={"type": "database_id", "database_id": "test-db-id"},
            url="https://notion.so/test",
            public_url=None,
            request_id=None,
        )

        # Test conversion
        mapper = TaskMapper()
        task = mapper.to_domain(mock_page)

        assert isinstance(task, Task)
        assert task.id == "test-page-id"
        assert task.name == "Test Task"
        assert task.status == "In Progress"
        assert task.priority == 3

    def test_mapper_build_update_properties(self):
        """Test build_update_properties method."""
        mapper = TaskMapper()
        task = Task(id="page-123", name="Updated Task", status="Done", priority=5)

        params = mapper.build_update_properties(task)

        assert isinstance(params, UpdatePageParameters)
        assert params.page_id == "page-123"
        assert params.properties is not None
        assert "Name" in params.properties
        assert "Status" in params.properties
        assert "Priority" in params.properties

        # Verify request types
        assert isinstance(params.properties["Name"], TitlePropertyRequest)
        assert isinstance(params.properties["Status"], StatusPropertyRequest)
        assert isinstance(params.properties["Priority"], NumberPropertyRequest)

    def test_mapper_build_create_properties(self):
        """Test build_create_properties method."""
        mapper = TaskMapper()
        task = Task(id="", name="New Task", status="Todo", priority=1)

        params = mapper.build_create_properties("db-123", task)

        assert isinstance(params, CreatePageParameters)
        # Type narrow to DatabaseParent
        parent = params.parent
        assert parent["type"] == "database_id"
        if parent["type"] == "database_id":  # type: ignore
            assert parent["database_id"] == "db-123"

        assert params.properties is not None
        assert "Name" in params.properties
        assert "Status" in params.properties
        assert "Priority" in params.properties


class TestMapperEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_title_property(self):
        """Test parsing empty title property."""
        mapper = TaskMapper()
        empty_title = TitleProperty(
            id="title-id", type=NotionPropertyType.TITLE, title=[]
        )

        result = mapper.name_field.parse(empty_title)
        assert result == ""

    def test_none_status_property(self):
        """Test parsing status property with None value."""
        mapper = TaskMapper()
        none_status = StatusProperty(
            id="status-id", type=NotionPropertyType.STATUS, status=None
        )

        result = mapper.status_field.parse(none_status)
        assert result == ""

    def test_none_number_property(self):
        """Test parsing number property with None value."""
        mapper = TaskMapper()
        none_number = NumberProperty(
            id="number-id", type=NotionPropertyType.NUMBER, number=None
        )

        result = mapper.priority_field.parse(none_number)
        assert result == 0
