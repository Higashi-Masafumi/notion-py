from pydantic import BaseModel, Field, StrictBool, StrictFloat, StrictInt, StrictStr

from .date_info import DateInfo


class FormulaResult(BaseModel):
    """Notionのformula結果"""

    type: StrictStr = Field(..., description="結果タイプ（string、number、boolean等）")
    string: StrictStr | None = Field(
        None, description="文字列結果（typeがstringの場合）"
    )
    number: StrictInt | StrictFloat | None = Field(
        None, description="数値結果（typeがnumberの場合）"
    )
    boolean: StrictBool | None = Field(
        None, description="真偽値結果（typeがbooleanの場合）"
    )
    date: DateInfo | None = Field(
        None, description="日付結果（typeがdateの場合）"
    )
