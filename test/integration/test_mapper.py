"""Integration tests for Domain Mapper.

These tests require actual Notion API data.
Set NOTION_API_TOKEN and TEST_DATASOURCE_ID environment variables to run these tests.

Usage:
    export NOTION_API_TOKEN="your_api_key"
    export TEST_DATASOURCE_ID="your_datasource_id"
    pytest test/integration/test_mapper.py -v
"""

import os
import pytest
from notion_py_client import NotionAsyncClient


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
def test_datasource_id():
    """Get test datasource ID from environment."""
    datasource_id = os.getenv("TEST_DATASOURCE_ID")
    if not datasource_id:
        pytest.skip("TEST_DATASOURCE_ID not set")
    return datasource_id


class TestMapperIntegration:
    """Integration tests for NotionMapper with real data."""

    @pytest.mark.asyncio
    async def test_query_and_parse_with_mapper(
        self, notion_client, test_datasource_id, mock_notion_mapper
    ):
        """Test querying datasource and parsing with mapper.

        Steps:
        1. Query pages from real datasource
        2. Use mapper to convert to domain models
        3. Verify domain model fields are correctly populated
        """
        # Query datasource
        response = await notion_client.dataSources.query(
            data_source_id=test_datasource_id, page_size=5
        )

        assert response is not None
        assert hasattr(response, "results")
        assert len(response.results) > 0

        # Parse first page with mapper
        first_page = response.results[0]

        # Convert to domain model
        try:
            domain_model = mock_notion_mapper.to_domain(first_page)

            # Verify domain model
            assert domain_model.id == first_page.id
            assert domain_model.assignee is None or isinstance(
                domain_model.assignee, str
            )
            assert domain_model.date_range is not None
            assert domain_model.project_range is not None

            print(f"Successfully parsed page: {domain_model.id}")
            print(f"  Assignee: {domain_model.assignee}")
            print(f"  Date Range: {domain_model.date_range}")
            print(f"  Project Range: {domain_model.project_range}")

        except ValueError as e:
            # Skip if page doesn't have required fields
            pytest.skip(f"Page missing required fields: {e}")

    @pytest.mark.asyncio
    async def test_query_multiple_pages_with_mapper(
        self, notion_client, test_datasource_id, mock_notion_mapper
    ):
        """Test parsing multiple pages from datasource.

        Verifies that mapper can handle various data patterns.
        """
        response = await notion_client.dataSources.query(
            data_source_id=test_datasource_id, page_size=10
        )

        assert response is not None
        assert len(response.results) > 0

        parsed_count = 0
        error_count = 0

        for page in response.results:
            try:
                domain_model = mock_notion_mapper.to_domain(page)
                parsed_count += 1

                # Basic validation
                assert domain_model.id == page.id
                assert isinstance(domain_model.project_range, list)

            except (ValueError, KeyError, AttributeError) as e:
                # Some pages may not have all required fields
                error_count += 1
                print(f"Failed to parse page {page.id}: {e}")

        print(f"Successfully parsed: {parsed_count}/{len(response.results)} pages")
        print(f"Parse errors: {error_count}")

        # At least some pages should be parseable
        assert parsed_count > 0
