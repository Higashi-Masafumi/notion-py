from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject
from ....properties.base_properties._base_property import NotionPropertyType


class ButtonPropertyConfig(BasePropertyConfig):
    """Notionのbuttonプロパティ設定"""

    type: Literal[NotionPropertyType.BUTTON] = Field(
        NotionPropertyType.BUTTON, description="プロパティタイプ"
    )
    button: EmptyObject = Field(default_factory=EmptyObject, description="button設定")
