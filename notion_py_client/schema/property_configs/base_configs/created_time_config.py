from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject


class CreatedTimePropertyConfig(
    BasePropertyConfig[Literal["created_time"]]
):
    """Notionのcreated_timeプロパティ設定"""

    type: Literal["created_time"] = Field(
        "created_time", description="プロパティタイプ"
    )
    created_time: EmptyObject = Field(
        default_factory=EmptyObject, description="created_time設定"
    )
