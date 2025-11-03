from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject


class VerificationPropertyConfig(
    BasePropertyConfig[Literal["verification"]]
):
    """Notionのverificationプロパティ設定"""

    type: Literal["verification"] = Field(
        "verification", description="プロパティタイプ"
    )
    verification: EmptyObject = Field(
        default_factory=EmptyObject, description="verification設定"
    )
