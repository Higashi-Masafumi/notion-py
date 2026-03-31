"""
特殊ブロックの定義

SyncedBlock, ChildPage, ChildDatabase, Equation, Code, Callout
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, StrictStr

from .base import ApiColor, BaseBlockObject
from ..models.rich_text_item import RichTextItem
from ..models.icon import NotionIcon


# CodeLanguage as Literal (TypeScript-style)
CodeLanguage = Literal[
    "abap",
    "abc",
    "agda",
    "arduino",
    "ascii art",
    "assembly",
    "bash",
    "basic",
    "bnf",
    "c",
    "c#",
    "c++",
    "clojure",
    "coffeescript",
    "coq",
    "css",
    "dart",
    "dhall",
    "diff",
    "docker",
    "ebnf",
    "elixir",
    "elm",
    "erlang",
    "f#",
    "flow",
    "fortran",
    "gherkin",
    "glsl",
    "go",
    "graphql",
    "groovy",
    "haskell",
    "hcl",
    "html",
    "idris",
    "java",
    "javascript",
    "json",
    "julia",
    "kotlin",
    "latex",
    "less",
    "lisp",
    "livescript",
    "llvm ir",
    "lua",
    "makefile",
    "markdown",
    "markup",
    "matlab",
    "mathematica",
    "mermaid",
    "nix",
    "notion formula",
    "objective-c",
    "ocaml",
    "pascal",
    "perl",
    "php",
    "plain text",
    "powershell",
    "prolog",
    "protobuf",
    "purescript",
    "python",
    "r",
    "racket",
    "reason",
    "ruby",
    "rust",
    "sass",
    "scala",
    "scheme",
    "scss",
    "shell",
    "smalltalk",
    "solidity",
    "sql",
    "swift",
    "toml",
    "typescript",
    "vb.net",
    "verilog",
    "vhdl",
    "visual basic",
    "webassembly",
    "xml",
    "yaml",
    "java/c/c++/c#",
]


# ============================================
# Content Models
# ============================================


class SyncedBlockContent(BaseModel):
    """同期ブロックコンテンツ"""

    synced_from: SyncedFromBlock | None = Field(None, description="同期元ブロック")


class SyncedFromBlock(BaseModel):
    """同期元ブロック情報"""

    type: Literal["block_id"] = Field("block_id", description="タイプ")
    block_id: StrictStr = Field(..., description="ブロックID")


class TitleObject(BaseModel):
    """タイトルオブジェクト"""

    title: StrictStr = Field(..., description="タイトル")


class ExpressionObject(BaseModel):
    """数式オブジェクト"""

    expression: StrictStr = Field(..., description="数式")


class CodeContent(BaseModel):
    """コードコンテンツ"""

    rich_text: list[RichTextItem] = Field(..., description="リッチテキスト配列")
    caption: list[RichTextItem] = Field(..., description="キャプション")
    language: CodeLanguage = Field(..., description="プログラミング言語")


class CalloutContent(BaseModel):
    """コールアウトコンテンツ"""

    rich_text: list[RichTextItem] = Field(..., description="リッチテキスト配列")
    color: ApiColor = Field(..., description="カラー設定")
    icon: NotionIcon | None = Field(None, description="アイコン")


class MeetingNotesChildren(BaseModel):
    """会議メモの関連ブロックID"""

    summary_block_id: StrictStr | None = Field(None, description="要約ブロックID")
    notes_block_id: StrictStr | None = Field(None, description="ノートブロックID")
    transcript_block_id: StrictStr | None = Field(
        None, description="トランスクリプトブロックID"
    )


class MeetingNotesCalendarEvent(BaseModel):
    """会議メモのカレンダー情報"""

    start_time: StrictStr | None = Field(None, description="開始時刻")
    end_time: StrictStr | None = Field(None, description="終了時刻")
    attendees: list[StrictStr] | None = Field(None, description="参加者のユーザーID")


class MeetingNotesRecording(BaseModel):
    """会議メモの録音情報"""

    start_time: StrictStr | None = Field(None, description="録音開始時刻")
    end_time: StrictStr | None = Field(None, description="録音終了時刻")


class MeetingNotesContent(BaseModel):
    """会議メモコンテンツ"""

    title: list[RichTextItem] | None = Field(None, description="会議タイトル")
    status: StrictStr | None = Field(None, description="会議メモの状態")
    children: MeetingNotesChildren | None = Field(None, description="子ブロック参照")
    calendar_event: MeetingNotesCalendarEvent | None = Field(
        None, description="カレンダー情報"
    )
    recording: MeetingNotesRecording | None = Field(None, description="録音情報")


# ============================================
# Special Blocks
# ============================================


class SyncedBlockBlock(BaseBlockObject):
    """同期ブロック"""

    type: Literal["synced_block"] = Field("synced_block", description="ブロックタイプ")
    synced_block: SyncedBlockContent = Field(..., description="同期ブロックコンテンツ")

class ChildPageBlock(BaseBlockObject):
    """子ページブロック"""

    type: Literal["child_page"] = Field("child_page", description="ブロックタイプ")
    child_page: TitleObject = Field(..., description="子ページ情報")

class ChildDatabaseBlock(BaseBlockObject):
    """子データベースブロック"""

    type: Literal["child_database"] = Field(
        "child_database", description="ブロックタイプ"
    )
    child_database: TitleObject = Field(..., description="子データベース情報")

class EquationBlock(BaseBlockObject):
    """数式ブロック"""

    type: Literal["equation"] = Field("equation", description="ブロックタイプ")
    equation: ExpressionObject = Field(..., description="数式")

class CodeBlock(BaseBlockObject):
    """コードブロック"""

    type: Literal["code"] = Field("code", description="ブロックタイプ")
    code: CodeContent = Field(..., description="コードコンテンツ")

class CalloutBlock(BaseBlockObject):
    """コールアウトブロック"""

    type: Literal["callout"] = Field("callout", description="ブロックタイプ")
    callout: CalloutContent = Field(..., description="コールアウトコンテンツ")


class MeetingNotesBlock(BaseBlockObject):
    """会議メモブロック"""

    type: Literal["meeting_notes"] = Field(
        "meeting_notes", description="ブロックタイプ"
    )
    meeting_notes: MeetingNotesContent = Field(..., description="会議メモコンテンツ")


class TranscriptionBlock(BaseBlockObject):
    """旧transcriptionブロック"""

    type: Literal["transcription"] = Field(
        "transcription", description="旧ブロックタイプ"
    )
    transcription: MeetingNotesContent = Field(..., description="会議メモコンテンツ")
