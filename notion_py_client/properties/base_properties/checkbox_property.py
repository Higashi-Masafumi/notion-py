from typing import Literal
from pydantic import Field, StrictBool

from ._base_property import BaseProperty, NotionPropertyType


class CheckboxProperty(BaseProperty[Literal[NotionPropertyType.CHECKBOX]]):
    """Notionのcheckboxプロパティ"""

    type: Literal[NotionPropertyType.CHECKBOX] = Field(
        NotionPropertyType.CHECKBOX, description="プロパティタイプ"
    )

    checkbox: StrictBool = Field(False, description="チェックボックスの状態")

    def get_display_value(self) -> str | int | float | StrictBool | None:
        """チェックボックスの状態を取得

        Returns:
            StrictBool | None: チェックボックスの状態（True or False）
        """
        return self.checkbox
