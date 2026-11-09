"""読み取り可能なデータソースに付く同期メタデータ.

公式スキーマは独立した任意フィールドを持つ1つのオブジェクトです。
応答には保存されている表現に対応するフィールドだけが含まれます。
検索、作成、更新、部分レスポンスではオブジェクト自体が省略されます。
"""

from typing import Literal

from pydantic import BaseModel, Field, StrictBool, StrictStr, model_validator


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


class SyncHealthChecks(BaseModel):
    """ライブ同期ヘルスの時刻.

    値は UTC の ISO 8601 文字列。実行時刻とチェックポイントが無い場合は不明。
    ``sync_version_updated_at`` は設定変更の時刻であり、取り込み成功を意味しない。
    """

    sync_version_updated_at: StrictStr = Field(
        ..., description="同期設定が更新された時刻（ISO 8601）"
    )
    delta_synced_through_at: StrictStr | None = Field(
        None, description="差分同期が到達している時刻（ISO 8601）。無い場合は不明"
    )
    last_execution_succeeded_at: StrictStr | None = Field(
        None, description="直近の実行が成功した時刻（ISO 8601）。無い場合は不明"
    )


class SyncHealthError(BaseModel):
    """ライブ同期ヘルスのエラー。``ok`` が false のときだけ付く."""

    code: StrictStr = Field(..., description="エラーコード")
    severity: Literal["action_required", "degraded", "failing"] = Field(
        ...,
        description="重大度。action_required、degraded、failing のいずれか",
    )


class SyncHealth(BaseModel):
    """ライブなコレクション同期ヘルス.

    形は次のいずれかです。

    - ``{"paused": true}``: リソースヘルスを持たない一時停止
    - ``ok`` が true: ``stage`` と ``checks`` を含み、``error`` は含まない
    - ``ok`` が false: ``stage``、``checks``、``error`` を含む

    親の ``health`` が null または省略された場合、このオブジェクト自体は作られません。
    null はヘルス不明であり、同期が不健全であることではありません。
    """

    paused: StrictBool = Field(..., description="同期が一時停止しているか")
    stage: Literal["initializing", "backfilling", "steady"] | None = Field(
        None,
        description="同期ステージ。initializing、backfilling、steady のいずれか",
    )
    ok: StrictBool | None = Field(None, description="同期が健全なら true")
    error: SyncHealthError | None = Field(
        None, description="ok が false のときのエラーコードと重大度"
    )
    checks: SyncHealthChecks | None = Field(None, description="ヘルス判定に使う時刻")

    @model_validator(mode="after")
    def validate_documented_shape(self) -> "SyncHealth":
        paused_only = (
            self.stage is None
            and self.ok is None
            and self.error is None
            and self.checks is None
        )
        if paused_only:
            if self.paused is not True:
                raise ValueError('paused-only sync health must be {"paused": true}')
            return self
        if self.ok is None or self.stage is None or self.checks is None:
            raise ValueError("sync health requires paused, stage, ok, and checks")
        if self.ok and self.error is not None:
            raise ValueError("healthy sync health does not include error")
        if not self.ok and self.error is None:
            raise ValueError("unhealthy sync health requires error")
        return self


class SyncMetadata(BaseModel):
    """読み取り専用の同期メタデータ.

    保存済みの識別子は次のいずれか、またはその一部です。

    - ``external_database_sync``: GitHub / Jira / Salesforce の外部データベース同期
    - ``external_collection_type`` と任意の ``sync_state``: レガシー同期（``Jira`` または ``Salesforce``）
    - ``sync_id``: プロバイダ詳細がない保存済み同期 ID
    - ``synced_collection_key``: Worker 同期のコレクションキー

    対応する外部データベース同期では、同じオブジェクトにライブヘルスが載ります。
    ``owner_user_id`` と ``resource`` はヘルス参照で得られたときだけ含まれます。
    レガシー同期と Worker 同期の保存済みフィールドにヘルスは追加されません。
    この値は同期を開始せず、認証情報や同期設定も含みません。
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
    owner_user_id: StrictStr | None = Field(
        None, description="同期認証情報を所有する Notion ユーザー ID。得られたときだけ含まれる"
    )
    resource: StrictStr | None = Field(
        None, description="このデータソースが同期するプロバイダのリソース。得られたときだけ含まれる"
    )
    health: SyncHealth | None = Field(
        None,
        description="ライブな同期ヘルス。null は不明であり、不健全を意味しない",
    )
