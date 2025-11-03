from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject


class CheckboxPropertyConfig(
    BasePropertyConfig[Literal["checkbox"]]
):
    """Notionのcheckboxプロパティ設定"""

    type: Literal["checkbox"] = Field(
        "checkbox", description="プロパティタイプ"
    )
    checkbox: EmptyObject = Field(
        default_factory=EmptyObject, description="checkbox設定"
    )
