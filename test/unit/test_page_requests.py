"""Unit tests for page request models."""

from notion_py_client.requests.page_requests import UpdatePageParameters


class TestUpdatePageParameters:
    """Test page update parameter normalization."""

    def test_archived_maps_to_in_trash(self):
        params = UpdatePageParameters(page_id="page_123", archived=True)

        payload = params.model_dump(exclude_none=True, by_alias=True)

        assert payload["in_trash"] is True
        assert "archived" not in payload

    def test_in_trash_backfills_archived_attribute(self):
        params = UpdatePageParameters(page_id="page_123", in_trash=False)

        assert params.archived is False
