from typing import Literal
from pydantic import Field

from ...models import SelectOption
from ._base_property import BaseProperty


class SelectProperty(BaseProperty[Literal["select"]]):
    """Notionのselectプロパティ"""

    type: Literal["select"] = Field("select", description="プロパティタイプ")

    select: SelectOption | None = Field(
        None, description="選択されたオプション（設定されていない場合はnull）"
    )

    def get_display_value(self) -> str | None:
        """選択されたオプション名を取得

        Returns:
            str | None: 選択されたオプション名。未設定の場合はNone
        """
        if self.select is None:
            return None
        return self.select.name
