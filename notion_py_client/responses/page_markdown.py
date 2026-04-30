from typing import Literal

from pydantic import BaseModel, Field, StrictBool, StrictStr


class PageMarkdownResponse(BaseModel):
    """Markdown representation returned by the page markdown endpoints."""

    object: Literal["page_markdown"] = Field(
        "page_markdown", description="オブジェクトタイプ"
    )
    id: StrictStr = Field(..., description="ページID")
    markdown: StrictStr = Field(..., description="Notion-flavored Markdown")
    truncated: StrictBool = Field(..., description="結果が省略されたかどうか")
    unknown_block_ids: list[StrictStr] = Field(
        default_factory=list, description="追加取得が必要な未知ブロックID"
    )
