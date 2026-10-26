"""Unit tests for status property schema responses."""

import pytest
from pydantic import ValidationError

from notion_py_client.responses.datasource import DataSource
from notion_py_client.schema.property_configs.base_configs.status_config import (
    StatusPropertyConfig,
)


def _status_property(*, default_option: str | None) -> dict:
    return {
        "id": "stat",
        "name": "Status",
        "description": None,
        "type": "status",
        "status": {
            "default_option": default_option,
            "options": [
                {
                    "id": "opt_progress",
                    "name": "In progress",
                    "color": "blue",
                    "description": None,
                }
            ],
            "groups": [
                {
                    "id": "group_progress",
                    "name": "In progress",
                    "color": "blue",
                    "option_ids": ["opt_progress"],
                }
            ],
        },
    }


class TestStatusPropertyConfig:
    """Status schemas expose the read-only default option name."""

    def test_parses_default_option_name(self):
        config = StatusPropertyConfig.model_validate(
            _status_property(default_option="In progress")
        )

        assert config.status.default_option == "In progress"
        assert config.status.options[0].name == "In progress"

    def test_parses_null_default_option(self):
        config = StatusPropertyConfig.model_validate(
            _status_property(default_option=None)
        )

        assert config.status.default_option is None

    def test_rejects_missing_default_option(self):
        payload = _status_property(default_option="In progress")
        del payload["status"]["default_option"]

        with pytest.raises(ValidationError):
            StatusPropertyConfig.model_validate(payload)

    def test_to_dict_omits_read_only_default_option(self):
        config = StatusPropertyConfig.model_validate(
            _status_property(default_option="In progress")
        )

        payload = config.to_dict()

        assert "default_option" not in payload["status"]
        assert payload["status"]["options"][0]["name"] == "In progress"

    def test_data_source_schema_exposes_default_option(self):
        data_source = DataSource.model_validate(
            {
                "object": "data_source",
                "id": "ds_123",
                "title": [],
                "description": [],
                "parent": {"type": "database_id", "database_id": "db_123"},
                "database_parent": {"type": "page_id", "page_id": "page_123"},
                "is_inline": False,
                "in_trash": False,
                "created_time": "2026-10-22T00:00:00.000Z",
                "last_edited_time": "2026-10-22T00:00:00.000Z",
                "created_by": {"object": "user", "id": "user_123"},
                "last_edited_by": {"object": "user", "id": "user_123"},
                "properties": {"Status": _status_property(default_option="In progress")},
                "url": "https://www.notion.so/ds_123",
                "public_url": None,
            }
        )

        status = data_source.properties["Status"]
        assert isinstance(status, StatusPropertyConfig)
        assert status.status.default_option == "In progress"
