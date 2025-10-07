from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject
from ....properties.base_properties._base_property import NotionPropertyType


class TitlePropertyConfig(BasePropertyConfig):
    """Notionのtitleプロパティ設定"""

    type: Literal[NotionPropertyType.TITLE] = Field(
        NotionPropertyType.TITLE, description="プロパティタイプ"
    )
    title: EmptyObject = Field(
        default_factory=EmptyObject, description="title設定"
    )
