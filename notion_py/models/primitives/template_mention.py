from typing import Literal

from pydantic import BaseModel, Field


class TemplateMentionDate(BaseModel):
    """today/now を参照するテンプレートメンション"""

    type: Literal["template_mention_date"] = Field(
        "template_mention_date", description="テンプレートメンションタイプ"
    )
    template_mention_date: Literal["today", "now"] = Field(
        ..., description="参照される日付"
    )


class TemplateMentionUser(BaseModel):
    """me を参照するテンプレートメンション"""

    type: Literal["template_mention_user"] = Field(
        "template_mention_user", description="テンプレートメンションタイプ"
    )
    template_mention_user: Literal["me"] = Field(
        ..., description="参照されるユーザー"
    )


TemplateMention = TemplateMentionDate | TemplateMentionUser
