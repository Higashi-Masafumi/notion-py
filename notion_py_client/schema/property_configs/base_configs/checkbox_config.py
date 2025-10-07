from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject
from ....properties.base_properties._base_property import NotionPropertyType


class CheckboxPropertyConfig(BasePropertyConfig):
    """Notionのcheckboxプロパティ設定"""

    type: Literal[NotionPropertyType.CHECKBOX] = Field(
        NotionPropertyType.CHECKBOX, description="プロパティタイプ"
    )
    checkbox: EmptyObject = Field(
        default_factory=EmptyObject, description="checkbox設定"
    )
