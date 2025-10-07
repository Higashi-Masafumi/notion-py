from typing import Literal

from pydantic import BaseModel, Field

from ..date_info import DateInfo
from ..user import PartialUser, User
from .custom_emoji import CustomEmoji
from .link_mention import LinkMention
from .link_preview import LinkPreviewMention
from .template_mention import TemplateMention


class Mention(BaseModel):
    """RichTextで利用されるメンション情報"""

    type: Literal[
        "user",
        "date",
        "link_preview",
        "link_mention",
        "page",
        "database",
        "template_mention",
        "custom_emoji",
    ] = Field(..., description="メンションタイプ")
    user: PartialUser | User | None = Field(
        None, description="ユーザーメンションの詳細"
    )
    date: DateInfo | None = Field(None, description="日付メンションの詳細")
    link_preview: LinkPreviewMention | None = Field(
        None, description="リンクプレビューメンションの詳細"
    )
    link_mention: LinkMention | None = Field(
        None, description="リンクメンションの詳細"
    )
    page: dict[str, str] | None = Field(None, description="ページメンションの詳細")
    database: dict[str, str] | None = Field(None, description="データベースメンションの詳細")
    template_mention: TemplateMention | None = Field(
        None, description="テンプレートメンションの詳細"
    )
    custom_emoji: CustomEmoji | None = Field(
        None, description="カスタム絵文字メンションの詳細"
    )
