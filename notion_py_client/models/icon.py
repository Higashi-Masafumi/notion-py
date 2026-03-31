"""
Notionアイコンモデル

Database、Page、DataSourceなどで使用されるアイコンの定義
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field, StrictStr, model_validator

from .file import ExternalFile, InternalFile
from .primitives import CustomEmoji


class IconType(str, Enum):
    """アイコンタイプ"""

    ICON = "icon"
    EMOJI = "emoji"
    EXTERNAL = "external"
    FILE = "file"
    CUSTOM_EMOJI = "custom_emoji"


class NativeIcon(BaseModel):
    """Notionのネイティブアイコン"""

    name: StrictStr = Field(..., description="アイコン名")
    color: StrictStr | None = Field(None, description="アイコン色")


class NotionIcon(BaseModel):
    """
    Notionのアイコン（絵文字、外部画像、内部ファイル）

    Database、Page、DataSourceで共通使用

    Examples:
        ```python
        # 絵文字アイコン
        emoji_icon = NotionIcon(type=IconType.EMOJI, emoji="📝")

        # 外部画像アイコン
        external_icon = NotionIcon(
            type=IconType.EXTERNAL,
            external=ExternalFile(url="https://example.com/icon.png")
        )

        # 内部ファイルアイコン
        file_icon = NotionIcon(
            type=IconType.FILE,
            file=InternalFile(url="https://notion.so/...", expiry_time="...")
        )
        ```
    """

    type: IconType = Field(..., description="アイコンタイプ")
    icon: NativeIcon | None = Field(
        None, description="ネイティブアイコン（typeがiconの場合のみ）"
    )
    emoji: StrictStr | None = Field(None, description="絵文字アイコン")
    external: ExternalFile | None = Field(None, description="外部ファイル")
    file: InternalFile | None = Field(None, description="内部ファイル")
    custom_emoji: CustomEmoji | None = Field(
        None, description="カスタム絵文字（typeがcustom_emojiの場合のみ）"
    )

    @model_validator(mode="before")
    @classmethod
    def normalize_icon_shape(cls, value: object) -> object:
        if not isinstance(value, dict):
            return value

        normalized = dict(value)

        if "type" not in normalized:
            for icon_type in ("icon", "emoji", "external", "file", "custom_emoji"):
                if icon_type in normalized:
                    normalized["type"] = icon_type
                    break

        if normalized.get("type") == "icon" and "icon" not in normalized:
            name = normalized.get("name")
            color = normalized.get("color")
            if name is not None:
                normalized["icon"] = {
                    "name": name,
                    **({"color": color} if color is not None else {}),
                }

        if (
            normalized.get("type") == "icon"
            and isinstance(normalized.get("icon"), str)
        ):
            normalized["icon"] = {"name": normalized["icon"]}

        if "in_trash" in normalized and "archived" not in normalized:
            normalized["archived"] = normalized["in_trash"]
        if "archived" in normalized and "in_trash" not in normalized:
            normalized["in_trash"] = normalized["archived"]

        return normalized
