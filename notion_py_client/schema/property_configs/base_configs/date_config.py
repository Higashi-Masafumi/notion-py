from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject
from ....properties.base_properties._base_property import NotionPropertyType


class DatePropertyConfig(BasePropertyConfig):
    """Notionのdateプロパティ設定"""

    type: Literal[NotionPropertyType.DATE] = Field(
        NotionPropertyType.DATE, description="プロパティタイプ"
    )
    date: EmptyObject = Field(
        default_factory=EmptyObject, description="date設定"
    )
