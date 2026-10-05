"""Agent Skills API response models.

Official list and retrieve payloads from the Agent Skills API and
`@notionhq/client` v5.27.0.
"""

from typing import Literal

from pydantic import BaseModel, Field, StrictStr

from .list_response import ListResponse


class Plugin(BaseModel):
    """One entry from `GET /v1/ai/plugins`."""

    id: StrictStr = Field(..., description="Plugin ID")
    name: StrictStr = Field(..., description="Plugin name")
    description: StrictStr = Field(..., description="Plugin description")
    version_id: StrictStr = Field(..., description="Content version used to skip unchanged downloads")


class ListPluginsResponse(ListResponse[Plugin]):
    """plugins.list() response."""

    type: Literal["plugin"] = Field(..., description="結果の型")
    next_cursor: StrictStr | None = Field(..., description="次ページのカーソル")


class SignedDirectoryResponse(BaseModel):
    """Signed archive URL for a plugin or skill directory.

    The URL points at a temporary gzipped tar archive. This client does not
    download or extract it.
    """

    id: StrictStr = Field(..., description="Plugin or skill ID")
    version_id: StrictStr = Field(..., description="Archive content version")
    url: StrictStr = Field(..., description="Signed archive URL")
