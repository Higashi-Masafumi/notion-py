from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject
from ....properties.base_properties._base_property import NotionPropertyType


class StatusPropertyConfig(BasePropertyConfig):
    """Notionのstatusプロパティ設定"""

    type: Literal[NotionPropertyType.STATUS] = Field(
        NotionPropertyType.STATUS, description="プロパティタイプ"
    )
    status: EmptyObject = Field(
        default_factory=EmptyObject, description="status設定"
    )
