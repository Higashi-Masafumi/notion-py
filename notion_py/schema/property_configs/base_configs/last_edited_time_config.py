from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject
from ....properties.base_properties._base_property import NotionPropertyType


class LastEditedTimePropertyConfig(BasePropertyConfig):
    """Notionのlast_edited_timeプロパティ設定"""

    type: Literal[NotionPropertyType.LAST_EDITED_TIME] = Field(
        NotionPropertyType.LAST_EDITED_TIME, description="プロパティタイプ"
    )
    last_edited_time: EmptyObject = Field(
        default_factory=EmptyObject, description="last_edited_time設定"
    )
