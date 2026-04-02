"""Unit tests for page request models."""

import pytest

from notion_py_client.requests.page_requests import (
    CreatePageParameters,
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
            template={"type": "default", "timezone": "Asia/Tokyo"},
            erase_content=True,
        )

        payload = params.model_dump(exclude_none=True, by_alias=True)

        assert payload["template"]["type"] == "default"
        assert payload["template"]["timezone"] == "Asia/Tokyo"
        assert payload["erase_content"] is True


class TestCreatePageParameters:
    """Test page create parameters."""

    def test_markdown_mode_serializes(self):
        params = CreatePageParameters(
            parent={"type": "page_id", "page_id": "page_123"},
            properties={},
            markdown="# Heading\n\nBody",
            position={"type": "page_end"},
        )

        payload = params.model_dump(exclude_none=True, by_alias=True)

        assert payload["markdown"] == "# Heading\n\nBody"
        assert payload["position"]["type"] == "page_end"

    def test_template_serializes(self):
        params = CreatePageParameters(
            parent={"type": "data_source_id", "data_source_id": "ds_123"},
            properties={},
            template={
                "type": "template_id",
                "template_id": "template_123",
                "timezone": "America/New_York",
            },
        )

        payload = params.model_dump(exclude_none=True, by_alias=True)

        assert payload["template"]["template_id"] == "template_123"
        assert payload["template"]["timezone"] == "America/New_York"

    def test_markdown_cannot_mix_with_children(self):
        with pytest.raises(ValueError, match="markdown cannot be used"):
            CreatePageParameters(
                parent={"type": "page_id", "page_id": "page_123"},
                properties={},
                markdown="# Heading",
                children=[{"object": "block", "type": "paragraph", "paragraph": {}}],
            )

    def test_template_cannot_mix_with_children(self):
        with pytest.raises(ValueError, match="template cannot be used"):
            CreatePageParameters(
                parent={"type": "data_source_id", "data_source_id": "ds_123"},
                properties={},
                template={"type": "default"},
                children=[{"object": "block", "type": "paragraph", "paragraph": {}}],
            )
