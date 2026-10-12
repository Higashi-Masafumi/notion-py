from typing import Literal

from pydantic import BaseModel, Field, StrictBool, StrictStr


class PageMarkdownWarning(BaseModel):
    """Parser warning from a synchronous ``markdown_version: v2`` update."""

    code: StrictStr = Field(..., description="警告コード")
    message: StrictStr = Field(..., description="パーサーが変更または無視した内容")


class PageMarkdownResponse(BaseModel):
    """Markdown representation returned by the page markdown endpoints."""

    object: Literal["page_markdown"] = Field(
        "page_markdown", description="オブジェクトタイプ"
    )
    id: StrictStr = Field(..., description="ページID")
    markdown: StrictStr = Field(..., description="ページ本文の Markdown")
    truncated: StrictBool = Field(..., description="結果が省略されたかどうか")
    unknown_block_ids: list[StrictStr] = Field(
        default_factory=list, description="追加取得が必要な未知ブロックID"
    )
    warnings: list[PageMarkdownWarning] = Field(
        default_factory=list,
        description="同期的な markdown_version v2 更新が返したパーサー警告",
    )
