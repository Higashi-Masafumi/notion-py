from typing import Literal

from pydantic import Field

from ...models import FileWithName
from ._base_property import BaseProperty


class FilesProperty(BaseProperty[Literal["files"]]):
    """Notionのfilesプロパティ"""

    type: Literal["files"] = Field("files", description="プロパティタイプ")

    files: list[FileWithName] = Field(
        default_factory=list, description="ファイル情報のリスト"
    )

    def get_display_value(self) -> str | None:
        """ファイル名のリストを取得

        Returns:
            str | None: ファイル名をカンマ区切りで連結した文字列。ファイルがない場合はNone
        """
        if len(self.files) == 0:
            return None
        return ", ".join(file.name for file in self.files)
