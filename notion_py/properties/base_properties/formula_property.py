from typing import Any, Literal

from pydantic import Field

from ...models import FormulaResult
from ._base_property import BaseProperty, NotionPropertyType


class FormulaProperty(BaseProperty):
    """Notionのformulaプロパティ"""

    type: Literal[NotionPropertyType.FORMULA] = Field(
        NotionPropertyType.FORMULA, description="プロパティタイプ"
    )

    formula: FormulaResult = Field(..., description="フォーミュラの計算結果")

    def get_value(self) -> Any:
        """
        formula プロパティから計算結果を型に応じて動的に取得

        Returns:
            Any: 計算結果の型に応じた値（str, int, float, bool, None）

        Note:
            - formulaプロパティはNotionで設定された数式の計算結果です
            - 結果の型は実行時まで不明で、動的に決定されます

        Examples:
            - 文字列結果: "結果文字列"
            - 数値結果: 42 または 3.14
            - 真偽値結果: True または False
            - エラー/未定義: None
        """
        match self.formula.type:
            case "string":
                return self.formula.string
            case "number":
                return self.formula.number
            case "boolean":
                return self.formula.boolean
            case "date":
                return self.formula.date
            case _:
                # 未知の型の場合はNoneを返す
                return None
