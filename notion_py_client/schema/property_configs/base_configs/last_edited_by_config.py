from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject


class LastEditedByPropertyConfig(
    BasePropertyConfig[Literal["last_edited_by"]]
):
    """Notionのlast_edited_byプロパティ設定"""

    type: Literal["last_edited_by"] = Field(
        "last_edited_by", description="プロパティタイプ"
    )
    last_edited_by: EmptyObject = Field(
        default_factory=EmptyObject, description="last_edited_by設定"
    )
