"""Tests for data source sync metadata and live health."""

import pytest
from pydantic import ValidationError

from notion_py_client import (
    DataSource,
    ExternalDatabaseSync,
    LegacySyncState,
    NotionAsyncClient,
    NotionDatabase,
    SyncHealth,
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
        "created_time": "2026-11-05T00:00:00.000Z",
        "last_edited_time": "2026-11-05T00:00:00.000Z",
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
        "created_time": "2026-11-05T00:00:00.000Z",
        "last_edited_time": "2026-11-05T00:00:00.000Z",
        "data_sources": data_sources,
        "url": "https://www.notion.so/db_123",
        "public_url": None,
    }


def _healthy_checks(**extra: str) -> dict[str, str]:
    checks = {"sync_version_updated_at": "2026-11-01T10:00:00.000Z"}
    checks.update(extra)
    return checks


class TestSyncMetadataModels:
    def test_external_database_sync_with_live_health(self):
        metadata = SyncMetadata.model_validate(
            {
                "external_database_sync": {
                    "sync_id": "2f26ee68-df30-4251-aad4-8ddc420cba3d",
                    "provider": "github",
                },
                "owner_user_id": "48d4cadc-82c9-48a7-b3ea-8a54b7787d31",
                "resource": "issues",
                "health": {
                    "paused": False,
                    "stage": "steady",
                    "ok": True,
                    "checks": _healthy_checks(
                        last_execution_succeeded_at="2026-11-01T10:01:00.000Z",
                        delta_synced_through_at="2026-11-01T10:02:00.000Z",
                    ),
                },
            }
        )

        assert metadata.external_database_sync == ExternalDatabaseSync(
            sync_id="2f26ee68-df30-4251-aad4-8ddc420cba3d",
            provider="github",
        )
        assert metadata.owner_user_id == "48d4cadc-82c9-48a7-b3ea-8a54b7787d31"
        assert metadata.resource == "issues"
        assert metadata.health == SyncHealth(
            paused=False,
            stage="steady",
            ok=True,
            checks={
                "sync_version_updated_at": "2026-11-01T10:00:00.000Z",
                "last_execution_succeeded_at": "2026-11-01T10:01:00.000Z",
                "delta_synced_through_at": "2026-11-01T10:02:00.000Z",
            },
        )

    def test_null_health_means_unavailable(self):
        metadata = SyncMetadata.model_validate(
            {
                "external_database_sync": {
                    "sync_id": "2f26ee68-df30-4251-aad4-8ddc420cba3d",
                    "provider": "salesforce",
                },
                "health": None,
            }
        )

        assert metadata.health is None
        assert metadata.resource is None
        assert metadata.owner_user_id is None

    def test_missing_check_timestamps_mean_unknown(self):
        metadata = SyncMetadata.model_validate(
            {
                "health": {
                    "paused": False,
                    "stage": "backfilling",
                    "ok": True,
                    "checks": _healthy_checks(),
                }
            }
        )

        assert metadata.health is not None
        assert metadata.health.checks is not None
        assert metadata.health.checks.delta_synced_through_at is None
        assert metadata.health.checks.last_execution_succeeded_at is None

    def test_paused_sync_without_resource_health(self):
        metadata = SyncMetadata.model_validate({"health": {"paused": True}})

        assert metadata.health == SyncHealth(paused=True)
        assert metadata.resource is None
        assert metadata.health.ok is None
        assert metadata.health.checks is None

    def test_unhealthy_sync_includes_error(self):
        metadata = SyncMetadata.model_validate(
            {
                "resource": "issues",
                "health": {
                    "paused": False,
                    "stage": "initializing",
                    "ok": False,
                    "error": {"code": "auth_expired", "severity": "action_required"},
                    "checks": _healthy_checks(),
                },
            }
        )

        assert metadata.health is not None
        assert metadata.health.ok is False
        assert metadata.health.error is not None
        assert metadata.health.error.severity == "action_required"

    def test_legacy_and_worker_metadata_stay_unchanged(self):
        legacy = SyncMetadata.model_validate(
            {
                "external_collection_type": "Jira",
                "sync_state": {"syncing": "row_limit_exceeded"},
            }
        )
        worker = SyncMetadata.model_validate({"synced_collection_key": "issues"})
        by_id = SyncMetadata.model_validate(
            {"sync_id": "2f26ee68-df30-4251-aad4-8ddc420cba3d"}
        )

        assert legacy.external_collection_type == "Jira"
        assert legacy.sync_state == LegacySyncState(syncing="row_limit_exceeded")
        assert legacy.health is None
        assert worker.synced_collection_key == "issues"
        assert worker.health is None
        assert by_id.sync_id == "2f26ee68-df30-4251-aad4-8ddc420cba3d"

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

    def test_rejects_invalid_health_and_identity(self):
        invalid_payloads = [
            {"health": {"paused": False}},
            {"health": {"paused": True, "ok": True}},
            {
                "health": {
                    "paused": False,
                    "stage": "steady",
                    "ok": True,
                    "error": {"code": "auth_expired", "severity": "degraded"},
                    "checks": _healthy_checks(),
                }
            },
            {
                "health": {
                    "paused": False,
                    "stage": "steady",
                    "ok": False,
                    "checks": _healthy_checks(),
                }
            },
            {
                "health": {
                    "paused": False,
                    "stage": "steady",
                    "ok": False,
                    "error": {"code": "auth_expired", "severity": "warning"},
                    "checks": _healthy_checks(),
                }
            },
            {
                "health": {
                    "paused": False,
                    "stage": "running",
                    "ok": True,
                    "checks": _healthy_checks(),
                }
            },
            {"health": {"paused": False, "stage": "steady", "ok": True, "checks": {}}},
            {
                "external_database_sync": {
                    "sync_id": "2f26ee68-df30-4251-aad4-8ddc420cba3d",
                    "provider": "GitHub",
                }
            },
            {"external_collection_type": "jira"},
        ]

        for payload in invalid_payloads:
            with pytest.raises(ValidationError):
                SyncMetadata.model_validate(payload)

    def test_data_source_omits_sync_metadata_when_absent(self):
        data_source = DataSource.model_validate(_data_source_payload())

        assert data_source.sync_metadata is None

    def test_database_reference_parses_health_without_injecting_missing_keys(self):
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
                            },
                            "resource": "issues",
                            "health": {
                                "paused": False,
                                "stage": "steady",
                                "ok": True,
                                "checks": _healthy_checks(),
                            },
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
        assert synced.health is not None
        assert synced.health.ok is True
        assert synced.resource == "issues"


class TestSyncMetadataClient:
    @pytest.mark.asyncio
    async def test_retrieve_data_source_reads_sync_health(self):
        client = NotionAsyncClient(auth="test-token")

        async def fake_request(*, path, method, auth=None, **kwargs):
            assert path == "data_sources/ds_123"
            assert method == "get"
            return _data_source_payload(
                sync_metadata={
                    "synced_collection_key": "issues",
                    "health": None,
                }
            )

        client.request = fake_request  # type: ignore[method-assign]

        result = await client.dataSources.retrieve(data_source_id="ds_123")

        assert result.sync_metadata is not None
        assert result.sync_metadata.synced_collection_key == "issues"
        assert result.sync_metadata.health is None

    @pytest.mark.asyncio
    async def test_retrieve_database_reads_sync_health(self):
        client = NotionAsyncClient(auth="test-token")

        async def fake_request(*, path, method, auth=None, **kwargs):
            assert path == "databases/db_123"
            assert method == "get"
            return _database_payload(
                [
                    {
                        "id": "ds_123",
                        "name": "Issues",
                        "sync_metadata": {
                            "sync_id": "sync_123",
                            "owner_user_id": "user_123",
                            "health": {"paused": True},
                        },
                    }
                ]
            )

        client.request = fake_request  # type: ignore[method-assign]

        result = await client.databases.retrieve({"database_id": "db_123"})

        metadata = result.data_sources[0]["sync_metadata"]
        assert metadata is not None
        assert metadata.sync_id == "sync_123"
        assert metadata.owner_user_id == "user_123"
        assert metadata.health == SyncHealth(paused=True)
