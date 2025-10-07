from typing import Literal

from pydantic import BaseModel, Field, StrictStr


class InternalFile(BaseModel):
    """Notionの内部ファイル"""

    url: StrictStr = Field(..., description="ファイルURL")
    expiry_time: StrictStr = Field(..., description="URLの有効期限")


class ExternalFile(BaseModel):
    """Notionの外部ファイル"""

    url: StrictStr = Field(..., description="外部リソースURL")


class FileWithName(BaseModel):
    """Notionのファイル（名前付き）"""

    name: StrictStr = Field(..., description="ファイル名")
    type: Literal["file", "external"] = Field(
        ..., description="ファイルタイプ"
    )
    file: InternalFile | None = Field(
        None, description="内部ファイル（typeがfileの場合のみ）"
    )
    external: ExternalFile | None = Field(
        None, description="外部ファイル（typeがexternalの場合のみ）"
    )


class FileObject(BaseModel):
    """Notionのfilesプロパティが保持するファイルオブジェクト"""

    files: list[FileWithName] = Field(
        default_factory=list, description="ファイルのリスト"
    )

    def get_urls(self) -> list[str]:
        """ファイルに紐づくURLの一覧を取得"""
        urls: list[str] = []
        for file_item in self.files:
            if file_item.type == "file" and file_item.file:
                urls.append(file_item.file.url)
            elif file_item.type == "external" and file_item.external:
                urls.append(file_item.external.url)
        return urls
