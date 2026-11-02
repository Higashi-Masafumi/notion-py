"""Stored sync metadata returned with readable data sources.

Official schema: optional fields on one object. A response uses the subset that
matches its stored representation. Search, create, and update responses omit
the object entirely.
"""

from typing import Literal

from pydantic import BaseModel, Field, StrictBool, StrictStr


class ExternalDatabaseSync(BaseModel):
    """外部データベース同期の保存済み識別子."""

    sync_id: StrictStr = Field(..., description="保存済み同期ID。認証情報ではない")
    provider: Literal["github", "jira", "salesforce"] = Field(
        ...,
        description="同期プロバイダ。github、jira、salesforce のいずれか",
    )


class LegacySyncState(BaseModel):
    """レガシー同期データソースの保存済み状態.

    タイムスタンプは UTC の ISO 8601 文字列。欠ける値はキーごと省略される。
    ライブなヘルスチェックではない。
    """

    syncing: StrictBool | Literal["row_limit_exceeded"] = Field(
        ...,
        description="同期中は true、停止中は false、行数上限で止まった場合は row_limit_exceeded",
    )
    last_synced_at: StrictStr | None = Field(
        None, description="保存済みの最終同期時刻（ISO 8601）"
    )
    last_sync_checkpoint_at: StrictStr | None = Field(
        None, description="保存済みの同期チェックポイント時刻（ISO 8601）"
    )
    last_sync_heartbeat_at: StrictStr | None = Field(
        None, description="保存済みの同期ハートビート時刻（ISO 8601）"
    )


class SyncMetadata(BaseModel):
    """読み取り専用の保存済み同期メタデータ.

    取得できる表現は次のいずれか、またはその一部です。

    - ``external_database_sync``: GitHub / Jira / Salesforce の外部データベース同期
    - ``external_collection_type`` と任意の ``sync_state``: レガシー同期（``Jira`` または ``Salesforce``）
    - ``sync_id``: プロバイダ詳細がない保存済み同期 ID
    - ``synced_collection_key``: Worker 同期のコレクションキー
    """

    external_database_sync: ExternalDatabaseSync | None = Field(
        None, description="外部データベース同期の識別子"
    )
    external_collection_type: Literal["Jira", "Salesforce"] | None = Field(
        None,
        description="レガシー同期のプロバイダ。Jira または Salesforce（大文字小文字を区別）",
    )
    sync_id: StrictStr | None = Field(
        None, description="プロバイダ詳細がない場合の保存済み同期ID"
    )
    sync_state: LegacySyncState | None = Field(
        None, description="レガシー同期の保存済み状態"
    )
    synced_collection_key: StrictStr | None = Field(
        None, description="Worker 同期のコレクションキー。グローバルに一意な ID ではない"
    )
