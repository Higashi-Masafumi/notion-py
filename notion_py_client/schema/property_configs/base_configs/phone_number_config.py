from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject
from ....properties.base_properties._base_property import NotionPropertyType


class PhoneNumberPropertyConfig(BasePropertyConfig):
    """Notionのphone_numberプロパティ設定"""

    type: Literal[NotionPropertyType.PHONE_NUMBER] = Field(
        NotionPropertyType.PHONE_NUMBER, description="プロパティタイプ"
    )
    phone_number: EmptyObject = Field(
        default_factory=EmptyObject, description="phone_number設定"
    )
