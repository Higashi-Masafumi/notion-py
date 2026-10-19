from typing import Literal

from pydantic import BaseModel, Field, StrictBool, StrictStr


class PageMarkdownWarning(BaseModel):
    """同期的なページ Markdown 更新が返す警告."""

    code: StrictStr = Field(..., description="警告コード")
    message: StrictStr = Field(..., description="変更または無視された内容")


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
    warnings: list[PageMarkdownWarning] = Field(
        default_factory=list,
        description=(
            "同期更新の警告。パーサーが内容を変えた場合や、"
            "update_content の old_str が一致しなかった場合に付く。"
            "警告がないレスポンスでは省略される"
        ),
    )
