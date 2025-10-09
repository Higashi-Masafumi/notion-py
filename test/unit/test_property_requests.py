"""Unit tests for property request classes."""

import pytest
from notion_py_client.requests.property_requests import (
    TitlePropertyRequest,
    RichTextPropertyRequest,
    StatusPropertyRequest,
    SelectPropertyRequest,
    MultiSelectPropertyRequest,
    NumberPropertyRequest,
    DatePropertyRequest,
    CheckboxPropertyRequest,
    UrlPropertyRequest,
    EmailPropertyRequest,
    PhoneNumberPropertyRequest,
    PeoplePropertyRequest,
    FilesPropertyRequest,
    RelationPropertyRequest,
)
from notion_py_client.requests.common import (
    SelectPropertyItemRequest,
    PartialUserObjectRequest,
    DateRequest,
    RelationItemRequest,
)


class TestTitlePropertyRequest:
    """Test TitlePropertyRequest."""

    def test_create_title_request(self):
        """Test creating a title property request."""
        request = TitlePropertyRequest(
            title=[{"type": "text", "text": {"content": "Test Title"}}]
        )

        result = request.model_dump(by_alias=True, exclude_none=True)

        assert "title" in result
        assert result["title"][0]["text"]["content"] == "Test Title"

    def test_empty_title_request(self):
        """Test creating an empty title request."""
        request = TitlePropertyRequest(title=[])

        result = request.model_dump(by_alias=True, exclude_none=True)

        assert "title" in result
        assert result["title"] == []


class TestRichTextPropertyRequest:
    """Test RichTextPropertyRequest."""

    def test_create_rich_text_request(self):
        """Test creating a rich text property request."""
        request = RichTextPropertyRequest(
            rich_text=[{"type": "text", "text": {"content": "Rich text content"}}]
        )

        result = request.model_dump(by_alias=True, exclude_none=True)

        assert "rich_text" in result
        assert result["rich_text"][0]["text"]["content"] == "Rich text content"


class TestStatusPropertyRequest:
    """Test StatusPropertyRequest."""

    def test_create_status_request_with_name(self):
        """Test creating a status property request with name."""
        request = StatusPropertyRequest(
            status=SelectPropertyItemRequest(name="In Progress")
        )

        result = request.model_dump(by_alias=True, exclude_none=True)

        assert "status" in result
        assert result["status"]["name"] == "In Progress"

    def test_create_status_request_with_id(self):
        """Test creating a status property request with ID."""
        request = StatusPropertyRequest(
            status=SelectPropertyItemRequest(id="status-123")
        )

        result = request.model_dump(by_alias=True, exclude_none=True)

        assert "status" in result
        assert result["status"]["id"] == "status-123"

    def test_create_none_status_request(self):
        """Test creating a status request to clear status."""
        request = StatusPropertyRequest(status=None)

        result = request.model_dump(by_alias=True, exclude_none=True)

        # When status is None, it should not appear in the result
        assert "status" not in result or result.get("status") is None


class TestSelectPropertyRequest:
    """Test SelectPropertyRequest."""

    def test_create_select_request(self):
        """Test creating a select property request."""
        request = SelectPropertyRequest(
            select=SelectPropertyItemRequest(name="High Priority")
        )

        result = request.model_dump(by_alias=True, exclude_none=True)

        assert "select" in result
        assert result["select"]["name"] == "High Priority"


class TestMultiSelectPropertyRequest:
    """Test MultiSelectPropertyRequest."""

    def test_create_multi_select_request(self):
        """Test creating a multi-select property request."""
        request = MultiSelectPropertyRequest(
            multi_select=[
                SelectPropertyItemRequest(name="Tag1"),
                SelectPropertyItemRequest(name="Tag2"),
            ]
        )

        result = request.model_dump(by_alias=True, exclude_none=True)

        assert "multi_select" in result
        assert len(result["multi_select"]) == 2
        assert result["multi_select"][0]["name"] == "Tag1"
        assert result["multi_select"][1]["name"] == "Tag2"

    def test_empty_multi_select_request(self):
        """Test creating an empty multi-select request."""
        request = MultiSelectPropertyRequest(multi_select=[])

        result = request.model_dump(by_alias=True, exclude_none=True)

        assert "multi_select" in result
        assert result["multi_select"] == []


class TestNumberPropertyRequest:
    """Test NumberPropertyRequest."""

    def test_create_number_request(self):
        """Test creating a number property request."""
        request = NumberPropertyRequest(number=42)

        result = request.model_dump(by_alias=True, exclude_none=True)

        assert "number" in result
        assert result["number"] == 42

    def test_create_float_number_request(self):
        """Test creating a float number property request."""
        request = NumberPropertyRequest(number=3.14)

        result = request.model_dump(by_alias=True, exclude_none=True)

        assert "number" in result
        assert result["number"] == 3.14

    def test_create_none_number_request(self):
        """Test creating a number request to clear value."""
        request = NumberPropertyRequest(number=None)

        result = request.model_dump(by_alias=True, exclude_none=True)

        assert "number" not in result or result.get("number") is None


class TestDatePropertyRequest:
    """Test DatePropertyRequest."""

    def test_create_date_request(self):
        """Test creating a date property request."""
        request = DatePropertyRequest(
            date=DateRequest(start="2025-10-09", end=None, time_zone=None)
        )

        result = request.model_dump(by_alias=True, exclude_none=True)

        assert "date" in result
        assert result["date"]["start"] == "2025-10-09"

    def test_create_date_range_request(self):
        """Test creating a date range property request."""
        request = DatePropertyRequest(
            date=DateRequest(
                start="2025-10-09", end="2025-10-10", time_zone="Asia/Tokyo"
            )
        )

        result = request.model_dump(by_alias=True, exclude_none=True)

        assert "date" in result
        assert result["date"]["start"] == "2025-10-09"
        assert result["date"]["end"] == "2025-10-10"
        assert result["date"]["time_zone"] == "Asia/Tokyo"

    def test_create_none_date_request(self):
        """Test creating a date request to clear value."""
        request = DatePropertyRequest(date=None)

        result = request.model_dump(by_alias=True, exclude_none=True)

        assert "date" not in result or result.get("date") is None


class TestCheckboxPropertyRequest:
    """Test CheckboxPropertyRequest."""

    def test_create_checkbox_true_request(self):
        """Test creating a checkbox property request (true)."""
        request = CheckboxPropertyRequest(checkbox=True)

        result = request.model_dump(by_alias=True, exclude_none=True)

        assert "checkbox" in result
        assert result["checkbox"] is True

    def test_create_checkbox_false_request(self):
        """Test creating a checkbox property request (false)."""
        request = CheckboxPropertyRequest(checkbox=False)

        result = request.model_dump(by_alias=True, exclude_none=True)

        assert "checkbox" in result
        assert result["checkbox"] is False


class TestUrlPropertyRequest:
    """Test UrlPropertyRequest."""

    def test_create_url_request(self):
        """Test creating a URL property request."""
        request = UrlPropertyRequest(url="https://example.com")

        result = request.model_dump(by_alias=True, exclude_none=True)

        assert "url" in result
        assert result["url"] == "https://example.com"

    def test_create_none_url_request(self):
        """Test creating a URL request to clear value."""
        request = UrlPropertyRequest(url=None)

        result = request.model_dump(by_alias=True, exclude_none=True)

        assert "url" not in result or result.get("url") is None


class TestEmailPropertyRequest:
    """Test EmailPropertyRequest."""

    def test_create_email_request(self):
        """Test creating an email property request."""
        request = EmailPropertyRequest(email="test@example.com")

        result = request.model_dump(by_alias=True, exclude_none=True)

        assert "email" in result
        assert result["email"] == "test@example.com"


class TestPhoneNumberPropertyRequest:
    """Test PhoneNumberPropertyRequest."""

    def test_create_phone_number_request(self):
        """Test creating a phone number property request."""
        request = PhoneNumberPropertyRequest(phone_number="+81-90-1234-5678")

        result = request.model_dump(by_alias=True, exclude_none=True)

        assert "phone_number" in result
        assert result["phone_number"] == "+81-90-1234-5678"


class TestPeoplePropertyRequest:
    """Test PeoplePropertyRequest."""

    def test_create_people_request(self):
        """Test creating a people property request."""
        request = PeoplePropertyRequest(
            people=[PartialUserObjectRequest(id="user-123")]
        )

        result = request.model_dump(by_alias=True, exclude_none=True)

        assert "people" in result
        assert len(result["people"]) == 1
        assert result["people"][0]["id"] == "user-123"

    def test_create_multiple_people_request(self):
        """Test creating a people property request with multiple users."""
        request = PeoplePropertyRequest(
            people=[
                PartialUserObjectRequest(id="user-123"),
                PartialUserObjectRequest(id="user-456"),
            ]
        )

        result = request.model_dump(by_alias=True, exclude_none=True)

        assert "people" in result
        assert len(result["people"]) == 2


class TestFilesPropertyRequest:
    """Test FilesPropertyRequest."""

    def test_create_files_request(self):
        """Test creating a files property request."""
        request = FilesPropertyRequest(
            files=[{"name": "document.pdf", "external": {"url": "https://example.com/doc.pdf"}}]  # type: ignore
        )

        result = request.model_dump(by_alias=True, exclude_none=True)

        assert "files" in result
        assert len(result["files"]) == 1


class TestRelationPropertyRequest:
    """Test RelationPropertyRequest."""

    def test_create_relation_request(self):
        """Test creating a relation property request."""
        request = RelationPropertyRequest(relation=[RelationItemRequest(id="page-123")])

        result = request.model_dump(by_alias=True, exclude_none=True)

        assert "relation" in result
        assert len(result["relation"]) == 1
        assert result["relation"][0]["id"] == "page-123"

    def test_create_multiple_relations_request(self):
        """Test creating a relation property request with multiple pages."""
        request = RelationPropertyRequest(
            relation=[
                RelationItemRequest(id="page-123"),
                RelationItemRequest(id="page-456"),
            ]
        )

        result = request.model_dump(by_alias=True, exclude_none=True)

        assert "relation" in result
        assert len(result["relation"]) == 2


class TestPropertyRequestSerialization:
    """Test property request serialization for API compatibility."""

    def test_all_requests_serializable(self):
        """Test that all property requests can be serialized."""
        requests = [
            TitlePropertyRequest(title=[{"type": "text", "text": {"content": "Test"}}]),
            StatusPropertyRequest(status=SelectPropertyItemRequest(name="Done")),
            NumberPropertyRequest(number=100),
            DatePropertyRequest(date=DateRequest(start="2025-01-01")),
            CheckboxPropertyRequest(checkbox=True),
        ]

        for req in requests:
            result = req.model_dump(by_alias=True, exclude_none=True)
            assert isinstance(result, dict)
            assert len(result) > 0
