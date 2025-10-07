from typing import Literal

from pydantic import Field

from ...models import FileWithName
from ._base_property import BaseProperty, NotionPropertyType


class FilesProperty(BaseProperty):
    """Notionのfilesプロパティ"""

    type: Literal[NotionPropertyType.FILES] = Field(
        NotionPropertyType.FILES, description="プロパティタイプ"
    )

    files: list[FileWithName] = Field(
        default_factory=list, description="ファイル情報のリスト"
    )

    def get_value(self) -> list[str]:
        """files プロパティからURLのリストを取得"""
        urls: list[str] = []
        for file_item in self.files:
            if file_item.type == "file" and file_item.file:
                urls.append(file_item.file.url)
            elif file_item.type == "external" and file_item.external:
                urls.append(file_item.external.url)
        return urls
