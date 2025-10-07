from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject
from ....properties.base_properties._base_property import NotionPropertyType


class EmailPropertyConfig(BasePropertyConfig):
    """Notionのemailプロパティ設定"""

    type: Literal[NotionPropertyType.EMAIL] = Field(
        NotionPropertyType.EMAIL, description="プロパティタイプ"
    )
    email: EmptyObject = Field(
        default_factory=EmptyObject, description="email設定"
    )
