from typing import Literal

from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr


class FileUploadCreatedBy(BaseModel):
    """file_upload.created_by の最小表現

    type は person | bot | agent のいずれか。
    """

    id: StrictStr
    type: Literal["person", "bot", "agent"]


class FileImportError(BaseModel):
    type: Literal[
        "validation_error",
        "internal_system_error",
        "download_error",
        "upload_error",
    ]
    code: StrictStr
    message: StrictStr
    parameter: StrictStr | None = None
    status_code: StrictInt | None = None


class FileImportResult(BaseModel):
    imported_time: StrictStr
    type: Literal["success", "error"]
    success: dict | None = None
    error: FileImportError | None = None


class FileUploadObject(BaseModel):
    """TypeScript: FileUploadObjectResponse"""

    object: Literal["file_upload"]
    id: StrictStr
    created_time: StrictStr
    created_by: FileUploadCreatedBy
    last_edited_time: StrictStr
    archived: StrictBool
    expiry_time: StrictStr | None
    status: Literal["pending", "uploaded", "expired", "failed"]
    filename: StrictStr | None = None
    content_type: StrictStr | None = None
    content_length: StrictInt | None = None
    upload_url: StrictStr | None = None
    complete_url: StrictStr | None = None
    file_import_result: FileImportResult | None = None
    number_of_parts: dict[str, StrictInt] | None = Field(
        None, description='{"total": n, "sent": m}'
    )
