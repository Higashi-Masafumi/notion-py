from pydantic import BaseModel, model_validator


class EmptyObject(BaseModel):
    """Notionで空オブジェクトを表すプレースホルダ"""

    @model_validator(mode="before")
    @classmethod
    def ensure_empty(cls, value: object) -> dict:
        if value in (None, {}):
            return {}
        if isinstance(value, dict) and not value:
            return value
        raise ValueError("EmptyObject expects an empty dict")
