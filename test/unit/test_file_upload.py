"""Unit tests for FileUploadObject response type."""

import pytest
from notion_py_client.responses.file_upload import (
    FileUploadObject,
    FileUploadCreatedBy,
    FileImportResult,
    FileImportError,
)
from notion_py_client.responses.list_response import ListFileUploadsResponse


class TestFileUploadCreatedBy:
    """Test FileUploadCreatedBy."""

    def test_parse_created_by_person(self):
        """Test parsing created_by with person type."""
        data = {
            "id": "user_123",
            "type": "person",
        }

        result = FileUploadCreatedBy.model_validate(data)

        assert result.id == "user_123"
        assert result.type == "person"

    def test_parse_created_by_bot(self):
        """Test parsing created_by with bot type."""
        data = {
            "id": "bot_456",
            "type": "bot",
        }

        result = FileUploadCreatedBy.model_validate(data)

        assert result.type == "bot"

    def test_parse_created_by_agent(self):
        """Test parsing created_by with agent type."""
        data = {
            "id": "agent_789",
            "type": "agent",
        }

        result = FileUploadCreatedBy.model_validate(data)

        assert result.type == "agent"


class TestFileImportError:
    """Test FileImportError."""

    def test_parse_file_import_error(self):
        """Test parsing a file import error."""
        data = {
            "type": "validation_error",
            "code": "invalid_file_type",
            "message": "The file type is not supported",
            "parameter": "file",
            "status_code": 400,
        }

        result = FileImportError.model_validate(data)

        assert result.type == "validation_error"
        assert result.code == "invalid_file_type"
        assert result.message == "The file type is not supported"
        assert result.parameter == "file"
        assert result.status_code == 400

    def test_parse_file_import_error_minimal(self):
        """Test parsing a file import error with minimal fields."""
        data = {
            "type": "internal_system_error",
            "code": "internal_error",
            "message": "An internal error occurred",
        }

        result = FileImportError.model_validate(data)

        assert result.type == "internal_system_error"
        assert result.parameter is None
        assert result.status_code is None


class TestFileImportResult:
    """Test FileImportResult."""

    def test_parse_file_import_result_success(self):
        """Test parsing a successful file import result."""
        data = {
            "imported_time": "2025-01-01T12:00:00.000Z",
            "type": "success",
            "success": {"pages_imported": 5},
        }

        result = FileImportResult.model_validate(data)

        assert result.type == "success"
        assert result.imported_time == "2025-01-01T12:00:00.000Z"
        assert result.success == {"pages_imported": 5}
        assert result.error is None

    def test_parse_file_import_result_error(self):
        """Test parsing a failed file import result."""
        data = {
            "imported_time": "2025-01-01T12:00:00.000Z",
            "type": "error",
            "error": {
                "type": "upload_error",
                "code": "upload_failed",
                "message": "Failed to upload file",
            },
        }

        result = FileImportResult.model_validate(data)

        assert result.type == "error"
        assert result.error.type == "upload_error"
        assert result.success is None


class TestFileUploadObject:
    """Test FileUploadObject."""

    def test_parse_file_upload_pending(self):
        """Test parsing a file upload object with pending status."""
        data = {
            "object": "file_upload",
            "id": "file_123",
            "created_time": "2025-01-01T00:00:00.000Z",
            "created_by": {
                "id": "user_123",
                "type": "person",
            },
            "last_edited_time": "2025-01-01T00:00:00.000Z",
            "archived": False,
            "expiry_time": "2025-01-02T00:00:00.000Z",
            "status": "pending",
            "filename": "document.pdf",
            "content_type": "application/pdf",
            "content_length": 1024,
            "upload_url": "https://example.com/upload",
        }

        result = FileUploadObject.model_validate(data)

        assert result.object == "file_upload"
        assert result.id == "file_123"
        assert result.status == "pending"
        assert result.filename == "document.pdf"
        assert result.content_type == "application/pdf"
        assert result.content_length == 1024
        assert result.upload_url == "https://example.com/upload"
        assert result.archived is False

    def test_parse_file_upload_uploaded(self):
        """Test parsing a file upload object with uploaded status."""
        data = {
            "object": "file_upload",
            "id": "file_456",
            "created_time": "2025-01-01T00:00:00.000Z",
            "created_by": {
                "id": "bot_789",
                "type": "bot",
            },
            "last_edited_time": "2025-01-01T00:10:00.000Z",
            "archived": False,
            "expiry_time": None,
            "status": "uploaded",
            "filename": "image.png",
            "content_type": "image/png",
            "content_length": 2048,
            "complete_url": "https://example.com/complete",
        }

        result = FileUploadObject.model_validate(data)

        assert result.status == "uploaded"
        assert result.complete_url == "https://example.com/complete"
        assert result.expiry_time is None

    def test_parse_file_upload_with_import_result(self):
        """Test parsing a file upload with import result."""
        data = {
            "object": "file_upload",
            "id": "file_789",
            "created_time": "2025-01-01T00:00:00.000Z",
            "created_by": {
                "id": "user_456",
                "type": "person",
            },
            "last_edited_time": "2025-01-01T00:15:00.000Z",
            "archived": False,
            "expiry_time": None,
            "status": "uploaded",
            "file_import_result": {
                "imported_time": "2025-01-01T00:15:00.000Z",
                "type": "success",
                "success": {"pages_imported": 3},
            },
        }

        result = FileUploadObject.model_validate(data)

        assert result.file_import_result is not None
        assert result.file_import_result.type == "success"
        assert result.file_import_result.success["pages_imported"] == 3

    def test_parse_file_upload_failed(self):
        """Test parsing a failed file upload."""
        data = {
            "object": "file_upload",
            "id": "file_failed",
            "created_time": "2025-01-01T00:00:00.000Z",
            "created_by": {
                "id": "user_123",
                "type": "person",
            },
            "last_edited_time": "2025-01-01T00:05:00.000Z",
            "archived": False,
            "expiry_time": None,
            "status": "failed",
        }

        result = FileUploadObject.model_validate(data)

        assert result.status == "failed"
        assert result.filename is None

    def test_parse_file_upload_with_parts(self):
        """Test parsing a file upload with multi-part info."""
        data = {
            "object": "file_upload",
            "id": "file_multipart",
            "created_time": "2025-01-01T00:00:00.000Z",
            "created_by": {
                "id": "user_123",
                "type": "person",
            },
            "last_edited_time": "2025-01-01T00:00:00.000Z",
            "archived": False,
            "expiry_time": "2025-01-02T00:00:00.000Z",
            "status": "pending",
            "number_of_parts": {"total": 10, "sent": 5},
        }

        result = FileUploadObject.model_validate(data)

        assert result.number_of_parts is not None
        assert result.number_of_parts["total"] == 10
        assert result.number_of_parts["sent"] == 5


class TestListFileUploadsResponse:
    """Test ListFileUploadsResponse."""

    def test_parse_list_file_uploads_response(self):
        """Test parsing a list of file uploads."""
        data = {
            "object": "list",
            "results": [
                {
                    "object": "file_upload",
                    "id": "file_1",
                    "created_time": "2025-01-01T00:00:00.000Z",
                    "created_by": {"id": "user_123", "type": "person"},
                    "last_edited_time": "2025-01-01T00:00:00.000Z",
                    "archived": False,
                    "expiry_time": None,
                    "status": "uploaded",
                    "filename": "file1.pdf",
                    "content_type": "application/pdf",
                    "content_length": 1024,
                },
                {
                    "object": "file_upload",
                    "id": "file_2",
                    "created_time": "2025-01-01T00:05:00.000Z",
                    "created_by": {"id": "user_456", "type": "person"},
                    "last_edited_time": "2025-01-01T00:05:00.000Z",
                    "archived": False,
                    "expiry_time": "2025-01-02T00:00:00.000Z",
                    "status": "pending",
                },
            ],
            "next_cursor": "cursor_123",
            "has_more": True,
            "type": "file_upload",
        }

        result = ListFileUploadsResponse.model_validate(data)

        assert result.object == "list"
        assert result.has_more is True
        assert result.next_cursor == "cursor_123"
        assert result.type == "file_upload"
        assert len(result.results) == 2
        assert isinstance(result.results[0], FileUploadObject)
        assert result.results[0].status == "uploaded"
        assert result.results[1].status == "pending"

    def test_parse_empty_list_file_uploads(self):
        """Test parsing an empty file uploads list."""
        data = {
            "object": "list",
            "results": [],
            "next_cursor": None,
            "has_more": False,
            "type": "file_upload",
        }

        result = ListFileUploadsResponse.model_validate(data)

        assert len(result.results) == 0
        assert result.has_more is False
        assert result.next_cursor is None
