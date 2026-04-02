"""Unit tests for client facade additions and defaults."""

import pytest

from notion_py_client.notion_client import NotionAsyncClient
from notion_py_client.requests.page_requests import ReplaceContentMarkdownCommand
from notion_py_client.responses.page_markdown import PageMarkdownResponse


class TestNotionAsyncClientDefaults:
    """Test client default configuration."""

    def test_default_version_tracks_latest_breaking_release(self):
        client = NotionAsyncClient(auth="test-token")

        assert client.default_notion_version == "2026-03-11"
        assert client._notion_version == "2026-03-11"


class TestPageMarkdownAPI:
    """Test page markdown helpers."""

    @pytest.mark.asyncio
    async def test_retrieve_markdown_passes_query(self):
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
            page_id="page_123", include_transcript=True
        )

        assert isinstance(result, PageMarkdownResponse)
        assert captured["path"] == "pages/page_123/markdown"
        assert captured["method"] == "get"
        assert captured["query"] == {"include_transcript": True}
        assert result.markdown == "# Heading"

    @pytest.mark.asyncio
    async def test_update_markdown_serializes_command(self):
        client = NotionAsyncClient(auth="test-token")
        captured: dict = {}

        async def fake_request(*, path, method, body=None, auth=None, **kwargs):
            captured["path"] = path
            captured["method"] = method
            captured["body"] = body
            return {
                "object": "page_markdown",
                "id": "page_123",
                "markdown": "# Fresh Start",
                "truncated": False,
                "unknown_block_ids": [],
            }

        client.request = fake_request  # type: ignore[method-assign]

        result = await client.pages.update_markdown(
            page_id="page_123",
            command=ReplaceContentMarkdownCommand(
                replace_content={
                    "new_str": "# Fresh Start",
                    "allow_deleting_content": True,
                }
            ),
        )

        assert captured["path"] == "pages/page_123/markdown"
        assert captured["method"] == "patch"
        assert captured["body"] == {
            "type": "replace_content",
            "replace_content": {
                "new_str": "# Fresh Start",
                "allow_deleting_content": True,
            },
        }
        assert result.markdown == "# Fresh Start"


class TestCustomEmojisAPI:
    """Test custom emoji listing facade."""

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
                "type": "custom_emoji",
                "results": [
                    {
                        "id": "emoji_123",
                        "name": "ship-it",
                        "url": "https://example.com/ship-it.png",
                    }
                ],
                "has_more": False,
                "next_cursor": None,
            }

        client.request = fake_request  # type: ignore[method-assign]

        result = await client.customEmojis.list(name="ship-it", page_size=10)

        assert captured["path"] == "custom_emojis"
        assert captured["method"] == "get"
        assert captured["query"] == {"page_size": 10, "name": "ship-it"}
        assert result.type == "custom_emoji"
        assert result.results[0].name == "ship-it"
