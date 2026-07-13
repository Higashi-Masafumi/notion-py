"""Async task response models."""

from typing import Any, Literal

from pydantic import BaseModel, Field, StrictInt, StrictStr


class AsyncTaskOperation(BaseModel):
    """Operation metadata for a Notion async task."""

    surface: StrictStr = Field(..., description="Operation surface, such as 'rest'")
    name: StrictStr = Field(..., description="Operation name")


class AsyncTaskError(BaseModel):
    """Standard Public API error object attached to a failed async task."""

    object: Literal["error"] = Field("error", description="Object type")
    status: StrictInt = Field(..., description="HTTP status code")
    code: StrictStr = Field(..., description="Notion API error code")
    message: StrictStr = Field(..., description="Error message")
    additional_data: dict[str, Any] | None = Field(
        None, description="Endpoint-specific error context"
    )
    request_id: StrictStr | None = Field(None, description="Notion request ID")


class AsyncTaskResponse(BaseModel):
    """Response returned by async-capable Notion operations."""

    object: Literal["async_task"] = Field("async_task", description="Object type")
    id: StrictStr = Field(..., description="Async task ID")
    status: Literal["queued", "running", "retrying", "succeeded", "failed"] = Field(
        ..., description="Task status"
    )
    status_url: StrictStr = Field(..., description="URL for polling task status")
    created_time: StrictStr = Field(..., description="Task creation timestamp")
    operation: AsyncTaskOperation = Field(..., description="Queued operation")
    poll_after_seconds: int | None = Field(
        None, description="Minimum seconds to wait before polling again"
    )
    result: dict[str, Any] | None = Field(None, description="Successful task result")
    error: AsyncTaskError | None = Field(None, description="Terminal task error")
