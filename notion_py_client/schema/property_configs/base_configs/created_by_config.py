from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject


class CreatedByPropertyConfig(
    BasePropertyConfig[Literal["created_by"]]
):
    """Notionのcreated_byプロパティ設定"""

    type: Literal["created_by"] = Field(
        "created_by", description="プロパティタイプ"
    )
    created_by: EmptyObject = Field(
        default_factory=EmptyObject, description="created_by設定"
    )
