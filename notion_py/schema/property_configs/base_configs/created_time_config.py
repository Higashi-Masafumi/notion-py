from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject
from ....properties.base_properties._base_property import NotionPropertyType


class CreatedTimePropertyConfig(BasePropertyConfig):
    """Notionのcreated_timeプロパティ設定"""

    type: Literal[NotionPropertyType.CREATED_TIME] = Field(
        NotionPropertyType.CREATED_TIME, description="プロパティタイプ"
    )
    created_time: EmptyObject = Field(
        default_factory=EmptyObject, description="created_time設定"
    )
