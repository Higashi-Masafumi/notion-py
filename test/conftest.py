"""Pytest configuration and fixtures."""

import pytest

from notion_py_client.notion_client import NotionAsyncClient
from notion_py_client.properties.base_properties.multi_select_property import (
    MultiSelectProperty,
)
from notion_py_client.properties.base_properties.people_property import PeopleProperty
from notion_py_client.requests.page_requests import (
    CreatePageParameters,
    UpdatePageParameters,
)
from notion_py_client.helper import (
    NotionMapper,
    NotionPropertyDescriptor,
    Field as NotionField,
)
from notion_py_client.properties.base_properties._base_property import (
    NotionPropertyType,
)
from notion_py_client.properties.base_properties.date_property import DateProperty
from notion_py_client.requests.common import (
    PartialUserObjectRequest,
    SelectPropertyItemRequest,
)
from notion_py_client.requests.property_requests import (
    DatePropertyRequest,
    MultiSelectPropertyRequest,
    PeoplePropertyRequest,
)
from notion_py_client.responses.page import NotionPage

from datetime import date
from typing import Annotated

from pydantic import BaseModel, Field, StrictStr, StringConstraints
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


class DateRange(BaseModel):
    start_date: date = Field(..., description="The start date of the date range")
    end_date: date = Field(..., description="The end date of the date range")
    time_zone: StrictStr | None = Field(
        None, description="The time zone of the date range"
    )


class MemberResource(BaseModel):
    id: StrictStr = Field(..., description="The ID of the member resource")
    assignee: StrictStr | None = Field(
        None, description="The assignee of the member resource"
    )
    date_range: DateRange = Field(
        ...,
        description="The date range of the member resource",
        examples=[
            {
                "start_date": "2025-01-01",
                "end_date": "2025-02-01",
                "time_zone": "Asia/Tokyo",
            }
        ],
    )
    project_range: list[
        Annotated[StrictStr, StringConstraints(pattern=r"^\d{4}/\d{2}$")]
    ] = Field(
        ...,
        description="The project range of the member resource",
        examples=[["2025/01", "2025/02"]],
    )


class MockMapper(NotionMapper[MemberResource]):
    member_field: NotionPropertyDescriptor[
        PeopleProperty, PeoplePropertyRequest, str | None
    ] = NotionField(
        notion_name="Assignee",
        parser=lambda p: (
            getattr(p.people[0], "name", None)
            if p.people and len(p.people) > 0
            else None
        ),
        request_builder=lambda v: (
            PeoplePropertyRequest(people=[PartialUserObjectRequest(id=v)])
            if v is not None
            else PeoplePropertyRequest(people=[])
        ),
    )
    date_range_field: NotionPropertyDescriptor[
        DateProperty, DatePropertyRequest, DateRange | None
    ] = NotionField(
        notion_name="DateRange",
        parser=lambda p: (
            DateRange(
                start_date=date.fromisoformat(p.date.start),
                end_date=date.fromisoformat(p.date.end),
                time_zone=p.date.time_zone,
            )
            if p.date and p.date.end
            else None
        ),
    )
    project_range_field: NotionPropertyDescriptor[
        MultiSelectProperty, MultiSelectPropertyRequest, list[str]
    ] = NotionField(
        notion_name="ProjectRange",
        parser=lambda p: (
            [item.name for item in p.multi_select] if len(p.multi_select) > 0 else []
        ),
        request_builder=lambda v: (
            MultiSelectPropertyRequest(
                multi_select=[SelectPropertyItemRequest(name=name) for name in v]
            )
            if v
            else MultiSelectPropertyRequest(multi_select=[])
        ),
    )

    def to_domain(self, notion_page: NotionPage) -> MemberResource:
        properties = notion_page.properties
        member_property = properties[self.member_field.notion_name]
        if not member_property.type == NotionPropertyType.PEOPLE:
            raise ValueError(
                f"Expected PeopleProperty for '{self.member_field.notion_name}', got {member_property.type}"
            )
        date_property = properties[self.date_range_field.notion_name]
        if not date_property.type == NotionPropertyType.DATE:
            raise ValueError(
                f"Expected DateProperty for '{self.date_range_field.notion_name}', got {date_property.type}"
            )
        project_property = properties[self.project_range_field.notion_name]
        if not project_property.type == NotionPropertyType.MULTI_SELECT:
            raise ValueError(
                f"Expected MultiSelectProperty for '{self.project_range_field.notion_name}', got {project_property.type}"
            )
        date_range = self.date_range_field.parse(date_property)
        if date_range is None:
            raise ValueError("Date range lacking end date is not supported")
        return MemberResource(
            id=notion_page.id,
            assignee=self.member_field.parse(member_property),
            date_range=date_range,
            project_range=self.project_range_field.parse(project_property),
        )

    def build_create_properties(
        self, datasource_id: str, model: MemberResource
    ) -> CreatePageParameters: ...

    def build_update_properties(
        self, model: MemberResource
    ) -> UpdatePageParameters: ...


@pytest.fixture
def mock_notion_page():
    """Mock NotionPage for testing."""
    # TODO: Add mock NotionPage data
    pass


@pytest.fixture
def mock_database():
    """Mock NotionDatabase for testing."""
    # TODO: Add mock NotionDatabase data
    pass


@pytest.fixture
def mock_datasource():
    """Mock DataSource for testing."""
    # TODO: Add mock DataSource data
    notion_client = NotionAsyncClient(auth="fake_api_key")
    response = notion_client.dataSources.query(
        data_source_id="fake_datasource_id",
        page_size=1,
        filter={
            "property": "Status",
            "select": {"equals": "Active"},
        },
    )


@pytest.fixture
def mock_notion_mapper():
    """Mock NotionMapper for testing."""
    return MockMapper()
