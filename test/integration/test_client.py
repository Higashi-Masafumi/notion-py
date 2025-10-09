"""Integration tests for Notion API client.

These tests require actual Notion API credentials and will make real API calls.
Set the NOTION_API_TOKEN environment variable to run these tests.

Usage:
    export NOTION_API_TOKEN="your_api_key"
    pytest test/integration/test_client.py
"""

import os
import pytest
from notion_py_client import NotionAsyncClient
from notion_py_client.requests.common import DateRequest


# Skip integration tests if NOTION_API_TOKEN is not set
pytestmark = pytest.mark.skipif(
    not os.getenv("NOTION_API_TOKEN"),
    reason="NOTION_API_TOKEN environment variable not set",
)


@pytest.fixture
def notion_client() -> NotionAsyncClient:
    """Create NotionAsyncClient with API key from environment."""

    api_key = os.getenv("NOTION_API_TOKEN")
    return NotionAsyncClient(auth=api_key)  # type: ignore


@pytest.fixture
def test_database_id():
    """Get test database ID from environment.

    Set TEST_DATABASE_ID environment variable to use a specific database.
    """
    return os.getenv("TEST_DATABASE_ID")


@pytest.fixture
def test_datasource_id():
    """Get test datasource ID from environment.

    Set TEST_DATASOURCE_ID environment variable to use a specific datasource.
    """
    return os.getenv("TEST_DATASOURCE_ID")


class TestDataSourcesAPI:
    """Integration tests for DataSources API."""

    @pytest.mark.asyncio
    async def test_query_datasource(self, notion_client, test_datasource_id):
        """Test querying a datasource."""
        if not test_datasource_id:
            pytest.skip("TEST_DATASOURCE_ID not set")

        response = await notion_client.dataSources.query(
            data_source_id=test_datasource_id, page_size=10
        )

        assert response is not None
        assert hasattr(response, "results")
        assert len(response.results) > 0

        # Verify response structure
        assert hasattr(response, "has_more")
        assert hasattr(response, "next_cursor")
        assert response.object == "list"

        # Verify first result is a NotionPage
        from notion_py_client.responses.page import NotionPage

        first_result = response.results[0]
        assert isinstance(first_result, NotionPage)
        assert hasattr(first_result, "id")
        assert hasattr(first_result, "properties")

    @pytest.mark.asyncio
    async def test_query_with_filter(self, notion_client, test_datasource_id):
        """Test querying a datasource with filters."""
        if not test_datasource_id:
            pytest.skip("TEST_DATASOURCE_ID not set")

        # Example filter for member resource schema (multi-select ProjectRange)
        filter_obj: dict = {
            "property": "ProjectRange",
            "multi_select": {"is_not_empty": True},
        }

        response = await notion_client.dataSources.query(
            data_source_id=test_datasource_id, filter=filter_obj, page_size=5
        )

        assert response is not None
        assert hasattr(response, "results")
        # Results may be empty if no matching records
        assert isinstance(response.results, list)

    @pytest.mark.asyncio
    async def test_query_with_compound_filter(self, notion_client, test_datasource_id):
        """Test querying with compound AND filter."""
        if not test_datasource_id:
            pytest.skip("TEST_DATASOURCE_ID not set")

        from notion_py_client.filters import create_and_filter

        # Create compound filter (adjust property names to match your datasource)
        filter_obj = create_and_filter(
            {"property": "Assignee", "people": {"is_not_empty": True}},
            {"property": "ProjectRange", "multi_select": {"is_not_empty": True}},
        )

        response = await notion_client.dataSources.query(
            data_source_id=test_datasource_id,
            filter=filter_obj,  # type: ignore
            page_size=10,
        )

        assert response is not None
        assert isinstance(response.results, list)

    @pytest.mark.asyncio
    async def test_query_with_sorts(self, notion_client, test_datasource_id):
        """Test querying with sort parameters."""
        if not test_datasource_id:
            pytest.skip("TEST_DATASOURCE_ID not set")

        # Sort by created_time descending
        sorts = [{"timestamp": "created_time", "direction": "descending"}]

        response = await notion_client.dataSources.query(
            data_source_id=test_datasource_id, sorts=sorts, page_size=5
        )

        assert response is not None
        assert len(response.results) > 0

        # Verify results are sorted (most recent first)
        if len(response.results) >= 2:
            first_time = response.results[0].created_time
            second_time = response.results[1].created_time
            assert first_time >= second_time

    @pytest.mark.asyncio
    async def test_query_pagination(self, notion_client, test_datasource_id):
        """Test pagination with start_cursor."""
        if not test_datasource_id:
            pytest.skip("TEST_DATASOURCE_ID not set")

        # Get first page
        first_response = await notion_client.dataSources.query(
            data_source_id=test_datasource_id, page_size=2
        )

        assert first_response is not None

        # If has_more is True, fetch next page
        if first_response.has_more:
            second_response = await notion_client.dataSources.query(
                data_source_id=test_datasource_id,
                page_size=2,
                start_cursor=first_response.next_cursor,
            )

            assert second_response is not None
            assert len(second_response.results) > 0

            # Verify different results
            first_ids = {p.id for p in first_response.results}
            second_ids = {p.id for p in second_response.results}
            assert first_ids.isdisjoint(second_ids)

    @pytest.mark.asyncio
    async def test_retrieve_datasource(self, notion_client, test_datasource_id):
        """Test retrieving datasource schema."""
        if not test_datasource_id:
            pytest.skip("TEST_DATASOURCE_ID not set")

        datasource = await notion_client.dataSources.retrieve(
            data_source_id=test_datasource_id
        )

        assert datasource is not None
        assert hasattr(datasource, "id")
        assert hasattr(datasource, "properties")
        assert datasource.id == test_datasource_id
        assert isinstance(datasource.properties, dict)
        assert len(datasource.properties) > 0


class TestPagesAPI:
    """Integration tests for Pages API."""

    @pytest.mark.asyncio
    async def test_create_and_retrieve_page(self, notion_client, test_datasource_id):
        """Test creating and retrieving a page."""
        if not test_datasource_id:
            pytest.skip("TEST_DATASOURCE_ID not set")

        from datetime import date

        from notion_py_client.requests.common import SelectPropertyItemRequest
        from notion_py_client.requests.page_requests import CreatePageParameters
        from notion_py_client.requests.property_requests import (
            DatePropertyRequest,
            MultiSelectPropertyRequest,
            PeoplePropertyRequest,
            TitlePropertyRequest,
        )

        # Create a new page
        params = CreatePageParameters(
            parent={"type": "data_source_id", "data_source_id": test_datasource_id},
            properties={
                "Assignee": PeoplePropertyRequest(people=[]),
                "DateRange": DatePropertyRequest(
                    date=DateRequest(
                        start=date.today().isoformat(), end=date.today().isoformat()
                    )
                ),
                "ProjectRange": MultiSelectPropertyRequest(
                    multi_select=[SelectPropertyItemRequest(name="2025/01")]
                ),
            },
        )

        created_page = await notion_client.pages.create(params=params)

        assert created_page is not None
        assert created_page.id is not None
        assert created_page.object == "page"

        # Retrieve the created page
        from notion_py_client.api_types import RetrievePageParameters

        retrieve_params: RetrievePageParameters = {"page_id": created_page.id}
        retrieved_page = await notion_client.pages.retrieve(params=retrieve_params)

        assert retrieved_page is not None
        assert retrieved_page.id == created_page.id
        assert retrieved_page.object == "page"

    @pytest.mark.asyncio
    async def test_update_page(self, notion_client, test_datasource_id):
        """Test updating a page."""
        if not test_datasource_id:
            pytest.skip("TEST_DATASOURCE_ID not set")

        from datetime import date

        from notion_py_client.requests.common import SelectPropertyItemRequest
        from notion_py_client.requests.page_requests import (
            CreatePageParameters,
            UpdatePageParameters,
        )
        from notion_py_client.requests.property_requests import (
            DatePropertyRequest,
            MultiSelectPropertyRequest,
            PeoplePropertyRequest,
            TitlePropertyRequest,
        )

        # First create a page
        create_params = CreatePageParameters(
            parent={"type": "data_source_id", "data_source_id": test_datasource_id},
            properties={
                "Assignee": PeoplePropertyRequest(people=[]),
                "DateRange": DatePropertyRequest(
                    date=DateRequest(
                        start=date.today().isoformat(), end=date.today().isoformat()
                    )
                ),
                "ProjectRange": MultiSelectPropertyRequest(
                    multi_select=[SelectPropertyItemRequest(name="2025/01")]
                ),
            },
        )

        created_page = await notion_client.pages.create(params=create_params)

        # Update the page
        update_params = UpdatePageParameters(
            page_id=created_page.id,
            properties={
                "ProjectRange": MultiSelectPropertyRequest(
                    multi_select=[SelectPropertyItemRequest(name="2025/02")]
                ),
            },
        )

        updated_page = await notion_client.pages.update(params=update_params)

        assert updated_page is not None
        assert updated_page.id == created_page.id

        # Verify the multi-select property was updated
        project_prop = updated_page.properties.get("ProjectRange")
        assert project_prop is not None
        from notion_py_client.responses.property_types import MultiSelectProperty

        if isinstance(project_prop, MultiSelectProperty):
            values = {item.name for item in project_prop.multi_select}
            assert "2025/02" in values

    @pytest.mark.skip(reason="Create operations affect Notion workspace")
    @pytest.mark.asyncio
    async def test_create_page_with_multiple_properties(
        self, notion_client, test_datasource_id
    ):
        """Test creating a page with various property types."""
        if not test_datasource_id:
            pytest.skip("TEST_DATASOURCE_ID not set")

        from datetime import date

        from notion_py_client.requests.common import SelectPropertyItemRequest
        from notion_py_client.requests.page_requests import CreatePageParameters
        from notion_py_client.requests.property_requests import (
            DatePropertyRequest,
            MultiSelectPropertyRequest,
            NumberPropertyRequest,
            PeoplePropertyRequest,
            RichTextPropertyRequest,
            TitlePropertyRequest,
        )

        params = CreatePageParameters(
            parent={"type": "database_id", "database_id": test_datasource_id},
            properties={
                "Name": TitlePropertyRequest(
                    title=[{"type": "text", "text": {"content": "Multi-Property Test"}}]
                ),
                "Summary": RichTextPropertyRequest(
                    rich_text=[{"type": "text", "text": {"content": "Test notes"}}]
                ),
                "Capacity": NumberPropertyRequest(number=80),
                "Assignee": PeoplePropertyRequest(people=[]),
                "DateRange": DatePropertyRequest(
                    date=DateRequest(
                        start=date.today().isoformat(),
                        end=date.today().isoformat(),
                    )
                ),
                "ProjectRange": MultiSelectPropertyRequest(
                    multi_select=[
                        SelectPropertyItemRequest(name="2025/01"),
                        SelectPropertyItemRequest(name="2025/02"),
                    ]
                ),
            },
        )

        page = await notion_client.pages.create(params=params)

        assert page is not None
        assert page.id is not None
        assert "Name" in page.properties


class TestBlocksAPI:
    """Integration tests for Blocks API."""

    @pytest.mark.asyncio
    async def test_retrieve_block_children(self, notion_client, test_datasource_id):
        """Test retrieving block children from a page."""
        if not test_datasource_id:
            pytest.skip("TEST_DATASOURCE_ID not set")

        # First get a page from the datasource
        response = await notion_client.dataSources.query(
            data_source_id=test_datasource_id, page_size=1
        )

        if len(response.results) == 0:
            pytest.skip("No pages in datasource")

        page_id = response.results[0].id

        # Retrieve block children
        blocks_response = await notion_client.blocks.children.list(
            block_id=page_id, page_size=10
        )

        assert blocks_response is not None
        assert "results" in blocks_response
        assert isinstance(blocks_response["results"], list)

    @pytest.mark.skip(reason="Append operations affect Notion workspace")
    @pytest.mark.asyncio
    async def test_append_block_children(self, notion_client, test_datasource_id):
        """Test appending block children to a page."""
        if not test_datasource_id:
            pytest.skip("TEST_DATASOURCE_ID not set")

        from notion_py_client.requests.page_requests import CreatePageParameters
        from notion_py_client.requests.property_requests import TitlePropertyRequest

        # Create a new page to add blocks to
        params = CreatePageParameters(
            parent={"type": "database_id", "database_id": test_datasource_id},
            properties={
                "Name": TitlePropertyRequest(
                    title=[{"type": "text", "text": {"content": "Page with Blocks"}}]
                ),
            },
        )

        page = await notion_client.pages.create(params=params)

        # Append paragraph block
        from notion_py_client.api_types import AppendBlockChildrenParameters

        append_params: AppendBlockChildrenParameters = {
            "block_id": page.id,
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": "This is a test paragraph."},
                            }
                        ]
                    },
                }
            ],
        }

        result = await notion_client.blocks.children.append(params=append_params)

        assert result is not None
        assert "results" in result
        assert len(result["results"]) > 0


class TestDatabasesAPI:
    """Integration tests for Databases API (legacy)."""

    @pytest.mark.asyncio
    async def test_retrieve_database(self, notion_client, test_database_id):
        """Test retrieving a database."""
        if not test_database_id:
            pytest.skip("TEST_DATABASE_ID not set")

        from notion_py_client.api_types import RetrieveDatabaseParameters

        params: RetrieveDatabaseParameters = {"database_id": test_database_id}
        database = await notion_client.databases.retrieve(params=params)

        assert database is not None
        assert hasattr(database, "id")
        # Normalize UUID comparison (remove hyphens)
        assert database.id.replace("-", "") == test_database_id.replace("-", "")
        assert hasattr(database, "data_sources")

    @pytest.mark.skip(
        reason="databases.query() method is legacy and may not be supported"
    )
    @pytest.mark.asyncio
    async def test_query_database(self, notion_client, test_database_id):
        """Test querying a database (legacy endpoint)."""
        if not test_database_id:
            pytest.skip("TEST_DATABASE_ID not set")

        from notion_py_client.api_types import QueryDatabaseParameters

        params: QueryDatabaseParameters = {
            "database_id": test_database_id,
            "page_size": 5,
        }

        response = await notion_client.databases.query(params=params)

        assert response is not None
        assert hasattr(response, "results")
        assert isinstance(response.results, list)


class TestUsersAPI:
    """Integration tests for Users API."""

    @pytest.mark.asyncio
    async def test_list_users(self, notion_client):
        """Test listing users."""
        response = await notion_client.users.list(page_size=10)

        assert response is not None
        assert hasattr(response, "results")
        assert isinstance(response.results, list)
        assert response.object == "list"

        # Verify user structure
        if len(response.results) > 0:
            user = response.results[0]
            assert hasattr(user, "id")
            assert hasattr(user, "object")
            assert user.object == "user"

    @pytest.mark.asyncio
    async def test_retrieve_bot_user(self, notion_client):
        """Test retrieving bot user details."""
        bot_user = await notion_client.users.me()

        assert bot_user is not None
        assert "object" in bot_user
        assert bot_user["object"] == "user"
        assert "type" in bot_user
        assert bot_user["type"] == "bot"


class TestSearchAPI:
    """Integration tests for Search API."""

    @pytest.mark.skip(reason="search.search() method not yet implemented")
    @pytest.mark.asyncio
    async def test_search_pages(self, notion_client):
        """Test search functionality for pages."""
        from notion_py_client.api_types import SearchParameters

        params: SearchParameters = {
            "query": "test",
            "filter": {"property": "object", "value": "page"},
            "page_size": 5,
        }

        response = await notion_client.search.search(params=params)

        assert response is not None
        assert hasattr(response, "results")
        assert isinstance(response.results, list)
        assert response.object == "list"

    @pytest.mark.skip(
        reason="search.search() method is legacy and may not be supported"
    )
    @pytest.mark.asyncio
    async def test_search_databases(self, notion_client):
        """Test search functionality for databases."""
        from notion_py_client.api_types import SearchParameters

        params: SearchParameters = {
            "filter": {"property": "object", "value": "database"},
            "page_size": 5,
        }

        response = await notion_client.search.search(params=params)

        assert response is not None
        assert hasattr(response, "results")
        assert isinstance(response.results, list)

    @pytest.mark.skip(reason="search.search() method not yet implemented")
    @pytest.mark.asyncio
    async def test_search_with_sort(self, notion_client):
        """Test search with sort parameter."""
        from notion_py_client.api_types import SearchParameters

        params: SearchParameters = {
            "query": "",
            "sort": {"direction": "descending", "timestamp": "last_edited_time"},
            "page_size": 5,
        }

        response = await notion_client.search.search(params=params)

        assert response is not None
        assert hasattr(response, "results")

        # Verify results are sorted if there are multiple
        if len(response.results) >= 2:
            # Results should be in descending order of last_edited_time
            for i in range(len(response.results) - 1):
                current = response.results[i]
                next_item = response.results[i + 1]
                if hasattr(current, "last_edited_time") and hasattr(
                    next_item, "last_edited_time"
                ):
                    assert current.last_edited_time >= next_item.last_edited_time
