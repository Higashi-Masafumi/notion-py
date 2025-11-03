from typing import Literal
from pydantic import Field, StrictBool

from ._base_property import BaseProperty


class CheckboxProperty(BaseProperty[Literal["checkbox"]]):
    """Notionのcheckboxプロパティ"""

    type: Literal["checkbox"] = Field("checkbox", description="プロパティタイプ")

    checkbox: StrictBool = Field(False, description="チェックボックスの状態")

    def get_display_value(self) -> bool:
        """チェックボックスの状態を取得

        Returns:
            StrictBool | None: チェックボックスの状態（True or False）
        """
        return self.checkbox
