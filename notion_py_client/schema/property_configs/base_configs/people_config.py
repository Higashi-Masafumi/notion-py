from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject


class PeoplePropertyConfig(BasePropertyConfig[Literal["people"]]):
    """Notionのpeopleプロパティ設定"""

    type: Literal["people"] = Field(
        "people", description="プロパティタイプ"
    )
    people: EmptyObject = Field(
        default_factory=EmptyObject, description="people設定"
    )
