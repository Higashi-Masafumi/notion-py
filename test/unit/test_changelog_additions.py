"""Unit tests for recent Notion API changelog additions."""

import pytest

from notion_py_client.models.user import Person, PersonUser
from notion_py_client.notion_client import NotionAsyncClient
from notion_py_client.responses.page import NotionPage
from notion_py_client.schema.property_configs.base_configs.status_config import (
    StatusOptionConfig,
    StatusPropertyConfig,
)


def _page_payload(*, is_archived: bool = False) -> dict:
    return {
        "object": "page",
        "id": "page_123",
        "created_time": "2025-01-01T00:00:00.000Z",
        "last_edited_time": "2025-01-02T00:00:00.000Z",
        "created_by": {"object": "user", "id": "user_123"},
        "last_edited_by": {"object": "user", "id": "user_123"},
        "parent": {"type": "data_source_id", "data_source_id": "ds_123"},
        "in_trash": False,
        "is_archived": is_archived,
        "is_locked": False,
        "properties": {},
        "url": "https://app.notion.com/p/page_123",
    }


class TestSearchInTrash:
    @pytest.mark.asyncio
    async def test_search_passes_in_trash_filter(self):
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

        await client.search({"filter": {"in_trash": True}})

        assert captured["path"] == "search"
        assert captured["method"] == "post"
        assert captured["body"]["filter"]["in_trash"] is True


class TestDataSourceQueryArchived:
    @pytest.mark.asyncio
    async def test_query_passes_is_archived(self):
        client = NotionAsyncClient(auth="test-token")
        captured: dict = {}

        async def fake_request(*, path, method, body=None, auth=None, **kwargs):
            captured["path"] = path
            captured["method"] = method
            captured["body"] = body
            return {
                "object": "list",
                "results": [_page_payload(is_archived=True)],
                "next_cursor": None,
                "has_more": False,
            }

        client.request = fake_request  # type: ignore[method-assign]

        response = await client.dataSources.query(
            data_source_id="ds_123",
            is_archived=True,
        )

        assert captured["path"] == "data_sources/ds_123/query"
        assert captured["body"]["is_archived"] is True
        assert len(response.results) == 1
        assert isinstance(response.results[0], NotionPage)
        assert response.results[0].is_archived is True


class TestPageIsArchived:
    def test_parse_is_archived(self):
        page = NotionPage.model_validate(_page_payload(is_archived=True))
        assert page.is_archived is True
        assert page.in_trash is False

    def test_defaults_is_archived_false_when_omitted(self):
        data = _page_payload()
        del data["is_archived"]
        page = NotionPage.model_validate(data)
        assert page.is_archived is False


class TestPersonEmailVerified:
    def test_parse_email_verified(self):
        user = PersonUser.model_validate(
            {
                "object": "user",
                "id": "user_123",
                "type": "person",
                "name": "Ada",
                "avatar_url": None,
                "person": {
                    "email": "ada@example.com",
                    "email_verified": True,
                },
            }
        )
        assert isinstance(user.person, Person)
        assert user.person.email == "ada@example.com"
        assert user.person.email_verified is True


class TestStatusOptionGroup:
    def test_create_option_with_group(self):
        option = StatusOptionConfig(
            name="Blocked",
            color="red",
            group="In progress",
        )
        payload = option.model_dump(exclude_none=True)
        assert payload == {
            "name": "Blocked",
            "color": "red",
            "group": "In progress",
        }

    def test_property_config_accepts_grouped_options(self):
        config = StatusPropertyConfig.model_validate(
            {
                "id": "status",
                "name": "Status",
                "type": "status",
                "status": {
                    "options": [
                        {
                            "id": "opt_1",
                            "name": "Review",
                            "color": "yellow",
                            "group": "In progress",
                        }
                    ],
                    "groups": [
                        {
                            "id": "grp_1",
                            "name": "In progress",
                            "color": "blue",
                            "option_ids": ["opt_1"],
                        }
                    ],
                },
            }
        )
        assert config.status.options[0].group == "In progress"
