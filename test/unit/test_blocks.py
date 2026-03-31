"""Unit tests for block response parsing and block API helpers."""

import pytest
from pydantic import TypeAdapter

from notion_py_client.blocks import BlockObject
from notion_py_client.blocks.special_blocks import MeetingNotesBlock, TranscriptionBlock
from notion_py_client.notion_client import NotionAsyncClient


class TestMeetingNotesBlocks:
    """Test parsing meeting_notes/transcription blocks."""

    def test_parse_meeting_notes_block(self):
        data = {
            "object": "block",
            "id": "block_123",
            "type": "meeting_notes",
            "created_time": "2026-02-24T10:00:00.000Z",
            "last_edited_time": "2026-02-24T10:45:00.000Z",
            "created_by": {"object": "user", "id": "user_123"},
            "last_edited_by": {"object": "user", "id": "user_123"},
            "parent": {"type": "page_id", "page_id": "page_123"},
            "has_children": True,
            "in_trash": False,
            "meeting_notes": {
                "title": [
                    {
                        "type": "text",
                        "text": {"content": "Team Sync", "link": None},
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default",
                        },
                        "plain_text": "Team Sync",
                        "href": None,
                    }
                ],
                "status": "notes_ready",
                "children": {
                    "summary_block_id": "a1",
                    "notes_block_id": "b2",
                    "transcript_block_id": "c3",
                },
            },
        }

        result = TypeAdapter(BlockObject).validate_python(data)

        assert isinstance(result, MeetingNotesBlock)
        assert result.meeting_notes.status == "notes_ready"
        assert result.meeting_notes.children is not None
        assert result.meeting_notes.children.transcript_block_id == "c3"

    def test_parse_transcription_block(self):
        data = {
            "object": "block",
            "id": "block_legacy",
            "type": "transcription",
            "created_time": "2026-02-24T10:00:00.000Z",
            "last_edited_time": "2026-02-24T10:45:00.000Z",
            "created_by": {"object": "user", "id": "user_123"},
            "last_edited_by": {"object": "user", "id": "user_123"},
            "parent": {"type": "page_id", "page_id": "page_123"},
            "has_children": True,
            "archived": False,
            "transcription": {
                "status": "summary_in_progress",
            },
        }

        result = TypeAdapter(BlockObject).validate_python(data)

        assert isinstance(result, TranscriptionBlock)
        assert result.in_trash is False
        assert result.archived is False
        assert result.transcription.status == "summary_in_progress"


class TestBlockChildrenAPI:
    """Test append block children request shaping."""

    @pytest.mark.asyncio
    async def test_append_uses_position_object_for_after(self):
        client = NotionAsyncClient(auth="test-token")
        captured: dict = {}

        async def fake_request(*, path, method, body=None, auth=None, **kwargs):
            captured["path"] = path
            captured["method"] = method
            captured["body"] = body
            return {
                "object": "list",
                "results": [],
                "next_cursor": None,
                "has_more": False,
            }

        client.request = fake_request  # type: ignore[method-assign]

        await client.blocks.children.append(
            block_id="block_123",
            children=[],
            after="after_block_123",
        )

        assert captured["path"] == "blocks/block_123/children"
        assert captured["method"] == "patch"
        assert captured["body"]["position"] == {
            "type": "after_block",
            "after_block": {"id": "after_block_123"},
        }

