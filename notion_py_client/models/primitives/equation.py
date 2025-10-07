from pydantic import BaseModel, Field, StrictStr


class Equation(BaseModel):
    """Notionのequationオブジェクト"""

    expression: StrictStr = Field(..., description="KaTeX互換の式")
