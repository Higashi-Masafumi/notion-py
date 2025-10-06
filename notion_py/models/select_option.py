from pydantic import BaseModel, Field, StrictStr


class SelectOption(BaseModel):
    """Notionのセレクトオプション"""

    id: StrictStr = Field(..., description="オプションID")
    name: StrictStr = Field(..., description="オプション名")
    color: StrictStr = Field(..., description="色")
    description: StrictStr | None = Field(
        None, description="オプションの説明"
    )
