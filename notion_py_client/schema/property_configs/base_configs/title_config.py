from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject


class TitlePropertyConfig(BasePropertyConfig[Literal["title"]]):
    """Notionのtitleプロパティ設定"""

    type: Literal["title"] = Field(
        "title", description="プロパティタイプ"
    )
    title: EmptyObject = Field(
        default_factory=EmptyObject, description="title設定"
    )
