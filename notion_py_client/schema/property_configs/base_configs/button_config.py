from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject


class ButtonPropertyConfig(BasePropertyConfig[Literal["button"]]):
    """Notionのbuttonプロパティ設定"""

    type: Literal["button"] = Field(
        "button", description="プロパティタイプ"
    )
    button: EmptyObject = Field(default_factory=EmptyObject, description="button設定")
