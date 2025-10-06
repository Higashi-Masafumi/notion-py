from pydantic import BaseModel, Field, StrictInt, StrictStr


class UniqueId(BaseModel):
    """Notionのunique_id値"""

    prefix: StrictStr | None = Field(None, description="ユニークIDのプレフィックス")
    number: StrictInt | None = Field(None, description="ユニークIDの番号")
