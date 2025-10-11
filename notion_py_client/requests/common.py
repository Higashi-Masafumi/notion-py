"""Common request types used across Notion API requests.

基本的なリクエスト型の定義。
TypeScript SDKの定義に準拠しています。
"""

from typing import Literal

from pydantic import BaseModel, Field, StrictBool, StrictStr

# 基本型エイリアス
IdRequest = str
StringRequest = str
TextRequest = str
EmojiRequest = str
TimeZoneRequest = str


class AnnotationRequest(BaseModel):
    """テキストの装飾情報（太字、斜体など）."""

    bold: StrictBool | None = None
    italic: StrictBool | None = None
    strikethrough: StrictBool | None = None
    underline: StrictBool | None = None
    code: StrictBool | None = None
    color: str | None = None  # ApiColor


class DateRequest(BaseModel):
    """日付リクエスト."""

    start: StrictStr
    end: StrictStr | None = None
    time_zone: TimeZoneRequest | None = None


class PartialUserObjectRequest(BaseModel):
    """部分的なユーザーオブジェクト（ID参照用）."""

    id: IdRequest
    object: Literal["user"] | None = None


class GroupObjectRequest(BaseModel):
    """グループオブジェクト."""

    id: IdRequest
    name: StrictStr | None = None
    object: Literal["group"] | None = None


class RelationItemRequest(BaseModel):
    """リレーションプロパティのアイテム."""

    id: IdRequest


# Select/MultiSelect/Status用の選択肢リクエスト
class SelectPropertyItemRequest(BaseModel):
    """Select/MultiSelect/Status用の選択肢.

    IDまたは名前のいずれかで指定可能。
    """

    id: StringRequest | None = None
    name: TextRequest | None = None
    color: str | None = None  # SelectColor
    description: TextRequest | None = None

    class Config:
        """Pydantic設定."""

        # IDまたは名前のいずれかが必須
        # どちらも指定された場合はIDが優先される
        pass


# ===== Files (request payloads) =====


class InternalFileRequest(BaseModel):
    """内部ファイルの参照（Notionが発行する一時URL）."""

    url: StrictStr
    expiry_time: StrictStr | None = None


class ExternalFileRequest(BaseModel):
    """外部ファイルの参照."""

    url: TextRequest


class InternalOrExternalFileWithNameRequest(BaseModel):
    """filesプロパティ用: 内部/外部ファイル + 名前."""

    type: Literal["file", "external"] | None = None
    name: StringRequest
    file: InternalFileRequest | None = None
    external: ExternalFileRequest | None = None


class FileUploadIdRequest(BaseModel):
    """ファイルアップロードID参照."""

    id: IdRequest


class FileUploadWithOptionalNameRequest(BaseModel):
    """filesプロパティ用: file_upload 参照 + 任意の名前."""

    type: Literal["file_upload"] | None = None
    file_upload: FileUploadIdRequest
    name: StringRequest | None = None


# ===== Page icon / cover (request payloads) =====


class FileUploadPageIconRequest(BaseModel):
    type: Literal["file_upload"] | None = None
    file_upload: FileUploadIdRequest


class EmojiPageIconRequest(BaseModel):
    type: Literal["emoji"] | None = None
    emoji: EmojiRequest


class ExternalPageIconRequest(BaseModel):
    type: Literal["external"] | None = None
    external: ExternalFileRequest


class CustomEmojiRef(BaseModel):
    id: IdRequest
    name: StrictStr | None = None
    url: StrictStr | None = None


class CustomEmojiPageIconRequest(BaseModel):
    type: Literal["custom_emoji"] | None = None
    custom_emoji: CustomEmojiRef


PageIconRequest = (
    FileUploadPageIconRequest
    | EmojiPageIconRequest
    | ExternalPageIconRequest
    | CustomEmojiPageIconRequest
)


class FileUploadPageCoverRequest(BaseModel):
    type: Literal["file_upload"] | None = None
    file_upload: FileUploadIdRequest


class ExternalPageCoverRequest(BaseModel):
    type: Literal["external"] | None = None
    external: ExternalFileRequest


PageCoverRequest = FileUploadPageCoverRequest | ExternalPageCoverRequest
