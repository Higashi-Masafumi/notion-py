from typing import Literal

from pydantic import Field

from ...models import UniqueId
from ._base_property import BaseProperty


class UniqueIdProperty(BaseProperty[Literal["unique_id"]]):
    """Notionのunique_idプロパティ"""

    type: Literal["unique_id"] = Field("unique_id", description="プロパティタイプ")

    unique_id: UniqueId = Field(..., description="ユニークIDの値")

    def get_display_value(self) -> str | None:
        """ユニークIDの表示値を取得

        - prefix と number の両方がある場合は `PREFIX-<number>`
        - number のみ: `<number>`
        - prefix のみ: `prefix`
        - どちらも無い場合: None
        """
        prefix = getattr(self.unique_id, "prefix", None)
        number = getattr(self.unique_id, "number", None)
        if prefix and number is not None:
            return f"{prefix}-{number}"
        if number is not None:
            return str(number)
        if prefix:
            return prefix
        return None
