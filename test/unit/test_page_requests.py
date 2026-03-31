"""Unit tests for page request models."""

from notion_py_client.requests.page_requests import UpdatePageParameters


class TestUpdatePageParameters:
    """Test page update parameters."""

    def test_in_trash_serializes(self):
        params = UpdatePageParameters(page_id="page_123", in_trash=True)

        payload = params.model_dump(exclude_none=True, by_alias=True)

        assert payload["in_trash"] is True
