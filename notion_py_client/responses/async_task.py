from typing import Any, Literal

from pydantic import BaseModel, Field, StrictInt, StrictStr


class AsyncTaskOperation(BaseModel):
    """非同期タスクが対象とする操作の識別情報."""

    surface: StrictStr = Field(..., description="操作の対象領域")
    name: StrictStr = Field(..., description="操作名")


class AsyncTaskError(BaseModel):
    """非同期タスクが失敗した際のエラー情報."""

    object: Literal["error"] = Field("error", description="オブジェクトタイプ")
    status: StrictInt = Field(..., description="HTTPステータスコード")
    code: StrictStr = Field(..., description="エラーコード")
    message: StrictStr = Field(..., description="エラーメッセージ")


class AsyncTaskResponse(BaseModel):
    """asyncTasks.retrieve() のレスポンス型.

    ステータスに応じて `poll_after_seconds`（実行中）、`result`（成功時）、
    `error`（失敗時）のいずれかが設定される。
    """

    object: Literal["async_task"] = Field("async_task", description="オブジェクトタイプ")
    id: StrictStr = Field(..., description="非同期タスクID")
    status_url: StrictStr = Field(..., description="ステータス確認用URL")
    created_time: StrictStr = Field(..., description="作成日時")
    operation: AsyncTaskOperation = Field(..., description="対象の操作")
    status: Literal["queued", "running", "retrying", "succeeded", "failed"] = Field(
        ..., description="タスクの状態"
    )
    poll_after_seconds: StrictInt | None = Field(
        None, description="次回ポーリングまでの推奨待機秒数"
    )
    result: dict[str, Any] | None = Field(None, description="成功時の結果")
    error: AsyncTaskError | None = Field(None, description="失敗時のエラー情報")
