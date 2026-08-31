"""Unit tests for recent Notion API changelog surfaces."""

import pytest
from pydantic import ValidationError

from notion_py_client.api_types import SearchObjectFilter, SearchParameters, SearchTrashFilter
from notion_py_client.filters import VerificationPropertyStatusFilter
from notion_py_client.models.user import Person
from notion_py_client.notion_client import APIErrorCode, NotionAsyncClient
from notion_py_client.properties import FormulaProperty, RollupProperty
from notion_py_client.requests.page_requests import (
    CreatePageParameters,
    MarkdownContentUpdateRequest,
    UpdateContentMarkdownCommand,
    UpdatePageParameters,
)
from notion_py_client.responses.page import NotionPage
from notion_py_client.schema import StatusOptionConfig
from notion_py_client.utils import is_full_data_source, is_full_database, is_full_page_or_data_source


def _page_payload(**overrides) -> dict:
    payload = {
        "object": "page",
        "id": "page_123",
        "created_time": "2026-08-01T00:00:00.000Z",
        "last_edited_time": "2026-08-01T00:00:00.000Z",
        "created_by": {"object": "user", "id": "user_123"},
        "last_edited_by": {"object": "user", "id": "user_123"},
        "parent": {"type": "database_id", "database_id": "db_123"},
        "in_trash": False,
        "is_archived": False,
        "is_locked": False,
        "properties": {},
        "url": "https://www.notion.so/page_123",
    }
    payload.update(overrides)
    return payload


class TestApiErrorCodes:
    def test_invalid_beta_is_typed(self):
        assert APIErrorCode.InvalidBeta == "invalid_beta"


class TestFullObjectGuards:
    def test_full_data_source_requires_title(self):
        assert is_full_data_source(
            {
                "object": "data_source",
                "id": "ds_123",
                "title": [{"type": "text", "text": {"content": "Tasks"}}],
            }
        )
        assert not is_full_data_source({"object": "data_source", "id": "ds_123"})

    def test_full_database_requires_title(self):
        assert is_full_database(
            {
                "object": "database",
                "id": "db_123",
                "title": [{"type": "text", "text": {"content": "Projects"}}],
            }
        )
        assert not is_full_database({"object": "database", "id": "db_123"})

    def test_full_page_or_data_source_uses_title_for_data_sources(self):
        assert not is_full_page_or_data_source({"object": "data_source", "id": "ds_123"})


class TestPageWriteFilterProperties:
    @pytest.mark.asyncio
    async def test_create_sends_filter_properties_as_query(self):
        client = NotionAsyncClient(auth="test-token")
        captured: dict = {}

        async def fake_request(*, path, method, body=None, query=None, auth=None, **kwargs):
            captured.update(path=path, method=method, body=body, query=query)
            return _page_payload()

        client.request = fake_request  # type: ignore[method-assign]

        result = await client.pages.create(
            CreatePageParameters(
                parent={"type": "database_id", "database_id": "db_123"},
                properties={},
                filter_properties=["title", "status"],
            )
        )

        assert captured["path"] == "pages"
        assert captured["query"] == {"filter_properties": ["title", "status"]}
        assert "filter_properties" not in captured["body"]
        assert isinstance(result, NotionPage)

    @pytest.mark.asyncio
    async def test_update_sends_filter_properties_as_query(self):
        client = NotionAsyncClient(auth="test-token")
        captured: dict = {}

        async def fake_request(*, path, method, body=None, query=None, auth=None, **kwargs):
            captured.update(path=path, method=method, body=body, query=query)
            return _page_payload()

        client.request = fake_request  # type: ignore[method-assign]

        await client.pages.update(
            UpdatePageParameters(
                page_id="page_123",
                in_trash=True,
                filter_properties=["title"],
            )
        )

        assert captured["path"] == "pages/page_123"
        assert captured["query"] == {"filter_properties": ["title"]}
        assert captured["body"] == {"in_trash": True}


class TestVerificationFilter:
    def test_status_and_does_not_equal(self):
        status_filter: VerificationPropertyStatusFilter = {"status": "verified"}
        inequality_filter: VerificationPropertyStatusFilter = {
            "does_not_equal": "expired"
        }

        assert status_filter["status"] == "verified"
        assert inequality_filter["does_not_equal"] == "expired"


class TestUnsupportedComputedValues:
    def test_formula_unsupported_parses_and_has_no_display_value(self):
        prop = FormulaProperty.model_validate(
            {
                "id": "formula_1",
                "type": "formula",
                "formula": {"type": "unsupported", "unsupported": {}},
            }
        )

        assert prop.formula.type == "unsupported"
        assert prop.get_display_value() is None

    def test_rollup_unsupported_parses_and_has_no_display_value(self):
        prop = RollupProperty.model_validate(
            {
                "id": "rollup_1",
                "type": "rollup",
                "rollup": {
                    "type": "unsupported",
                    "unsupported": {},
                    "function": "sum",
                },
            }
        )

        assert prop.rollup.type == "unsupported"
        assert prop.get_display_value() is None


class TestMeetingNotesCreate:
    @pytest.mark.asyncio
    async def test_create_from_file_upload(self):
        client = NotionAsyncClient(auth="test-token")
        captured: dict = {}

        async def fake_request(*, path, method, body=None, auth=None, **kwargs):
            captured.update(path=path, method=method, body=body)
            return {
                "object": "block",
                "id": "meeting_notes_123",
                "type": "meeting_notes",
                "created_time": "2026-08-01T00:00:00.000Z",
                "last_edited_time": "2026-08-01T00:00:00.000Z",
                "created_by": {"object": "user", "id": "user_123"},
                "last_edited_by": {"object": "user", "id": "user_123"},
                "parent": {"type": "page_id", "page_id": "page_123"},
                "has_children": True,
                "in_trash": False,
                "meeting_notes": {"title": [], "status": "processing"},
            }

        client.request = fake_request  # type: ignore[method-assign]

        result = await client.blocks.meetingNotes.create(
            source={"type": "file_upload", "file_upload_id": "file_123"},
            parent={"type": "page_id", "page_id": "page_123"},
        )

        assert captured["path"] == "blocks/meeting_notes"
        assert captured["method"] == "post"
        assert captured["body"]["source"]["file_upload_id"] == "file_123"
        assert result.id == "meeting_notes_123"

    @pytest.mark.asyncio
    async def test_file_upload_without_parent_raises(self):
        client = NotionAsyncClient(auth="test-token")

        with pytest.raises(ValueError, match="parent is required"):
            await client.blocks.meetingNotes.create(
                source={"type": "file_upload", "file_upload_id": "file_123"},
            )

    @pytest.mark.asyncio
    async def test_block_source_rejects_parent(self):
        client = NotionAsyncClient(auth="test-token")

        with pytest.raises(ValueError, match="parent is not accepted"):
            await client.blocks.meetingNotes.create(
                source={"type": "block", "block_id": "block_123"},
                parent={"type": "page_id", "page_id": "page_123"},
            )


class TestSearchTrashFilter:
    def test_standalone_and_combined_filters(self):
        trash_only: SearchTrashFilter = {"in_trash": True}
        pages_in_trash: SearchObjectFilter = {
            "property": "object",
            "value": "page",
            "in_trash": True,
        }
        params: SearchParameters = {"query": "notes", "filter": trash_only}

        assert trash_only["in_trash"] is True
        assert pages_in_trash["value"] == "page"
        assert params["filter"] == trash_only


class TestArchivedQueryAndPageField:
    @pytest.mark.asyncio
    async def test_query_sends_is_archived(self):
        client = NotionAsyncClient(auth="test-token")
        captured: dict = {}

        async def fake_request(*, path, method, body=None, auth=None, **kwargs):
            captured.update(path=path, method=method, body=body)
            return {
                "object": "list",
                "results": [],
                "has_more": False,
                "next_cursor": None,
            }

        client.request = fake_request  # type: ignore[method-assign]

        await client.dataSources.query(data_source_id="ds_123", is_archived=True)

        assert captured["path"] == "data_sources/ds_123/query"
        assert captured["body"]["is_archived"] is True

    def test_page_parses_is_archived(self):
        page = NotionPage.model_validate(_page_payload(is_archived=True))
        assert page.is_archived is True


class TestPersonEmailVerified:
    def test_person_parses_email_verified(self):
        person = Person.model_validate(
            {"email": "user@example.com", "email_verified": True}
        )
        assert person.email_verified is True


class TestStatusOptionGroup:
    def test_write_side_group(self):
        option = StatusOptionConfig(
            id="opt_1",
            name="Ready",
            color="blue",
            group="To-do",
        )
        assert option.group == "To-do"


class TestMarkdownOldStr:
    def test_empty_old_str_is_rejected(self):
        with pytest.raises(ValidationError, match="old_str must be a non-empty string"):
            MarkdownContentUpdateRequest(old_str="", new_str="replacement")

    def test_update_content_rejects_empty_old_str(self):
        with pytest.raises(ValidationError, match="old_str must be a non-empty string"):
            UpdateContentMarkdownCommand(
                update_content={
                    "content_updates": [{"old_str": "", "new_str": "x"}],
                }
            )
