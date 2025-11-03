from typing import Literal

from pydantic import BaseModel, Field, StrictStr

from ._base_config import BasePropertyConfig


class FormulaExpression(BaseModel):
    """formulaプロパティの式設定"""

    expression: StrictStr | None = Field(None, description="Notionの式")


class FormulaPropertyConfig(BasePropertyConfig[Literal["formula"]]):
    """Notionのformulaプロパティ設定"""

    type: Literal["formula"] = Field(
        "formula", description="プロパティタイプ"
    )
    formula: FormulaExpression = Field(..., description="formula設定")
