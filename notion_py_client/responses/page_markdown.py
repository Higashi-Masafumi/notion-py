"""Page markdown endpoint response models."""

from typing import Literal

from pydantic import BaseModel, Field, StrictBool, StrictStr


class PageMarkdownResponse(BaseModel):
    """`/pages/:page_id/markdown` 系エンドポイントのレスポンス."""

    object: Literal["page_markdown"] = Field(
        "page_markdown", description="オブジェクトタイプ"
    )
    id: StrictStr = Field(..., description="ページID")
    markdown: StrictStr = Field(..., description="Notion拡張Markdown本文")
    truncated: StrictBool = Field(..., description="省略の有無")
    unknown_block_ids: list[StrictStr] = Field(
        default_factory=list,
        description="未解決ブロックID一覧",
    )
