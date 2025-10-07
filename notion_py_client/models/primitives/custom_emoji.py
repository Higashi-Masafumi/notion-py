from pydantic import BaseModel, Field, StrictStr


class CustomEmoji(BaseModel):
    """Notionのcustom_emojiメンション"""

    id: StrictStr = Field(..., description="カスタム絵文字ID")
    name: StrictStr | None = Field(None, description="カスタム絵文字名")
    url: StrictStr | None = Field(None, description="カスタム絵文字URL")
