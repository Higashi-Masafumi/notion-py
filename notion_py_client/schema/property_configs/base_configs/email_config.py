from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject


class EmailPropertyConfig(BasePropertyConfig[Literal["email"]]):
    """Notionのemailプロパティ設定"""

    type: Literal["email"] = Field(
        "email", description="プロパティタイプ"
    )
    email: EmptyObject = Field(
        default_factory=EmptyObject, description="email設定"
    )
