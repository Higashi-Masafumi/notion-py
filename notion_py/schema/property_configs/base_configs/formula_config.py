from typing import Literal

from pydantic import BaseModel, Field, StrictStr

from ._base_config import BasePropertyConfig
from ....properties.base_properties._base_property import NotionPropertyType


class FormulaExpression(BaseModel):
    """formulaプロパティの式設定"""

    expression: StrictStr | None = Field(None, description="Notionの式")


class FormulaPropertyConfig(BasePropertyConfig):
    """Notionのformulaプロパティ設定"""

    type: Literal[NotionPropertyType.FORMULA] = Field(
        NotionPropertyType.FORMULA, description="プロパティタイプ"
    )
    formula: FormulaExpression = Field(..., description="formula設定")
