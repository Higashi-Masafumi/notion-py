# Meeting Notes API

Create a full-page meeting note, or link one to a calendar event.

Block endpoints still return meeting notes as `meeting_notes` blocks. Those blocks include `is_full_page`, and `calendar_event.event_id` when the note is linked to an event. Query existing notes with `blocks.meetingNotes.query()`.

These endpoints accept personal access tokens and Workers. A Worker must pass `parent` and cannot pass `calendar_event` on create.

## Methods

### create

Create a full-page meeting note, or return the existing note for a calendar event.

```python
async def create(
    params: CreateMeetingNotePageParameters | None = None,
    *,
    auth: AuthParam | None = None
) -> CreateMeetingNotePageResponse
```

`calendar_event` cannot be combined with `parent`, `title`, or `markdown`. Omit every field to create the note in the user's meeting notes database. `created` is `false` when the call returns an event's existing note.

**Example**:

```python
from notion_py_client import CreateMeetingNotePageParameters, NotionAsyncClient

async with NotionAsyncClient(auth="secret_xxx") as client:
    created = await client.meetingNotes.create(
        CreateMeetingNotePageParameters(
            parent={"type": "page_id", "page_id": "page_abc123"},
            title="Weekly sync",
            markdown="## Agenda\n- Roadmap review",
            markdown_version="v2",
        )
    )
    print(created.meeting_note.id, created.created)

    existing = await client.meetingNotes.create(
        CreateMeetingNotePageParameters(
            calendar_event={
                "calendar": {
                    "account_id": "account_abc123",
                    "calendar_id": "team@example.com",
                },
                "event_id": "event_abc123",
            }
        )
    )
    print(existing.meeting_note.meeting_notes.is_full_page)
```

### link

Link an existing full-page meeting note to a calendar event. The link replaces any event the note is already linked to.

```python
async def link(
    params: LinkMeetingNotePageParameters,
    *,
    auth: AuthParam | None = None
) -> LinkMeetingNotePageResponse
```

When the event already has other meeting notes, the API returns 409 unless `allow_other_meeting_notes` is `true`. On success, `other_meeting_note_ids` lists the other notes you can read that are linked to the same event.

**Example**:

```python
from notion_py_client import LinkMeetingNotePageParameters, NotionAsyncClient

async with NotionAsyncClient(auth="secret_xxx") as client:
    linked = await client.meetingNotes.link(
        LinkMeetingNotePageParameters(
            meeting_note_id="meeting_note_abc123",
            calendar_event={
                "calendar": {
                    "account_id": "account_abc123",
                    "calendar_id": "team@example.com",
                },
                "event_id": "event_abc123",
            },
            allow_other_meeting_notes=True,
        )
    )
    print(linked.other_meeting_note_ids)
```
