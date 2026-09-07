"""Unit tests for database and data source response models."""

from notion_py_client.api_types import CreateDatabaseParameters
from notion_py_client.responses.database import NotionDatabase
from notion_py_client.responses.datasource import DataSource


def _database_payload(**overrides) -> dict:
    payload = {
        "object": "database",
        "id": "db_123",
        "title": [],
        "description": [],
        "parent": {"type": "page_id", "page_id": "page_123"},
        "is_inline": False,
        "in_trash": False,
        "is_locked": False,
        "created_time": "2026-09-01T00:00:00.000Z",
        "last_edited_time": "2026-09-01T00:00:00.000Z",
        "data_sources": [{"id": "ds_123", "name": "Tasks"}],
        "icon": None,
        "cover": None,
        "url": "https://app.notion.com/p/db_123",
        "public_url": None,
    }
    payload.update(overrides)
    return payload


def _data_source_payload(**overrides) -> dict:
    payload = {
        "object": "data_source",
        "id": "ds_123",
        "title": [],
        "description": [],
        "parent": {"type": "database_id", "database_id": "db_123"},
        "database_parent": {"type": "page_id", "page_id": "page_123"},
        "is_inline": False,
        "in_trash": False,
        "created_time": "2026-09-01T00:00:00.000Z",
        "last_edited_time": "2026-09-01T00:00:00.000Z",
        "created_by": {"object": "user", "id": "user_123"},
        "last_edited_by": {"object": "user", "id": "user_123"},
        "properties": {
            "Task name": {
                "id": "title",
                "name": "Task name",
                "type": "title",
                "title": {},
            }
        },
        "icon": None,
        "cover": None,
        "url": "https://app.notion.com/p/ds_123",
        "public_url": None,
    }
    payload.update(overrides)
    return payload


class TestCreateDatabaseParameters:
    """CreateDatabaseParameters follows the current Create a database spec."""

    def test_typed_database_requires_only_parent(self):
        params: CreateDatabaseParameters = {
            "parent": {"type": "page_id", "page_id": "page_123"},
            "database_type": "tasks",
        }

        assert params["database_type"] == "tasks"
        assert "initial_data_source" not in params
        assert "properties" not in params

    def test_custom_schema_uses_initial_data_source(self):
        params: CreateDatabaseParameters = {
            "parent": {"type": "page_id", "page_id": "page_123"},
            "title": [{"type": "text", "text": {"content": "Tracker"}}],
            "initial_data_source": {"properties": {"Name": {"title": {}}}},
        }

        assert params["initial_data_source"]["properties"]["Name"] == {"title": {}}
        assert "database_type" not in params


class TestNotionDatabase:
    """Test NotionDatabase response parsing."""

    def test_parse_regular_database_without_database_type(self):
        result = NotionDatabase.model_validate(_database_payload())

        assert result.id == "db_123"
        assert result.database_type is None

    def test_parse_typed_database(self):
        result = NotionDatabase.model_validate(
            _database_payload(database_type="skills")
        )

        assert result.database_type == "skills"

    def test_parse_app_created_database_type(self):
        result = NotionDatabase.model_validate(
            _database_payload(database_type="wiki")
        )

        assert result.database_type == "wiki"


class TestDataSource:
    """Test DataSource response parsing."""

    def test_parse_regular_data_source_without_database_type(self):
        result = DataSource.model_validate(_data_source_payload())

        assert result.id == "ds_123"
        assert result.database_type is None

    def test_parse_typed_data_source(self):
        result = DataSource.model_validate(
            _data_source_payload(database_type="projects")
        )

        assert result.database_type == "projects"
