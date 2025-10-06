from pydantic import BaseModel, Field, StrictStr


class Link(BaseModel):
    """RichText内のリンク情報"""

    url: StrictStr = Field(..., description="リンクURL")


class Text(BaseModel):
    """NotionのRichTextのテキスト情報"""

    content: StrictStr = Field(..., description="テキスト内容")
    link: Link | None = Field(None, description="リンク情報（ない場合はnull）")
