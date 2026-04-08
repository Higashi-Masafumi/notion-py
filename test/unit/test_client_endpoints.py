"""Unit tests for newly added endpoint helpers."""

import pytest

from notion_py_client.notion_client import NotionAsyncClient
from notion_py_client.requests.page_requests import UpdatePageMarkdownParameters


class TestPageMarkdownAPI:
    @pytest.mark.asyncio
    async def test_retrieve_markdown_uses_markdown_endpoint(self):
        client = NotionAsyncClient(auth="test-token")
        captured: dict = {}

        async def fake_request(*, path, method, query=None, auth=None, **kwargs):
            captured["path"] = path
            captured["method"] = method
            captured["query"] = query
            return {
                "object": "page_markdown",
                "id": "page_123",
                "markdown": "# Heading",
                "truncated": False,
                "unknown_block_ids": [],
            }

        client.request = fake_request  # type: ignore[method-assign]

        result = await client.pages.retrieve_markdown(
            page_id="page_123",
            include_transcript=True,
        )

        assert captured["path"] == "pages/page_123/markdown"
        assert captured["method"] == "get"
        assert captured["query"] == {"include_transcript": "true"}
        assert result.markdown == "# Heading"

    @pytest.mark.asyncio
    async def test_update_markdown_uses_markdown_endpoint(self):
        client = NotionAsyncClient(auth="test-token")
        captured: dict = {}

        async def fake_request(*, path, method, body=None, auth=None, **kwargs):
            captured["path"] = path
            captured["method"] = method
            captured["body"] = body
            return {
                "object": "page_markdown",
                "id": "page_123",
                "markdown": "# Updated",
                "truncated": False,
                "unknown_block_ids": [],
            }

        client.request = fake_request  # type: ignore[method-assign]

        result = await client.pages.update_markdown(
            page_id="page_123",
            params=UpdatePageMarkdownParameters(
                type="replace_content",
                replace_content={"new_str": "# Updated"},
            ),
        )

        assert captured["path"] == "pages/page_123/markdown"
        assert captured["method"] == "patch"
        assert captured["body"]["type"] == "replace_content"
        assert captured["body"]["replace_content"]["new_str"] == "# Updated"
        assert result.object == "page_markdown"


class TestCommentsAPI:
    @pytest.mark.asyncio
    async def test_create_comment_accepts_markdown(self):
        client = NotionAsyncClient(auth="test-token")
        captured: dict = {}

        async def fake_request(*, path, method, body=None, auth=None, **kwargs):
            captured["path"] = path
            captured["method"] = method
            captured["body"] = body
            return {
                "object": "comment",
                "id": "comment_123",
                "parent": {"type": "page_id", "page_id": "page_123"},
                "discussion_id": "discussion_123",
                "created_time": "2026-04-07T00:00:00.000Z",
                "last_edited_time": "2026-04-07T00:00:00.000Z",
                "created_by": {"object": "user", "id": "user_123"},
                "rich_text": [],
            }

        client.request = fake_request  # type: ignore[method-assign]

        await client.comments.create(
            parent={"page_id": "page_123"},
            markdown="**hello**",
        )

        assert captured["path"] == "comments"
        assert captured["method"] == "post"
        assert captured["body"]["markdown"] == "**hello**"
        assert "rich_text" not in captured["body"]

    @pytest.mark.asyncio
    async def test_create_comment_requires_exactly_one_body_shape(self):
        client = NotionAsyncClient(auth="test-token")

        with pytest.raises(ValueError):
            await client.comments.create(
                parent={"page_id": "page_123"},
                rich_text=[],
                markdown="**hello**",
            )


class TestCustomEmojisAPI:
    @pytest.mark.asyncio
    async def test_list_custom_emojis(self):
        client = NotionAsyncClient(auth="test-token")
        captured: dict = {}

        async def fake_request(*, path, method, query=None, auth=None, **kwargs):
            captured["path"] = path
            captured["method"] = method
            captured["query"] = query
            return {
                "object": "list",
                "results": [
                    {
                        "id": "emoji_123",
                        "name": "party_parrot",
                        "url": "https://example.com/parrot.png",
                    }
                ],
                "next_cursor": None,
                "has_more": False,
            }

        client.request = fake_request  # type: ignore[method-assign]

        result = await client.customEmojis.list(name="party_parrot")

        assert captured["path"] == "custom_emojis"
        assert captured["method"] == "get"
        assert captured["query"] == {"name": "party_parrot"}
        assert result.results[0].name == "party_parrot"
