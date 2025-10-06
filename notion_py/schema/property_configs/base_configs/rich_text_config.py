from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject
from ....properties.base_properties._base_property import NotionPropertyType


class RichTextPropertyConfig(BasePropertyConfig):
    """Notionのrich_textプロパティ設定"""

    type: Literal[NotionPropertyType.RICH_TEXT] = Field(
        NotionPropertyType.RICH_TEXT, description="プロパティタイプ"
    )
    rich_text: EmptyObject = Field(
        default_factory=EmptyObject, description="rich_text設定"
    )
