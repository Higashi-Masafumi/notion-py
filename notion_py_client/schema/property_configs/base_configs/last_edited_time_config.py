from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject


class LastEditedTimePropertyConfig(
    BasePropertyConfig[Literal["last_edited_time"]]
):
    """Notionのlast_edited_timeプロパティ設定"""

    type: Literal["last_edited_time"] = Field(
        "last_edited_time", description="プロパティタイプ"
    )
    last_edited_time: EmptyObject = Field(
        default_factory=EmptyObject, description="last_edited_time設定"
    )
