from pydantic import BaseModel, Field, StrictBool, StrictStr


class Annotations(BaseModel):
    """NotionのRichTextのアノテーション情報"""

    bold: StrictBool = Field(..., description="太字かどうか")
    italic: StrictBool = Field(..., description="斜体かどうか")
    strikethrough: StrictBool = Field(..., description="取り消し線かどうか")
    underline: StrictBool = Field(..., description="下線かどうか")
    code: StrictBool = Field(..., description="コードかどうか")
    color: StrictStr = Field(..., description="色")
