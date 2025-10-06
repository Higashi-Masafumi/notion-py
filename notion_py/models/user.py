from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr

from .primitives import EmptyObject


class Person(BaseModel):
    """personタイプの詳細情報"""

    email: StrictStr | None = Field(None, description="メールアドレス")


class PartialUser(BaseModel):
    """Notionの部分ユーザー情報"""

    object: Literal["user"] = Field("user", description="オブジェクトタイプ")
    id: StrictStr = Field(..., description="ユーザーID")


class BaseFullUser(PartialUser):
    """共通のユーザー情報"""

    name: StrictStr | None = Field(None, description="ユーザー名")
    avatar_url: StrictStr | None = Field(None, description="アバターURL")


class PersonUser(BaseFullUser):
    """personタイプのユーザー"""

    type: Literal["person"] = Field("person", description="ユーザータイプ")
    person: Person | None = Field(None, description="personタイプの詳細")


class BotOwnerUser(BaseModel):
    """botユーザーのオーナーがユーザーの場合の情報"""

    type: Literal["user"] = Field("user", description="オーナータイプ")
    user: PartialUser | PersonUser = Field(..., description="オーナーユーザー情報")


class BotOwnerWorkspace(BaseModel):
    """botユーザーのオーナーがワークスペースの場合の情報"""

    type: Literal["workspace"] = Field(
        "workspace", description="オーナータイプ"
    )
    workspace: StrictBool = Field(True, description="ワークスペースフラグ")


class BotWorkspaceLimits(BaseModel):
    """ワークスペースの制限情報"""

    max_file_upload_size_in_bytes: StrictInt = Field(
        ..., description="最大アップロードサイズ（バイト）"
    )


class BotInfo(BaseModel):
    """botタイプユーザーの詳細情報"""

    owner: BotOwnerUser | BotOwnerWorkspace = Field(
        ..., description="Botのオーナー情報"
    )
    workspace_name: StrictStr | None = Field(
        None, description="Botの所属ワークスペース名"
    )
    workspace_limits: BotWorkspaceLimits = Field(
        ..., description="ワークスペースの制限"
    )


class BotUser(BaseFullUser):
    """botタイプのユーザー"""

    type: Literal["bot"] = Field("bot", description="ユーザータイプ")
    bot: EmptyObject | BotInfo = Field(
        default_factory=EmptyObject, description="Bot固有の情報"
    )


User = PersonUser | BotUser
"""NotionのユーザーのUnion型"""


class Group(BaseModel):
    """Notionのグループ情報"""

    object: Literal["group"] = Field("group", description="オブジェクトタイプ")
    id: StrictStr = Field(..., description="グループID")
    name: StrictStr | None = Field(None, description="グループ名")
