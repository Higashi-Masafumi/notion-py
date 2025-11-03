from typing import Literal

from pydantic import Field

from ._base_config import BasePropertyConfig
from ....models.primitives import EmptyObject


class FilesPropertyConfig(BasePropertyConfig[Literal["files"]]):
    """Notionのfilesプロパティ設定"""

    type: Literal["files"] = Field(
        "files", description="プロパティタイプ"
    )
    files: EmptyObject = Field(
        default_factory=EmptyObject, description="files設定"
    )
