"""Unit tests for database title visibility."""

import pytest

from notion_py_client.notion_client import NotionAsyncClient
from notion_py_client.responses.database import NotionDatabase


def _database_response(*, show_data_source_title: bool) -> dict:
    return {
        "object": "database",
        "id": "db_123",
        "title": [],
        "description": [],
        "parent": {"type": "page_id", "page_id": "page_123"},
        "is_inline": False,
        "in_trash": False,
        "is_locked": False,
        "show_data_source_title": show_data_source_title,
        "created_time": "2026-10-20T00:00:00.000Z",
        "last_edited_time": "2026-10-20T00:00:00.000Z",
        "data_sources": [{"id": "ds_123", "name": "Tasks"}],
        "icon": None,
        "cover": None,
        "url": "https://www.notion.so/db_123",
        "public_url": None,
    }


class TestNotionDatabase:
    """Database objects include the data source title setting."""

    def test_parses_hidden_data_source_title(self):
        database = NotionDatabase.model_validate(
            _database_response(show_data_source_title=False)
        )

        assert database.show_data_source_title is False

    def test_parses_shown_data_source_title(self):
        database = NotionDatabase.model_validate(
            _database_response(show_data_source_title=True)
        )

        assert database.show_data_source_title is True


class TestDatabasesAPI:
    """Create and update forward the data source title setting."""

    @pytest.mark.asyncio
    async def test_create_sends_show_data_source_title(self):
        client = NotionAsyncClient(auth="test-token")
        captured: dict = {}

        async def fake_request(*, path, method, body=None, auth=None, **kwargs):
            captured["path"] = path
            captured["method"] = method
            captured["body"] = body
            return _database_response(show_data_source_title=False)

        client.request = fake_request  # type: ignore[method-assign]

        result = await client.databases.create(
            {
                "parent": {"type": "page_id", "page_id": "page_123"},
                "properties": {},
                "show_data_source_title": False,
            }
        )

        assert captured["path"] == "databases"
        assert captured["method"] == "post"
        assert captured["body"]["show_data_source_title"] is False
        assert isinstance(result, NotionDatabase)
        assert result.show_data_source_title is False

    @pytest.mark.asyncio
    async def test_update_sends_show_data_source_title(self):
        client = NotionAsyncClient(auth="test-token")
        captured: dict = {}

        async def fake_request(*, path, method, body=None, auth=None, **kwargs):
            captured["path"] = path
            captured["method"] = method
            captured["body"] = body
            return _database_response(show_data_source_title=True)

        client.request = fake_request  # type: ignore[method-assign]

        result = await client.databases.update(
            {
                "database_id": "db_123",
                "show_data_source_title": True,
            }
        )

        assert captured["path"] == "databases/db_123"
        assert captured["method"] == "patch"
        assert captured["body"] == {"show_data_source_title": True}
        assert result.show_data_source_title is True
