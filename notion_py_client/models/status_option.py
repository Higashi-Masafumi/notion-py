from pydantic import BaseModel, Field, StrictStr


class StatusOption(BaseModel):
    """Notionのステータスオプション"""

    id: StrictStr = Field(..., description="ステータスID")
    name: StrictStr = Field(..., description="ステータス名")
    color: StrictStr = Field(..., description="色")
    description: StrictStr | None = Field(None, description="ステータスの説明")
