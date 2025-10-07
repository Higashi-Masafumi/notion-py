from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject
from ....properties.base_properties._base_property import NotionPropertyType


class VerificationPropertyConfig(BasePropertyConfig):
    """Notionのverificationプロパティ設定"""

    type: Literal[NotionPropertyType.VERIFICATION] = Field(
        NotionPropertyType.VERIFICATION, description="プロパティタイプ"
    )
    verification: EmptyObject = Field(
        default_factory=EmptyObject, description="verification設定"
    )
