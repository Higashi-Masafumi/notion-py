from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject
from ....properties.base_properties._base_property import NotionPropertyType


class FilesPropertyConfig(BasePropertyConfig):
    """Notionのfilesプロパティ設定"""

    type: Literal[NotionPropertyType.FILES] = Field(
        NotionPropertyType.FILES, description="プロパティタイプ"
    )
    files: EmptyObject = Field(
        default_factory=EmptyObject, description="files設定"
    )
