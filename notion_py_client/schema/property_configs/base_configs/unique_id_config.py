from typing import Literal

from pydantic import BaseModel, Field, StrictStr

from ._base_config import BasePropertyConfig


class UniqueIdOptions(BaseModel):
    """unique_idプロパティの設定"""

    prefix: StrictStr | None = Field(None, description="ユニークIDのプレフィックス")


class UniqueIdPropertyConfig(
    BasePropertyConfig[Literal["unique_id"]]
):
    """Notionのunique_idプロパティ設定"""

    type: Literal["unique_id"] = Field(
        "unique_id", description="プロパティタイプ"
    )
    unique_id: UniqueIdOptions = Field(
        default_factory=lambda: UniqueIdOptions(prefix=None),
        description="unique_id設定",
    )
