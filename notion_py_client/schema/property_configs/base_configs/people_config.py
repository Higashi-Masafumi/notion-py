from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject
from ....properties.base_properties._base_property import NotionPropertyType


class PeoplePropertyConfig(BasePropertyConfig):
    """Notionのpeopleプロパティ設定"""

    type: Literal[NotionPropertyType.PEOPLE] = Field(
        NotionPropertyType.PEOPLE, description="プロパティタイプ"
    )
    people: EmptyObject = Field(
        default_factory=EmptyObject, description="people設定"
    )
