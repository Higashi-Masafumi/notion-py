from pydantic import BaseModel, Field, StrictStr


class DateInfo(BaseModel):
    """Notionの日付情報"""

    start: StrictStr = Field(..., description="開始日（ISO8601形式）")
    end: StrictStr | None = Field(
        None, description="終了日（ISO8601形式、範囲でない場合はnull）"
    )
    time_zone: StrictStr | None = Field(None, description="タイムゾーン")
