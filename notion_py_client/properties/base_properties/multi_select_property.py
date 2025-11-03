from typing import Literal
from pydantic import Field

from ...models import SelectOption
from ._base_property import BaseProperty


class MultiSelectProperty(BaseProperty[Literal["multi_select"]]):
    """Notionのmulti_selectプロパティ"""

    type: Literal["multi_select"] = Field(
        "multi_select", description="プロパティタイプ"
    )

    multi_select: list[SelectOption] = Field(
        default_factory=list, description="選択されたオプション配列"
    )

    def get_display_value(self) -> str | None:
        """選択されたオプション名のリストを取得

        Returns:
            str | None: 選択されたオプション名をカンマ区切りで連結した文字列。選択がない場合はNone
        """
        if len(self.multi_select) == 0:
            return None
        return ", ".join(option.name for option in self.multi_select)
