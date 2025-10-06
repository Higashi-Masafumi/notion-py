from typing import Optional

from pydantic import BaseModel, Field, StrictFloat, StrictInt, StrictStr


class LinkMention(BaseModel):
    """Notionのlink_mention詳細"""

    href: StrictStr = Field(..., description="リンクのhref")
    title: Optional[StrictStr] = Field(None, description="リンクタイトル")
    description: Optional[StrictStr] = Field(None, description="リンクの説明")
    link_author: Optional[StrictStr] = Field(None, description="リンクの作者")
    link_provider: Optional[StrictStr] = Field(None, description="リンクの提供元")
    thumbnail_url: Optional[StrictStr] = Field(None, description="サムネイルURL")
    icon_url: Optional[StrictStr] = Field(None, description="アイコンURL")
    iframe_url: Optional[StrictStr] = Field(None, description="iframeのURL")
    height: Optional[StrictFloat | StrictInt] = Field(None, description="プレビュー高さ")
    padding: Optional[StrictFloat | StrictInt] = Field(None, description="iframeパディング")
    padding_top: Optional[StrictFloat | StrictInt] = Field(
        None, description="iframeパディング上部"
    )
