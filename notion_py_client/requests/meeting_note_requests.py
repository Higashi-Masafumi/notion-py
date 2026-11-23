"""Full-page meeting note request types.

POST /v1/meeting_notes and PATCH /v1/meeting_notes/{meeting_note_id}.
"""

from typing import Literal

from pydantic import BaseModel, Field, StrictBool, StrictStr, model_validator

from ..models.parent import DataSourceParent, PageParent
from .common import IdRequest


class MeetingNoteCalendarRequest(BaseModel):
    """Calendar that owns the event."""

    account_id: StrictStr = Field(..., min_length=1)
    calendar_id: StrictStr = Field(..., min_length=1)


class MeetingNoteCalendarEventRequest(BaseModel):
    """Calendar event used to find or link a full-page meeting note."""

    calendar: MeetingNoteCalendarRequest
    event_id: StrictStr = Field(..., min_length=1)


class CreateMeetingNotePageParameters(BaseModel):
    """Create a full-page meeting note, or get or create one for a calendar event.

    `calendar_event` cannot be combined with `parent`, `title`, or `markdown`.
    Omit every field to create the note in the user's meeting notes database.
    """

    parent: PageParent | DataSourceParent | None = None
    title: StrictStr | None = Field(None, max_length=2000)
    markdown: str | None = None
    calendar_event: MeetingNoteCalendarEventRequest | None = None
    markdown_version: Literal["v1", "v2"] | None = None

    @model_validator(mode="after")
    def validate_calendar_event_exclusivity(self) -> "CreateMeetingNotePageParameters":
        if self.calendar_event is not None and (
            self.parent is not None
            or self.title is not None
            or self.markdown is not None
        ):
            raise ValueError(
                "calendar_event cannot be combined with parent, title, or markdown"
            )
        return self


class LinkMeetingNotePageParameters(BaseModel):
    """Link a full-page meeting note to a calendar event."""

    meeting_note_id: IdRequest
    calendar_event: MeetingNoteCalendarEventRequest
    allow_other_meeting_notes: StrictBool | None = None
