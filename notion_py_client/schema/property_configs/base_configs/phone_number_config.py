from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject


class PhoneNumberPropertyConfig(
    BasePropertyConfig[Literal["phone_number"]]
):
    """Notionのphone_numberプロパティ設定"""

    type: Literal["phone_number"] = Field(
        "phone_number", description="プロパティタイプ"
    )
    phone_number: EmptyObject = Field(
        default_factory=EmptyObject, description="phone_number設定"
    )
