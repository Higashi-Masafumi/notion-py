from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject


class UrlPropertyConfig(BasePropertyConfig[Literal["url"]]):
    """Notionのurlプロパティ設定"""

    type: Literal["url"] = Field(
        "url", description="プロパティタイプ"
    )
    url: EmptyObject = Field(
        default_factory=EmptyObject, description="url設定"
    )
