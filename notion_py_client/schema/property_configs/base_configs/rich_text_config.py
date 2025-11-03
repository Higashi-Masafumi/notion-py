from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject


class RichTextPropertyConfig(
    BasePropertyConfig[Literal["rich_text"]]
):
    """Notionのrich_textプロパティ設定"""

    type: Literal["rich_text"] = Field(
        "rich_text", description="プロパティタイプ"
    )
    rich_text: EmptyObject = Field(
        default_factory=EmptyObject, description="rich_text設定"
    )
