"""Unit tests for PropertyItem response types."""

import pytest
from pydantic import TypeAdapter
from notion_py_client.responses.property_item import (
    PropertyItemObject,
    PropertyItemListResponse,
    NumberPropertyItem,
    UrlPropertyItem,
    SelectPropertyItem,
    StatusPropertyItem,
    DatePropertyItem,
    EmailPropertyItem,
    PhoneNumberPropertyItem,
    CheckboxPropertyItem,
    TitlePropertyItem,
    RichTextPropertyItem,
    PeoplePropertyItem,
)


class TestNumberPropertyItem:
    """Test NumberPropertyItem."""

    def test_parse_number_property_item(self):
        """Test parsing a number property item from API response."""
        data = {
            "object": "property_item",
            "id": "prop_123",
            "type": "number",
            "number": 42.5,
        }

        adapter = TypeAdapter(PropertyItemObject)
        result = adapter.validate_python(data)

        assert isinstance(result, NumberPropertyItem)
        assert result.type == "number"
        assert result.number == 42.5
        assert result.id == "prop_123"

    def test_parse_null_number_property_item(self):
        """Test parsing a number property item with null value."""
        data = {
            "object": "property_item",
            "id": "prop_456",
            "type": "number",
            "number": None,
        }

        adapter = TypeAdapter(PropertyItemObject)
        result = adapter.validate_python(data)

        assert isinstance(result, NumberPropertyItem)
        assert result.number is None


class TestUrlPropertyItem:
    """Test UrlPropertyItem."""

    def test_parse_url_property_item(self):
        """Test parsing a URL property item."""
        data = {
            "object": "property_item",
            "id": "prop_url",
            "type": "url",
            "url": "https://example.com",
        }

        adapter = TypeAdapter(PropertyItemObject)
        result = adapter.validate_python(data)

        assert isinstance(result, UrlPropertyItem)
        assert result.type == "url"
        assert result.url == "https://example.com"


class TestSelectPropertyItem:
    """Test SelectPropertyItem."""

    def test_parse_select_property_item(self):
        """Test parsing a select property item."""
        data = {
            "object": "property_item",
            "id": "prop_select",
            "type": "select",
            "select": {
                "id": "option_1",
                "name": "Option A",
                "color": "blue",
            },
        }

        adapter = TypeAdapter(PropertyItemObject)
        result = adapter.validate_python(data)

        assert isinstance(result, SelectPropertyItem)
        if result.select is not None:
            assert result.select.id == "option_1"
            assert result.select.name == "Option A"
            assert result.select.color == "blue"



class TestStatusPropertyItem:
    """Test StatusPropertyItem."""

    def test_parse_status_property_item(self):
        """Test parsing a status property item."""
        data = {
            "object": "property_item",
            "id": "prop_status",
            "type": "status",
            "status": {
                "id": "status_1",
                "name": "In Progress",
                "color": "yellow",
            },
        }

        adapter = TypeAdapter(PropertyItemObject)
        result = adapter.validate_python(data)

        assert isinstance(result, StatusPropertyItem)
        assert result.status is not None
        assert result.status.name == "In Progress"


class TestDatePropertyItem:
    """Test DatePropertyItem."""

    def test_parse_date_property_item(self):
        """Test parsing a date property item."""
        data = {
            "object": "property_item",
            "id": "prop_date",
            "type": "date",
            "date": {
                "start": "2025-01-01",
                "end": "2025-01-31",
                "time_zone": "Asia/Tokyo",
            },
        }

        adapter = TypeAdapter(PropertyItemObject)
        result = adapter.validate_python(data)

        assert isinstance(result, DatePropertyItem)
        assert result.date is not None
        assert result.date.start == "2025-01-01"
        assert result.date.end == "2025-01-31"
        assert result.date.time_zone == "Asia/Tokyo"


class TestEmailPropertyItem:
    """Test EmailPropertyItem."""

    def test_parse_email_property_item(self):
        """Test parsing an email property item."""
        data = {
            "object": "property_item",
            "id": "prop_email",
            "type": "email",
            "email": "test@example.com",
        }

        adapter = TypeAdapter(PropertyItemObject)
        result = adapter.validate_python(data)

        assert isinstance(result, EmailPropertyItem)
        assert result.email == "test@example.com"


class TestPhoneNumberPropertyItem:
    """Test PhoneNumberPropertyItem."""

    def test_parse_phone_number_property_item(self):
        """Test parsing a phone number property item."""
        data = {
            "object": "property_item",
            "id": "prop_phone",
            "type": "phone_number",
            "phone_number": "+81-90-1234-5678",
        }

        adapter = TypeAdapter(PropertyItemObject)
        result = adapter.validate_python(data)

        assert isinstance(result, PhoneNumberPropertyItem)
        assert result.phone_number == "+81-90-1234-5678"


class TestCheckboxPropertyItem:
    """Test CheckboxPropertyItem."""

    def test_parse_checkbox_property_item_true(self):
        """Test parsing a checkbox property item (checked)."""
        data = {
            "object": "property_item",
            "id": "prop_checkbox",
            "type": "checkbox",
            "checkbox": True,
        }

        adapter = TypeAdapter(PropertyItemObject)
        result = adapter.validate_python(data)

        assert isinstance(result, CheckboxPropertyItem)
        assert result.checkbox is True

    def test_parse_checkbox_property_item_false(self):
        """Test parsing a checkbox property item (unchecked)."""
        data = {
            "object": "property_item",
            "id": "prop_checkbox2",
            "type": "checkbox",
            "checkbox": False,
        }

        adapter = TypeAdapter(PropertyItemObject)
        result = adapter.validate_python(data)

        assert isinstance(result, CheckboxPropertyItem)
        assert result.checkbox is False


class TestTitlePropertyItem:
    """Test TitlePropertyItem."""

    def test_parse_title_property_item(self):
        """Test parsing a title property item."""
        data = {
            "object": "property_item",
            "id": "prop_title",
            "type": "title",
            "title": {
                "type": "text",
                "text": {"content": "Page Title", "link": None},
                "plain_text": "Page Title",
                "href": None,
                "annotations": {
                    "bold": False,
                    "italic": False,
                    "strikethrough": False,
                    "underline": False,
                    "code": False,
                    "color": "default",
                },
            },
        }

        adapter = TypeAdapter(PropertyItemObject)
        result = adapter.validate_python(data)

        assert isinstance(result, TitlePropertyItem)
        assert result.title.plain_text == "Page Title"


class TestRichTextPropertyItem:
    """Test RichTextPropertyItem."""

    def test_parse_rich_text_property_item(self):
        """Test parsing a rich text property item."""
        data = {
            "object": "property_item",
            "id": "prop_richtext",
            "type": "rich_text",
            "rich_text": {
                "type": "text",
                "text": {"content": "Rich content", "link": None},
                "plain_text": "Rich content",
                "href": None,
                "annotations": {
                    "bold": True,
                    "italic": False,
                    "strikethrough": False,
                    "underline": False,
                    "code": False,
                    "color": "default",
                },
            },
        }

        adapter = TypeAdapter(PropertyItemObject)
        result = adapter.validate_python(data)

        assert isinstance(result, RichTextPropertyItem)
        assert result.rich_text.plain_text == "Rich content"
        assert result.rich_text.annotations.bold is True


class TestPeoplePropertyItem:
    """Test PeoplePropertyItem."""

    def test_parse_people_property_item(self):
        """Test parsing a people property item."""
        data = {
            "object": "property_item",
            "id": "prop_people",
            "type": "people",
            "people": {
                "object": "user",
                "id": "user_123",
            },
        }

        adapter = TypeAdapter(PropertyItemObject)
        result = adapter.validate_python(data)

        assert isinstance(result, PeoplePropertyItem)
        assert result.people.id == "user_123"


class TestPropertyItemListResponse:
    """Test PropertyItemListResponse."""

    def test_parse_property_item_list_response(self):
        """Test parsing a paginated property item list."""
        data = {
            "object": "list",
            "next_cursor": "cursor_abc",
            "has_more": True,
            "type": "property_item",
            "property_item": {
                "type": "property_item",
                "next_url": "https://example.com/next",
                "id": "prop_123",
            },
            "results": [
                {
                    "object": "property_item",
                    "id": "item_1",
                    "type": "number",
                    "number": 10,
                },
                {
                    "object": "property_item",
                    "id": "item_2",
                    "type": "number",
                    "number": 20,
                },
            ],
        }

        result = PropertyItemListResponse.model_validate(data)

        assert result.object == "list"
        assert result.has_more is True
        assert result.next_cursor == "cursor_abc"
        assert len(result.results) == 2
        assert isinstance(result.results[0], NumberPropertyItem)
        assert isinstance(result.results[1], NumberPropertyItem)
        if isinstance(result.results[0], NumberPropertyItem):
            assert result.results[0].number == 10
        if isinstance(result.results[1], NumberPropertyItem):
            assert result.results[1].number == 20
