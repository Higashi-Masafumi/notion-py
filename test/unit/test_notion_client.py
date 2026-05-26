"""Unit tests for client facade additions and defaults."""

import pytest
from pydantic import ValidationError

from notion_py_client.blocks.special_blocks import MeetingNotesBlock
from notion_py_client.notion_client import NotionAsyncClient
from notion_py_client.requests.page_requests import ReplaceContentMarkdownCommand
from notion_py_client.responses.list_response import CommentObject, QueryMeetingNotesResponse
from notion_py_client.responses.page_markdown import PageMarkdownResponse


def _rich_text(content: str) -> list[dict]:
    return [
        {
            "type": "text",
            "text": {"content": content, "link": None},
            "annotations": {
                "bold": False,
                "italic": False,
                "strikethrough": False,
                "underline": False,
                "code": False,
                "color": "default",
            },
            "plain_text": content,
            "href": None,
        }
    ]


def _comment_response(content: str = "Hello") -> dict:
    return {
        "object": "comment",
        "id": "comment_123",
        "parent": {"type": "page_id", "page_id": "page_123"},
        "discussion_id": "discussion_123",
        "created_time": "2026-05-01T00:00:00.000Z",
        "last_edited_time": "2026-05-01T00:00:00.000Z",
        "created_by": {"object": "user", "id": "user_123"},
        "rich_text": _rich_text(content),
    }


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

    @pytest.mark.asyncio
    async def test_list_custom_emojis_validates_required_response_type(self):
        client = NotionAsyncClient(auth="test-token")

        async def fake_request(*, path, method, query=None, auth=None, **kwargs):
            return {
                "object": "list",
                "results": [],
                "has_more": False,
                "next_cursor": None,
            }

        client.request = fake_request  # type: ignore[method-assign]

        with pytest.raises(ValidationError):
            await client.customEmojis.list()


class TestCommentsAPI:
    """Test comment create/update/delete helpers."""

    @pytest.mark.asyncio
    async def test_create_comment_accepts_markdown(self):
        client = NotionAsyncClient(auth="test-token")
        captured: dict = {}

        async def fake_request(*, path, method, body=None, auth=None, **kwargs):
            captured["path"] = path
            captured["method"] = method
            captured["body"] = body
            return _comment_response("**Looks good**")

        client.request = fake_request  # type: ignore[method-assign]

        result = await client.comments.create(
            parent={"type": "page_id", "page_id": "page_123"},
            markdown="**Looks good**",
        )

        assert isinstance(result, CommentObject)
        assert captured["path"] == "comments"
        assert captured["method"] == "post"
        assert captured["body"] == {
            "parent": {"type": "page_id", "page_id": "page_123"},
            "markdown": "**Looks good**",
        }

    @pytest.mark.asyncio
    async def test_update_comment_uses_patch(self):
        client = NotionAsyncClient(auth="test-token")
        captured: dict = {}

        async def fake_request(*, path, method, body=None, auth=None, **kwargs):
            captured["path"] = path
            captured["method"] = method
            captured["body"] = body
            return _comment_response("Updated")

        client.request = fake_request  # type: ignore[method-assign]

        await client.comments.update(comment_id="comment_123", markdown="Updated")

        assert captured["path"] == "comments/comment_123"
        assert captured["method"] == "patch"
        assert captured["body"] == {"markdown": "Updated"}

    @pytest.mark.asyncio
    async def test_delete_comment_uses_delete(self):
        client = NotionAsyncClient(auth="test-token")
        captured: dict = {}

        async def fake_request(*, path, method, auth=None, **kwargs):
            captured["path"] = path
            captured["method"] = method
            return _comment_response("Deleted")

        client.request = fake_request  # type: ignore[method-assign]

        result = await client.comments.delete(comment_id="comment_123")

        assert isinstance(result, CommentObject)
        assert captured["path"] == "comments/comment_123"
        assert captured["method"] == "delete"

    @pytest.mark.asyncio
    async def test_comment_content_requires_exactly_one_body_format(self):
        client = NotionAsyncClient(auth="test-token")

        with pytest.raises(ValueError, match="rich_text or markdown"):
            await client.comments.update(comment_id="comment_123")


class TestMeetingNotesAPI:
    """Test meeting notes query helper."""

    @pytest.mark.asyncio
    async def test_query_meeting_notes(self):
        client = NotionAsyncClient(auth="test-token")
        captured: dict = {}

        async def fake_request(*, path, method, body=None, auth=None, **kwargs):
            captured["path"] = path
            captured["method"] = method
            captured["body"] = body
            return {
                "object": "list",
                "results": [
                    {
                        "object": "block",
                        "id": "meeting_notes_123",
                        "type": "meeting_notes",
                        "created_time": "2026-05-01T00:00:00.000Z",
                        "last_edited_time": "2026-05-01T00:00:00.000Z",
                        "created_by": {"object": "user", "id": "user_123"},
                        "last_edited_by": {"object": "user", "id": "user_123"},
                        "parent": {"type": "agent_id", "agent_id": "agent_123"},
                        "has_children": True,
                        "in_trash": False,
                        "meeting_notes": {
                            "title": _rich_text("Weekly sync"),
                            "status": "notes_ready",
                        },
                    }
                ],
                "has_more": False,
                "request_status": {"type": "complete"},
            }

        client.request = fake_request  # type: ignore[method-assign]

        result = await client.blocks.meetingNotes.query(
            sort=[{"property": "last_edited_time", "direction": "descending"}],
            limit=10,
        )

        assert isinstance(result, QueryMeetingNotesResponse)
        assert captured["path"] == "blocks/meeting_notes/query"
        assert captured["method"] == "post"
        assert captured["body"] == {
            "sort": [{"property": "last_edited_time", "direction": "descending"}],
            "limit": 10,
        }
        assert isinstance(result.results[0], MeetingNotesBlock)
        assert result.results[0].parent["type"] == "agent_id"
