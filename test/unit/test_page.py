"""Unit tests for page response models."""

from notion_py_client.properties import RelationProperty, RollupProperty
from notion_py_client.models.icon import IconType
from notion_py_client.responses.page import NotionPage


class TestNotionPage:
    """Test NotionPage response parsing."""

    def test_parse_rollup_show_original_relation_property(self):
        """Rollup arrays should accept relation property values."""
        data = {
            "object": "page",
            "id": "page_123",
            "created_time": "2025-01-01T00:00:00.000Z",
            "last_edited_time": "2025-01-02T00:00:00.000Z",
            "created_by": {"object": "user", "id": "user_123"},
            "last_edited_by": {"object": "user", "id": "user_123"},
            "parent": {"type": "database_id", "database_id": "db_123"},
            "archived": False,
            "in_trash": False,
            "is_locked": False,
            "properties": {
                "新チャネル": {
                    "id": "prop_rollup",
                    "type": "rollup",
                    "rollup": {
                        "type": "array",
                        "array": [
                            {
                                "id": "prop_relation",
                                "type": "relation",
                                "relation": [
                                    {"id": "page-id-1"},
                                    {"id": "page-id-2"},
                                ],
                                "has_more": False,
                            }
                        ],
                        "function": "show_original",
                    },
                }
            },
            "url": "https://www.notion.so/page_123",
        }

        result = NotionPage.model_validate(data)

        rollup_property = result.properties["新チャネル"]
        assert isinstance(rollup_property, RollupProperty)
        assert rollup_property.rollup.type == "array"
        assert rollup_property.rollup.array is not None
        assert len(rollup_property.rollup.array) == 1

        relation_property = rollup_property.rollup.array[0]
        assert isinstance(relation_property, RelationProperty)
        assert [item.id for item in relation_property.relation] == [
            "page-id-1",
            "page-id-2",
        ]
        assert relation_property.get_display_value() == "page-id-1, page-id-2"

    def test_parse_native_icon_and_in_trash_alias(self):
        """Page responses should accept native icons and archived aliases."""
        data = {
            "object": "page",
            "id": "page_icon",
            "created_time": "2025-01-01T00:00:00.000Z",
            "last_edited_time": "2025-01-02T00:00:00.000Z",
            "created_by": {"object": "user", "id": "user_123"},
            "last_edited_by": {"object": "user", "id": "user_123"},
            "parent": {"type": "page_id", "page_id": "parent_123"},
            "in_trash": True,
            "is_locked": False,
            "properties": {},
            "icon": {
                "type": "icon",
                "icon": {
                    "name": "bullseye",
                    "color": "blue",
                },
            },
            "url": "https://www.notion.so/page_icon",
        }

        result = NotionPage.model_validate(data)

        assert result.in_trash is True
        assert result.archived is True
        assert result.icon is not None
        assert result.icon.type == IconType.ICON
        assert result.icon.icon is not None
        assert result.icon.icon.name == "bullseye"
        assert result.icon.icon.color == "blue"
