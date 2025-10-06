from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject
from ....properties.base_properties._base_property import NotionPropertyType


class LastEditedByPropertyConfig(BasePropertyConfig):
    """Notionのlast_edited_byプロパティ設定"""

    type: Literal[NotionPropertyType.LAST_EDITED_BY] = Field(
        NotionPropertyType.LAST_EDITED_BY, description="プロパティタイプ"
    )
    last_edited_by: EmptyObject = Field(
        default_factory=EmptyObject, description="last_edited_by設定"
    )
