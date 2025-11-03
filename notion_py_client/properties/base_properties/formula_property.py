from typing import Any, Literal

from pydantic import Field

from ...models import FormulaResult
from ._base_property import BaseProperty


class FormulaProperty(BaseProperty[Literal["formula"]]):
    """Notionのformulaプロパティ"""

    type: Literal["formula"] = Field("formula", description="プロパティタイプ")

    formula: FormulaResult = Field(..., description="フォーミュラの計算結果")

    def get_display_value(self) -> str | int | float | bool | None:
        """フォーミュラの計算結果を取得

        Returns:
            str | int | float | bool | None: フォーミュラの計算結果

        Note:
            - フォーミュラの型に応じて、string, number, boolean, dateのいずれかの値を返す
            - date型の場合、startとendの両方が存在する場合は "start→end" の形式で返す
            - date型でstartのみ存在する場合はstartを返す
            - フォーミュラが未設定の場合はNoneを返す
        """
        if self.formula.type == "string":
            return self.formula.string
        elif self.formula.type == "number":
            return self.formula.number
        elif self.formula.type == "boolean":
            return self.formula.boolean
        elif self.formula.type == "date":
            if self.formula.date is None:
                return None
            if self.formula.date.start and self.formula.date.end:
                return f"{self.formula.date.start}→{self.formula.date.end}"
            else:
                return self.formula.date.start
        else:
            return None
