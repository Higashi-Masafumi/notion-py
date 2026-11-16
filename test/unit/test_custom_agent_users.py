"""Custom Agent bot users in people properties and mentions."""

from pydantic import TypeAdapter

from notion_py_client.models.primitives.mention import Mention
from notion_py_client.models.rich_text_item import RichTextItem
from notion_py_client.models.user import BotUser, PersonUser
from notion_py_client.properties.base_properties.people_property import PeopleProperty
from notion_py_client.requests.common import PartialUserObjectRequest
from notion_py_client.requests.property_requests import PeoplePropertyRequest
from notion_py_client.responses.page import NotionPage
from notion_py_client.responses.property_item import PeoplePropertyItem, PropertyItemObject

AGENT_ID = "ef82a3bc-58dc-47ca-8ab6-56d144d166cc"
BOT_USER_ID = "9188c6a5-7381-452f-b3dc-d4865aa89bdf"


def _page(people: list[dict]) -> dict:
    return {
        "object": "page",
        "id": "page_123",
        "created_time": "2026-11-10T00:00:00.000Z",
        "last_edited_time": "2026-11-10T00:00:00.000Z",
        "created_by": {"object": "user", "id": "user_123"},
        "last_edited_by": {"object": "user", "id": "user_123"},
        "parent": {"type": "page_id", "page_id": "parent_123"},
        "in_trash": False,
        "is_locked": False,
        "properties": {
            "Assignee": {
                "id": "prop_people",
                "type": "people",
                "people": people,
            }
        },
        "url": "https://www.notion.so/page_123",
    }


def _agent_bot() -> dict:
    return {
        "object": "user",
        "id": BOT_USER_ID,
        "type": "bot",
        "name": "Triage Agent",
        "avatar_url": None,
        "agent_id": AGENT_ID,
        "bot": {},
    }


class TestBotUserAgentId:
    def test_custom_agent_bot_keeps_agent_id(self):
        user = BotUser.model_validate(_agent_bot())

        assert user.id == BOT_USER_ID
        assert user.agent_id == AGENT_ID
        assert user.avatar_url is None
        assert user.type == "bot"

    def test_integration_bot_omits_agent_id(self):
        user = BotUser.model_validate(
            {
                "object": "user",
                "id": "bot_integration",
                "type": "bot",
                "name": "My Integration",
                "avatar_url": "https://example.com/avatar.png",
                "bot": {
                    "owner": {"type": "workspace", "workspace": True},
                    "workspace_name": "My Workspace",
                    "workspace_limits": {"max_file_upload_size_in_bytes": 5242880},
                },
            }
        )

        assert user.agent_id is None
        assert user.bot.workspace_name == "My Workspace"


class TestPeoplePropertyCustomAgent:
    def test_page_people_property_keeps_agent_and_bot_ids(self):
        page = NotionPage.model_validate(
            _page(
                [
                    {
                        "object": "user",
                        "id": "user_123",
                        "type": "person",
                        "name": "Ada Lovelace",
                        "avatar_url": None,
                        "person": {"email": "ada@example.com"},
                    },
                    _agent_bot(),
                ]
            )
        )

        people = page.properties["Assignee"]
        assert isinstance(people, PeopleProperty)
        assert isinstance(people.people[0], PersonUser)
        assert not hasattr(people.people[0], "agent_id")
        agent = people.people[1]
        assert isinstance(agent, BotUser)
        assert agent.id == BOT_USER_ID
        assert agent.agent_id == AGENT_ID
        assert people.get_display_value() == "Ada Lovelace, Triage Agent"

    def test_property_item_keeps_agent_id(self):
        result = TypeAdapter(PropertyItemObject).validate_python(
            {
                "object": "property_item",
                "id": "prop_people",
                "type": "people",
                "people": _agent_bot(),
            }
        )

        assert isinstance(result, PeoplePropertyItem)
        assert isinstance(result.people, BotUser)
        assert result.people.agent_id == AGENT_ID
        assert result.people.id == BOT_USER_ID


class TestUserMentionCustomAgent:
    def test_user_mention_keeps_agent_id(self):
        item = RichTextItem.model_validate(
            {
                "type": "mention",
                "mention": {"type": "user", "user": _agent_bot()},
                "annotations": {
                    "bold": False,
                    "italic": False,
                    "strikethrough": False,
                    "underline": False,
                    "code": False,
                    "color": "default",
                },
                "plain_text": "@Triage Agent",
                "href": None,
            }
        )

        assert isinstance(item.mention, Mention)
        assert isinstance(item.mention.user, BotUser)
        assert item.mention.user.agent_id == AGENT_ID
        assert item.mention.user.id == BOT_USER_ID


class TestPeoplePropertyRequestCustomAgent:
    def test_agent_id_uses_existing_user_id_field(self):
        request = PeoplePropertyRequest(
            people=[
                PartialUserObjectRequest(id="user_123"),
                PartialUserObjectRequest(id=AGENT_ID),
            ]
        )

        assert request.model_dump(exclude_none=True) == {
            "people": [{"id": "user_123"}, {"id": AGENT_ID}]
        }
