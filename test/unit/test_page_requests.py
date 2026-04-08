"""Unit tests for page request models."""

from notion_py_client.requests.page_requests import (
    CreatePageParameters,
    PageTemplateRequest,
    UpdatePageMarkdownParameters,
    UpdatePageParameters,
)


class TestUpdatePageParameters:
    """Test page update parameters."""

    def test_in_trash_serializes(self):
        params = UpdatePageParameters(page_id="page_123", in_trash=True)

        payload = params.model_dump(exclude_none=True, by_alias=True)

        assert payload["in_trash"] is True

    def test_template_and_erase_content_serialize(self):
        params = UpdatePageParameters(
            page_id="page_123",
            template=PageTemplateRequest(
                type="template_id",
                template_id="template_123",
                timezone="Asia/Tokyo",
            ),
            erase_content=True,
        )

        payload = params.model_dump(exclude_none=True, by_alias=True)

        assert payload["template"]["type"] == "template_id"
        assert payload["template"]["template_id"] == "template_123"
        assert payload["template"]["timezone"] == "Asia/Tokyo"
        assert payload["erase_content"] is True


class TestCreatePageParameters:
    """Test page creation parameters."""

    def test_markdown_and_template_serialize(self):
        params = CreatePageParameters(
            parent={"type": "page_id", "page_id": "page_123"},
            properties={},
            markdown="# Hello",
            template=PageTemplateRequest(type="default", timezone="America/New_York"),
        )

        payload = params.model_dump(exclude_none=True, by_alias=True)

        assert payload["markdown"] == "# Hello"
        assert payload["template"]["type"] == "default"
        assert payload["template"]["timezone"] == "America/New_York"


class TestUpdatePageMarkdownParameters:
    """Test markdown update parameters."""

    def test_update_content_serializes(self):
        params = UpdatePageMarkdownParameters(
            type="update_content",
            update_content={
                "content_updates": [
                    {
                        "old_str": "Draft proposal",
                        "new_str": "Draft proposal (due Friday)",
                        "replace_all_matches": True,
                    }
                ],
                "allow_deleting_content": True,
            },
        )

        payload = params.model_dump(exclude_none=True, by_alias=True)

        assert payload["type"] == "update_content"
        assert payload["update_content"]["content_updates"][0]["old_str"] == "Draft proposal"
        assert payload["update_content"]["allow_deleting_content"] is True
