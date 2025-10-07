from pydantic import BaseModel, Field, StrictStr


class LinkPreviewMention(BaseModel):
    """Notionのlink_previewメンション情報"""

    url: StrictStr = Field(..., description="プレビュー対象のURL")
