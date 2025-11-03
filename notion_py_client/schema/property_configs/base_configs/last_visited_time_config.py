from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject


class LastVisitedTimePropertyConfig(
    BasePropertyConfig[Literal["last_visited_time"]]
):
    """Notionのlast_visited_timeプロパティ設定

    TypeScript: LastVisitedTimePropertyConfigurationRequest
    フィールドは空オブジェクトで構成されます。
    """

    type: Literal["last_visited_time"] = Field(
        "last_visited_time", description="プロパティタイプ"
    )
    last_visited_time: EmptyObject = Field(
        default_factory=EmptyObject, description="last_visited_time設定"
    )

