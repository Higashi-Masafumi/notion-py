from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject
from ....properties.base_properties._base_property import NotionPropertyType


class LastVisitedTimePropertyConfig(
    BasePropertyConfig[Literal[NotionPropertyType.LAST_VISITED_TIME]]
):
    """Notionのlast_visited_timeプロパティ設定

    TypeScript: LastVisitedTimePropertyConfigurationRequest
    フィールドは空オブジェクトで構成されます。
    """

    type: Literal[NotionPropertyType.LAST_VISITED_TIME] = Field(
        NotionPropertyType.LAST_VISITED_TIME, description="プロパティタイプ"
    )
    last_visited_time: EmptyObject = Field(
        default_factory=EmptyObject, description="last_visited_time設定"
    )

