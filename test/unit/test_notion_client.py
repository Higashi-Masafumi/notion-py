"""Unit tests for client facade additions and defaults."""

import pytest
from pydantic import ValidationError

from notion_py_client.blocks.special_blocks import MeetingNotesBlock
from notion_py_client.notion_client import APIErrorCode, NotionAsyncClient
from notion_py_client.requests.page_requests import (
    MovePageParameters,
    ReplaceContentMarkdownCommand,
)
from notion_py_client.responses.async_task import AsyncTaskResponse
from notion_py_client.responses.list_response import (
    CommentObject,
    PartialCommentObject,
    QueryMeetingNotesResponse,
)
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

    def test_api_error_code_includes_gateway_timeout(self):
        assert APIErrorCode.GatewayTimeout == "gateway_timeout"


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


class TestMovePageAPI:
    """Test the move-a-page facade (POST /pages/{page_id}/move)."""

    @pytest.mark.asyncio
    async def test_move_page_to_new_parent(self):
        client = NotionAsyncClient(auth="test-token")
        captured: dict = {}

        async def fake_request(*, path, method, body=None, auth=None, **kwargs):
            captured["path"] = path
            captured["method"] = method
            captured["body"] = body
            return {
                "object": "page",
                "id": "page_123",
                "created_time": "2026-05-01T00:00:00.000Z",
                "last_edited_time": "2026-05-01T00:00:00.000Z",
                "created_by": {"object": "user", "id": "user_123"},
                "last_edited_by": {"object": "user", "id": "user_123"},
                "parent": {"type": "page_id", "page_id": "new_parent_123"},
                "in_trash": False,
                "is_locked": False,
                "properties": {},
                "url": "https://www.notion.so/page_123",
            }

        client.request = fake_request  # type: ignore[method-assign]

        result = await client.pages.move(
            MovePageParameters(
                page_id="page_123",
                parent={"type": "page_id", "page_id": "new_parent_123"},
            )
        )

        assert captured["path"] == "pages/page_123/move"
        assert captured["method"] == "post"
        assert captured["body"] == {
            "parent": {"type": "page_id", "page_id": "new_parent_123"},
        }
        assert result.parent["page_id"] == "new_parent_123"


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


class TestAsyncTasksAPI:
    """Test async task status retrieval facade."""

    @pytest.mark.asyncio
    async def test_retrieve_running_task(self):
        client = NotionAsyncClient(auth="test-token")
        captured: dict = {}

        async def fake_request(*, path, method, auth=None, **kwargs):
            captured["path"] = path
            captured["method"] = method
            return {
                "object": "async_task",
                "id": "task_123",
                "status_url": "https://api.notion.com/v1/async_tasks/task_123",
                "created_time": "2026-07-01T00:00:00.000Z",
                "operation": {"surface": "pages", "name": "create"},
                "status": "running",
                "poll_after_seconds": 2,
            }

        client.request = fake_request  # type: ignore[method-assign]

        result = await client.asyncTasks.retrieve(task_id="task_123")

        assert isinstance(result, AsyncTaskResponse)
        assert captured["path"] == "async_tasks/task_123"
        assert captured["method"] == "get"
        assert result.status == "running"
        assert result.poll_after_seconds == 2
        assert result.result is None
        assert result.error is None

    @pytest.mark.asyncio
    async def test_retrieve_failed_task(self):
        client = NotionAsyncClient(auth="test-token")

        async def fake_request(*, path, method, auth=None, **kwargs):
            return {
                "object": "async_task",
                "id": "task_123",
                "status_url": "https://api.notion.com/v1/async_tasks/task_123",
                "created_time": "2026-07-01T00:00:00.000Z",
                "operation": {"surface": "pages", "name": "create"},
                "status": "failed",
                "error": {
                    "object": "error",
                    "status": 400,
                    "code": "validation_error",
                    "message": "Invalid request",
                },
            }

        client.request = fake_request  # type: ignore[method-assign]

        result = await client.asyncTasks.retrieve(task_id="task_123")

        assert result.status == "failed"
        assert result.error is not None
        assert result.error.code == "validation_error"


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
    async def test_update_comment_accepts_partial_response(self):
        client = NotionAsyncClient(auth="test-token")

        async def fake_request(*, path, method, body=None, auth=None, **kwargs):
            return {"object": "comment", "id": "comment_123"}

        client.request = fake_request  # type: ignore[method-assign]

        result = await client.comments.update(
            comment_id="comment_123", markdown="Updated"
        )

        assert isinstance(result, PartialCommentObject)
        assert result.id == "comment_123"

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
    async def test_delete_comment_accepts_partial_response(self):
        client = NotionAsyncClient(auth="test-token")

        async def fake_request(*, path, method, auth=None, **kwargs):
            return {"object": "comment", "id": "comment_123"}

        client.request = fake_request  # type: ignore[method-assign]

        result = await client.comments.delete(comment_id="comment_123")

        assert isinstance(result, PartialCommentObject)
        assert result.id == "comment_123"

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
