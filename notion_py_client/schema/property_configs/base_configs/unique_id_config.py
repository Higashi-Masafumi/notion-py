from typing import Literal

from pydantic import BaseModel, Field, StrictStr

from ._base_config import BasePropertyConfig
from ....properties.base_properties._base_property import NotionPropertyType


class UniqueIdOptions(BaseModel):
    """unique_idプロパティの設定"""

    prefix: StrictStr | None = Field(None, description="ユニークIDのプレフィックス")


class UniqueIdPropertyConfig(BasePropertyConfig):
    """Notionのunique_idプロパティ設定"""

    type: Literal[NotionPropertyType.UNIQUE_ID] = Field(
        NotionPropertyType.UNIQUE_ID, description="プロパティタイプ"
    )
    unique_id: UniqueIdOptions = Field(
        default_factory=lambda: UniqueIdOptions(prefix=None),
        description="unique_id設定",
    )
