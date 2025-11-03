from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject


class DatePropertyConfig(BasePropertyConfig[Literal["date"]]):
    """Notionのdateプロパティ設定"""

    type: Literal["date"] = Field(
        "date", description="プロパティタイプ"
    )
    date: EmptyObject = Field(
        default_factory=EmptyObject, description="date設定"
    )
