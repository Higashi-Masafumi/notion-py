"""Unit tests for block response parsing and block API helpers."""

import pytest
from pydantic import TypeAdapter

from notion_py_client.blocks import BlockObject
from notion_py_client.blocks.layout_blocks import TabBlock
from notion_py_client.blocks.special_blocks import MeetingNotesBlock
from notion_py_client.blocks.text_blocks import Heading4Block, ParagraphBlock
from notion_py_client.models.icon import IconType
from notion_py_client.notion_client import NotionAsyncClient


class TestMeetingNotesBlocks:
    """Test parsing meeting_notes blocks."""

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

    def test_parse_heading_4_block(self):
        data = {
            "object": "block",
            "id": "block_heading_4",
            "type": "heading_4",
            "created_time": "2026-03-30T10:00:00.000Z",
            "last_edited_time": "2026-03-30T10:00:00.000Z",
            "created_by": {"object": "user", "id": "user_123"},
            "last_edited_by": {"object": "user", "id": "user_123"},
            "parent": {"type": "page_id", "page_id": "page_123"},
            "has_children": False,
            "in_trash": False,
            "heading_4": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": "Deep section", "link": None},
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default",
                        },
                        "plain_text": "Deep section",
                        "href": None,
                    }
                ],
                "color": "default",
                "is_toggleable": False,
            },
        }

        result = TypeAdapter(BlockObject).validate_python(data)

        assert isinstance(result, Heading4Block)
        assert result.heading_4.rich_text[0].plain_text == "Deep section"

    def test_parse_tab_block_with_iconized_paragraph_child(self):
        tab_data = {
            "object": "block",
            "id": "tab_123",
            "type": "tab",
            "created_time": "2026-03-25T10:00:00.000Z",
            "last_edited_time": "2026-03-25T10:00:00.000Z",
            "created_by": {"object": "user", "id": "user_123"},
            "last_edited_by": {"object": "user", "id": "user_123"},
            "parent": {"type": "page_id", "page_id": "page_123"},
            "has_children": True,
            "in_trash": False,
            "tab": {},
        }
        paragraph_data = {
            "object": "block",
            "id": "tab_label_123",
            "type": "paragraph",
            "created_time": "2026-03-25T10:00:00.000Z",
            "last_edited_time": "2026-03-25T10:00:00.000Z",
            "created_by": {"object": "user", "id": "user_123"},
            "last_edited_by": {"object": "user", "id": "user_123"},
            "parent": {"type": "block_id", "block_id": "tab_123"},
            "has_children": True,
            "in_trash": False,
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": "Overview", "link": None},
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default",
                        },
                        "plain_text": "Overview",
                        "href": None,
                    }
                ],
                "color": "default",
                "icon": {
                    "type": "icon",
                    "icon": {"name": "bulb", "color": "yellow"},
                },
            },
        }

        tab_result = TypeAdapter(BlockObject).validate_python(tab_data)
        paragraph_result = TypeAdapter(BlockObject).validate_python(paragraph_data)

        assert isinstance(tab_result, TabBlock)
        assert isinstance(paragraph_result, ParagraphBlock)
        assert paragraph_result.paragraph.icon is not None
        assert paragraph_result.paragraph.icon.type == IconType.ICON
        assert paragraph_result.paragraph.icon.icon is not None
        assert paragraph_result.paragraph.icon.icon.name == "bulb"


class TestBlockChildrenAPI:
    """Test append block children request shaping."""

    @pytest.mark.asyncio
    async def test_append_uses_position_object(self):
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
            position={
                "type": "after_block",
                "after_block": {"id": "after_block_123"},
            },
        )

        assert captured["path"] == "blocks/block_123/children"
        assert captured["method"] == "patch"
        assert captured["body"]["position"] == {
            "type": "after_block",
            "after_block": {"id": "after_block_123"},
        }
