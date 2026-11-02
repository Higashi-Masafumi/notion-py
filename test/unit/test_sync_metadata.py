"""Tests for stored data source sync metadata."""

import pytest
from pydantic import ValidationError

from notion_py_client import (
    DataSource,
    ExternalDatabaseSync,
    LegacySyncState,
    NotionAsyncClient,
    NotionDatabase,
    SyncMetadata,
)


def _data_source_payload(**extra: object) -> dict:
    payload = {
        "object": "data_source",
        "id": "ds_123",
        "title": [],
        "description": [],
        "parent": {"type": "database_id", "database_id": "db_123"},
        "database_parent": {"type": "page_id", "page_id": "page_123"},
        "is_inline": False,
        "in_trash": False,
        "created_time": "2026-10-30T00:00:00.000Z",
        "last_edited_time": "2026-10-30T00:00:00.000Z",
        "created_by": {"object": "user", "id": "user_123"},
        "last_edited_by": {"object": "user", "id": "user_123"},
        "properties": {
            "Name": {"id": "title", "name": "Name", "type": "title", "title": {}}
        },
        "url": "https://www.notion.so/ds_123",
        "public_url": None,
    }
    payload.update(extra)
    return payload


def _database_payload(data_sources: list[dict]) -> dict:
    return {
        "object": "database",
        "id": "db_123",
        "title": [],
        "description": [],
        "parent": {"type": "page_id", "page_id": "page_123"},
        "is_inline": False,
        "in_trash": False,
        "is_locked": False,
        "created_time": "2026-10-30T00:00:00.000Z",
        "last_edited_time": "2026-10-30T00:00:00.000Z",
        "data_sources": data_sources,
        "url": "https://www.notion.so/db_123",
        "public_url": None,
    }


class TestSyncMetadataModels:
    def test_external_database_sync(self):
        metadata = SyncMetadata.model_validate(
            {
                "external_database_sync": {
                    "sync_id": "2f26ee68-df30-4251-aad4-8ddc420cba3d",
                    "provider": "github",
                }
            }
        )

        assert metadata.external_database_sync == ExternalDatabaseSync(
            sync_id="2f26ee68-df30-4251-aad4-8ddc420cba3d",
            provider="github",
        )
        assert metadata.sync_state is None

    def test_legacy_sync_state_omits_missing_timestamps(self):
        metadata = SyncMetadata.model_validate(
            {
                "external_collection_type": "Jira",
                "sync_state": {"syncing": "row_limit_exceeded"},
            }
        )

        assert metadata.external_collection_type == "Jira"
        assert metadata.sync_state == LegacySyncState(syncing="row_limit_exceeded")

    def test_legacy_sync_state_keeps_timestamps(self):
        metadata = SyncMetadata.model_validate(
            {
                "external_collection_type": "Salesforce",
                "sync_state": {
                    "syncing": False,
                    "last_synced_at": "2026-10-29T12:34:56.789Z",
                    "last_sync_checkpoint_at": "2026-10-29T12:30:00.000Z",
                    "last_sync_heartbeat_at": "2026-10-29T12:34:50.000Z",
                },
            }
        )

        assert metadata.sync_state is not None
        assert metadata.sync_state.syncing is False
        assert metadata.sync_state.last_synced_at == "2026-10-29T12:34:56.789Z"

    def test_providerless_sync_id_and_worker_key(self):
        by_id = SyncMetadata.model_validate(
            {"sync_id": "2f26ee68-df30-4251-aad4-8ddc420cba3d"}
        )
        by_key = SyncMetadata.model_validate({"synced_collection_key": "issues"})

        assert by_id.sync_id == "2f26ee68-df30-4251-aad4-8ddc420cba3d"
        assert by_key.synced_collection_key == "issues"

    def test_rejects_unknown_provider_and_collection_type(self):
        with pytest.raises(ValidationError):
            SyncMetadata.model_validate(
                {
                    "external_database_sync": {
                        "sync_id": "2f26ee68-df30-4251-aad4-8ddc420cba3d",
                        "provider": "GitHub",
                    }
                }
            )
        with pytest.raises(ValidationError):
            SyncMetadata.model_validate({"external_collection_type": "jira"})

    def test_data_source_omits_sync_metadata_when_absent(self):
        data_source = DataSource.model_validate(_data_source_payload())

        assert data_source.sync_metadata is None

    def test_database_reference_parses_sync_metadata(self):
        database = NotionDatabase.model_validate(
            _database_payload(
                [
                    {"id": "ds_plain", "name": "Plain"},
                    {
                        "id": "ds_synced",
                        "name": "GitHub",
                        "sync_metadata": {
                            "external_database_sync": {
                                "sync_id": "2f26ee68-df30-4251-aad4-8ddc420cba3d",
                                "provider": "jira",
                            }
                        },
                    },
                ]
            )
        )

        assert "sync_metadata" not in database.data_sources[0]
        synced = database.data_sources[1]["sync_metadata"]
        assert synced is not None
        assert synced.external_database_sync is not None
        assert synced.external_database_sync.provider == "jira"


class TestSyncMetadataClient:
    @pytest.mark.asyncio
    async def test_retrieve_data_source_reads_sync_metadata(self):
        client = NotionAsyncClient(auth="test-token")

        async def fake_request(*, path, method, auth=None, **kwargs):
            assert path == "data_sources/ds_123"
            assert method == "get"
            return _data_source_payload(
                sync_metadata={"synced_collection_key": "issues"}
            )

        client.request = fake_request  # type: ignore[method-assign]

        result = await client.dataSources.retrieve(data_source_id="ds_123")

        assert result.sync_metadata is not None
        assert result.sync_metadata.synced_collection_key == "issues"

    @pytest.mark.asyncio
    async def test_retrieve_database_reads_sync_metadata(self):
        client = NotionAsyncClient(auth="test-token")

        async def fake_request(*, path, method, auth=None, **kwargs):
            assert path == "databases/db_123"
            assert method == "get"
            return _database_payload(
                [
                    {
                        "id": "ds_123",
                        "name": "Issues",
                        "sync_metadata": {"sync_id": "sync_123"},
                    }
                ]
            )

        client.request = fake_request  # type: ignore[method-assign]

        result = await client.databases.retrieve({"database_id": "db_123"})

        assert result.data_sources[0]["sync_metadata"] is not None
        assert result.data_sources[0]["sync_metadata"].sync_id == "sync_123"
