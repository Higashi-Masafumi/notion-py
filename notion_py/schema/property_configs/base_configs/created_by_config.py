from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject
from ....properties.base_properties._base_property import NotionPropertyType


class CreatedByPropertyConfig(BasePropertyConfig):
    """Notionのcreated_byプロパティ設定"""

    type: Literal[NotionPropertyType.CREATED_BY] = Field(
        NotionPropertyType.CREATED_BY, description="プロパティタイプ"
    )
    created_by: EmptyObject = Field(
        default_factory=EmptyObject, description="created_by設定"
    )
