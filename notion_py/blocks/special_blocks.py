"""
特殊ブロックの定義

SyncedBlock, ChildPage, ChildDatabase, Equation, Code, Callout
"""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, StrictStr

from .base import ApiColor, BaseBlockObject, BlockType
from ..models.rich_text_item import RichTextItem
from ..models.icon import NotionIcon


class CodeLanguage(str, Enum):
    """コードブロックの言語"""

    ABAP = "abap"
    ABC = "abc"
    AGDA = "agda"
    ARDUINO = "arduino"
    ASCII_ART = "ascii art"
    ASSEMBLY = "assembly"
    BASH = "bash"
    BASIC = "basic"
    BNF = "bnf"
    C = "c"
    C_SHARP = "c#"
    C_PLUS_PLUS = "c++"
    CLOJURE = "clojure"
    COFFEESCRIPT = "coffeescript"
    COQ = "coq"
    CSS = "css"
    DART = "dart"
    DHALL = "dhall"
    DIFF = "diff"
    DOCKER = "docker"
    EBNF = "ebnf"
    ELIXIR = "elixir"
    ELM = "elm"
    ERLANG = "erlang"
    F_SHARP = "f#"
    FLOW = "flow"
    FORTRAN = "fortran"
    GHERKIN = "gherkin"
    GLSL = "glsl"
    GO = "go"
    GRAPHQL = "graphql"
    GROOVY = "groovy"
    HASKELL = "haskell"
    HCL = "hcl"
    HTML = "html"
    IDRIS = "idris"
    JAVA = "java"
    JAVASCRIPT = "javascript"
    JSON = "json"
    JULIA = "julia"
    KOTLIN = "kotlin"
    LATEX = "latex"
    LESS = "less"
    LISP = "lisp"
    LIVESCRIPT = "livescript"
    LLVM_IR = "llvm ir"
    LUA = "lua"
    MAKEFILE = "makefile"
    MARKDOWN = "markdown"
    MARKUP = "markup"
    MATLAB = "matlab"
    MATHEMATICA = "mathematica"
    MERMAID = "mermaid"
    NIX = "nix"
    NOTION_FORMULA = "notion formula"
    OBJECTIVE_C = "objective-c"
    OCAML = "ocaml"
    PASCAL = "pascal"
    PERL = "perl"
    PHP = "php"
    PLAIN_TEXT = "plain text"
    POWERSHELL = "powershell"
    PROLOG = "prolog"
    PROTOBUF = "protobuf"
    PURESCRIPT = "purescript"
    PYTHON = "python"
    R = "r"
    RACKET = "racket"
    REASON = "reason"
    RUBY = "ruby"
    RUST = "rust"
    SASS = "sass"
    SCALA = "scala"
    SCHEME = "scheme"
    SCSS = "scss"
    SHELL = "shell"
    SMALLTALK = "smalltalk"
    SOLIDITY = "solidity"
    SQL = "sql"
    SWIFT = "swift"
    TOML = "toml"
    TYPESCRIPT = "typescript"
    VB_NET = "vb.net"
    VERILOG = "verilog"
    VHDL = "vhdl"
    VISUAL_BASIC = "visual basic"
    WEBASSEMBLY = "webassembly"
    XML = "xml"
    YAML = "yaml"
    JAVA_C_CPP_CSHARP = "java/c/c++/c#"


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


# ============================================
# Special Blocks
# ============================================


class SyncedBlockBlock(BaseBlockObject):
    """同期ブロック"""

    type: Literal[BlockType.SYNCED_BLOCK] = Field(
        BlockType.SYNCED_BLOCK, description="ブロックタイプ"
    )
    synced_block: SyncedBlockContent = Field(..., description="同期ブロックコンテンツ")


class ChildPageBlock(BaseBlockObject):
    """子ページブロック"""

    type: Literal[BlockType.CHILD_PAGE] = Field(
        BlockType.CHILD_PAGE, description="ブロックタイプ"
    )
    child_page: TitleObject = Field(..., description="子ページ情報")


class ChildDatabaseBlock(BaseBlockObject):
    """子データベースブロック"""

    type: Literal[BlockType.CHILD_DATABASE] = Field(
        BlockType.CHILD_DATABASE, description="ブロックタイプ"
    )
    child_database: TitleObject = Field(..., description="子データベース情報")


class EquationBlock(BaseBlockObject):
    """数式ブロック"""

    type: Literal[BlockType.EQUATION] = Field(
        BlockType.EQUATION, description="ブロックタイプ"
    )
    equation: ExpressionObject = Field(..., description="数式")


class CodeBlock(BaseBlockObject):
    """コードブロック"""

    type: Literal[BlockType.CODE] = Field(BlockType.CODE, description="ブロックタイプ")
    code: CodeContent = Field(..., description="コードコンテンツ")


class CalloutBlock(BaseBlockObject):
    """コールアウトブロック"""

    type: Literal[BlockType.CALLOUT] = Field(
        BlockType.CALLOUT, description="ブロックタイプ"
    )
    callout: CalloutContent = Field(..., description="コールアウトコンテンツ")
