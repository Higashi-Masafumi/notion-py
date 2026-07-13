"""Unit tests for property schema request/response models."""

import pytest

from notion_py_client.schema import StatusOptionConfig, StatusPropertyConfig


class TestStatusPropertyConfig:
    """Test status property schema configuration."""

    def test_status_option_group_serializes(self):
        config = StatusPropertyConfig(
            id="status",
            name="Status",
            status={
                "options": [
                    {
                        "name": "Needs review",
                        "group": "In progress",
                    }
                ]
            }
        )

        payload = config.model_dump(exclude_none=True)

        assert payload["status"]["options"] == [
            {"name": "Needs review", "group": "In progress"}
        ]

    def test_status_option_requires_id_or_name(self):
        with pytest.raises(ValueError, match="Status option requires"):
            StatusOptionConfig(group="Complete")
