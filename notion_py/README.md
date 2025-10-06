# Notion Parser

Notion の JSON レスポンスを型安全な Python クラスとして管理するためのライブラリです。

## 概要

このライブラリは、Notion の API から取得した JSON データを、Pydantic ベースの型安全な Python クラスに変換するために作成されました。TypeScript の公式 Notion API 型定義を参考に、各 Notion オブジェクトとプロパティタイプに対応したクラスを提供し、データの検証と型安全性を確保します。

## 主な特徴

- ✅ **完全な型安全性**: Pydantic v2 による厳密な型検証
- ✅ **TypeScript 定義準拠**: Notion 公式 TypeScript 型定義に基づく実装
- ✅ **DRY 原則**: 重複コードを排除し、役割ごとにファイル分割
- ✅ **Enum + Literal パターン**: 基底クラスで Enum、サブクラスで Literal オーバーライド
- ✅ **包括的なカバレッジ**: Database、DataSource、Page、Block (33 種類) をサポート
- ✅ **リポジトリパターン**: ドメインモデル中心の型安全な CRUD 操作
- ✅ **Request 型システム**: ページ作成・更新用の完全な型定義 (14 種類のプロパティリクエスト)

````

### AbstractNotionRepository の使用

`AbstractNotionRepository` は、ドメインモデルとNotion APIの間の型安全なブリッジを提供する抽象基底クラスです。

#### 基本的な使い方

```python
from typing import TypedDict
from src.core.adapter.notion.parser.abstract_repository import AbstractNotionRepository
from src.core.adapter.notion.parser.requests.property_requests import PropertyRequest, TitlePropertyRequest, StatusPropertyRequest
from src.core.adapter.notion.parser import NotionPage

# 1. ドメインモデルを定義
class Task(TypedDict):
    id: str
    title: str
    status: str
    created_time: str

# 2. リポジトリクラスを実装
class TaskRepository(AbstractNotionRepository[Task, NotionPage]):
    def __init__(self, client, database_id: str):
        super().__init__(client, database_id)

    def _page_to_domain_model(self, page: NotionPage) -> Task:
        """NotionページをTaskドメインモデルに変換"""
        return Task(
            id=page.id,
            title=page.properties["タスク名"].title[0].plain_text if page.properties["タスク名"].title else "",
            status=page.properties["ステータス"].status.name if page.properties["ステータス"].status else "未着手",
            created_time=page.created_time,
        )

    def _domain_to_property_requests(self, domain_model: Task) -> dict[str, PropertyRequest]:
        """Taskドメインモデルをプロパティリクエストに変換"""
        return {
            "タスク名": TitlePropertyRequest(
                title=[{"type": "text", "text": {"content": domain_model["title"]}}]
            ),
            "ステータス": StatusPropertyRequest(
                status={"name": domain_model["status"]}
            ),
        }

# 3. リポジトリを使用
task_repo = TaskRepository(client, database_id="your-database-id")

# ページを取得してドメインモデルに変換
task = await task_repo.get_page("page-id")
print(f"Task: {task['title']} - {task['status']}")

# ドメインモデルから新規ページを作成
new_task = Task(
    id="",  # 作成時は空
    title="新しいタスク",
    status="進行中",
    created_time="",  # 作成時は空
)
created_task = await task_repo.create(new_task)

# ドメインモデルでページを更新
task["status"] = "完了"
updated_task = await task_repo.update(task["id"], task)

# データベース全体をクエリ
all_tasks = await task_repo.query_database()
for task in all_tasks:
    print(f"{task['title']}: {task['status']}")
````

#### 主要なメソッド

- **`get_page(page_id: str) -> TDomainModel`**: ページを取得してドメインモデルに変換
- **`query_database(**kwargs) -> list[TDomainModel]`\*\*: データベースをクエリしてドメインモデルのリストを返す
- **`create(domain_model: TDomainModel, parent=None) -> TDomainModel`**: ドメインモデルから新規ページを作成
- **`update(page_id: str, domain_model: TDomainModel) -> TDomainModel`**: ドメインモデルでページを更新
- **`update_properties(page_id: str, properties: dict) -> TDomainModel`**: 低レベル API（通常は`update()`を使用）

#### 実装する必要がある抽象メソッド

リポジトリクラスでは、以下の 2 つの抽象メソッドを実装する必要があります：

1. **`_page_to_domain_model(page: NotionPage) -> TDomainModel`**

   - Notion ページをドメインモデルに変換（読み取り用）
   - プロパティの取得と型変換のロジックを実装

2. **`_domain_to_property_requests(domain_model: TDomainModel) -> dict[str, PropertyRequest]`**
   - ドメインモデルをプロパティリクエストに変換（書き込み用）
   - 作成・更新時に使用されるリクエストペイロードを生成

#### 利点

- ✅ **型安全性**: ドメインモデルと Notion API の間で完全な型チェック
- ✅ **一貫性**: 読み取り・作成・更新すべてでドメインモデルを使用
- ✅ **DRY 原則**: 変換ロジックを 1 箇所に集約
- ✅ **テスタビリティ**: ドメインロジックと API 呼び出しを分離

詳細な実装例とベストプラクティスについては、[Abstract Repository Guide](docs/abstract-repository-guide.md) を参照してください。

## アーキテクチャ- ✅ **DRY 原則**: 重複コードを排除し、役割ごとにファイル分割

- ✅ **Enum + Literal パターン**: 基底クラスで Enum、サブクラスで Literal オーバーライド
- ✅ **包括的なカバレッジ**: Database、DataSource、Page、Block (33 種類) をサポート

## ディレクトリ構造

```
parser/
├── __init__.py                    # メインエクスポート
├── README.md                      # このファイル
├── abstract_repository.py         # AbstractNotionRepositoryクラス
├── database.py                    # NotionDatabaseクラス
├── datasource.py                  # DataSourceクラス
├── page.py                        # NotionPageクラス
├── block.py                       # ブロックの再エクスポート
├── docs/                          # ドキュメントディレクトリ
│   ├── abstract-repository-guide.md      # リポジトリパターン実装ガイド
│   ├── abstract-repository-changes.md    # リポジトリパターン変更履歴
│   └── openapi-issues.md                 # OpenAPI生成コードの問題点
├── blocks/                        # ブロック実装ディレクトリ
│   ├── __init__.py               # 全ブロックのエクスポート
│   ├── base.py                   # BaseBlockObject, BlockType, ApiColor
│   ├── text_blocks.py            # テキスト系ブロック (10種類)
│   ├── special_blocks.py         # 特殊ブロック (6種類)
│   ├── layout_blocks.py          # レイアウト系ブロック (8種類)
│   ├── media_blocks.py           # メディア系ブロック (8種類)
│   └── unsupported.py            # サポート外ブロック (1種類)
├── models/                        # 基本モデルディレクトリ
│   ├── __init__.py               # モデルのエクスポート
│   ├── icon.py                   # NotionIcon, IconType
│   ├── cover.py                  # NotionCover, CoverType
│   ├── parent.py                 # NotionParent, ParentType
│   ├── date_info.py              # 日付情報
│   ├── file.py                   # ファイル関連モデル
│   ├── formula.py                # フォーミュラ結果
│   ├── rich_text_item.py         # RichText要素
│   ├── select_option.py          # セレクトオプション
│   ├── status_option.py          # ステータスオプション
│   ├── unique_id.py              # ユニークID
│   ├── user.py                   # ユーザー情報
│   ├── verification.py           # 検証情報
│   └── primitives/               # プリミティブ型
│       ├── __init__.py           # プリミティブのエクスポート
│       ├── annotation.py         # テキストアノテーション
│       └── text_item.py          # テキスト情報
├── properties/                    # プロパティディレクトリ
│   ├── __init__.py               # プロパティのエクスポート
│   ├── relation_property.py      # relationプロパティ
│   ├── rollup_property.py        # rollupプロパティ
│   └── base_properties/          # 基本プロパティディレクトリ
│       ├── __init__.py           # 基本プロパティのエクスポート
│       ├── _base_property.py     # ベースプロパティクラス
│       ├── button_property.py    # buttonプロパティ
│       ├── checkbox_property.py  # checkboxプロパティ
│       ├── created_by_property.py # created_byプロパティ
│       ├── created_time_property.py # created_timeプロパティ
│       ├── date_property.py      # dateプロパティ
│       ├── email_property.py     # emailプロパティ
│       ├── files_property.py     # filesプロパティ
│       ├── formula_property.py   # formulaプロパティ
│       ├── last_edited_by_property.py # last_edited_byプロパティ
│       ├── last_edited_time_property.py # last_edited_timeプロパティ
│       ├── multi_select_property.py # multi_selectプロパティ
│       ├── number_property.py    # numberプロパティ
│       ├── people_property.py    # peopleプロパティ
│       ├── phone_number_property.py # phone_numberプロパティ
│       ├── rich_text_property.py # rich_textプロパティ
│       ├── select_property.py    # selectプロパティ
│       ├── status_property.py    # statusプロパティ
│       ├── title_property.py     # titleプロパティ
│       ├── unique_id_property.py # unique_idプロパティ
│       ├── url_property.py       # urlプロパティ
│       └── verification_property.py # verificationプロパティ
├── requests/                      # リクエスト型ディレクトリ
│   ├── __init__.py               # リクエスト型のエクスポート
│   ├── common.py                 # 共通リクエスト型
│   ├── property_requests.py      # プロパティリクエスト型 (14種類)
│   └── page_requests.py          # ページ作成・更新リクエスト型
└── schema/                        # スキーマディレクトリ
    ├── __init__.py               # スキーマのエクスポート
    └── property_configs.py       # データベースプロパティ設定
```

## サポートされるオブジェクトタイプ

### メインオブジェクト

- **NotionDatabase**: データベースオブジェクト (`databases.retrieve` API レスポンス)
- **DataSource**: データソースオブジェクト (`databases.query` API レスポンス)
- **NotionPage**: ページオブジェクト (`pages.retrieve` API レスポンス)
- **BlockObject**: ブロックオブジェクト (`blocks.retrieve` API レスポンス)

### ブロックタイプ (33 種類)

#### テキスト系ブロック (10 種類)

- **ParagraphBlock**: 段落
- **Heading1Block, Heading2Block, Heading3Block**: 見出し 1/2/3
- **BulletedListItemBlock**: 箇条書きリスト
- **NumberedListItemBlock**: 番号付きリスト
- **QuoteBlock**: 引用
- **ToDoBlock**: ToDo
- **ToggleBlock**: トグル
- **TemplateBlock**: テンプレート

#### 特殊ブロック (6 種類)

- **SyncedBlockBlock**: 同期ブロック
- **ChildPageBlock**: 子ページ
- **ChildDatabaseBlock**: 子データベース
- **EquationBlock**: 数式
- **CodeBlock**: コード (90+言語対応)
- **CalloutBlock**: コールアウト

#### レイアウト系ブロック (8 種類)

- **DividerBlock**: 区切り線
- **BreadcrumbBlock**: パンくずリスト
- **TableOfContentsBlock**: 目次
- **ColumnListBlock**: カラムリスト
- **ColumnBlock**: カラム
- **LinkToPageBlock**: ページへのリンク
- **TableBlock**: テーブル
- **TableRowBlock**: テーブル行

#### メディア系ブロック (8 種類)

- **EmbedBlock**: 埋め込み
- **BookmarkBlock**: ブックマーク
- **ImageBlock**: 画像
- **VideoBlock**: 動画
- **PdfBlock**: PDF
- **FileBlock**: ファイル
- **AudioBlock**: 音声
- **LinkPreviewBlock**: リンクプレビュー

#### その他

- **UnsupportedBlock**: サポート外ブロック

## サポートされるプロパティタイプ (23 種類)

### 基本プロパティ (23 種類)

- **title**: ページのタイトル
- **rich_text**: リッチテキスト
- **number**: 数値
- **select**: 単一選択
- **multi_select**: 複数選択
- **status**: ステータス
- **date**: 日付
- **checkbox**: チェックボックス
- **url**: URL
- **email**: メールアドレス
- **phone_number**: 電話番号
- **people**: ユーザー選択
- **files**: ファイル
- **created_by**: 作成者
- **created_time**: 作成日時
- **last_edited_by**: 最終編集者
- **last_edited_time**: 最終編集日時
- **formula**: 計算式
- **relation**: リレーション
- **rollup**: ロールアップ
- **unique_id**: ユニーク ID
- **verification**: 検証
- **button**: ボタン

## 使用方法

### データベースの取得と解析

```python
from notion_client import AsyncClient
from src.core.adapter.notion.parser import NotionDatabase

# Notion APIクライアントの初期化
client = AsyncClient(auth="secret_...")

# データベース取得
database_id = "your-database-id"
response = await client.databases.retrieve(database_id=database_id)

# 型安全にパース
database = NotionDatabase(**response)

# メタデータにアクセス
print(f"Database Title: {database.title[0].plain_text}")
print(f"Created: {database.created_time}")
print(f"URL: {database.url}")

# プロパティ設定にアクセス
for prop_name, prop_config in database.properties.items():
    print(f"{prop_name}: {prop_config.type}")
```

### データソースのクエリ

```python
from src.core.adapter.notion.parser import DataSource

# データベースをクエリ
query_response = await client.databases.query(database_id=database_id)

# 各ページを型安全にパース
for page_data in query_response["results"]:
    page = DataSource(**page_data)

    # プロパティに型安全にアクセス
    if "Title" in page.properties:
        title_prop = page.properties["Title"]
        print(f"Title: {title_prop.get_value()}")

    if "Status" in page.properties:
        status_prop = page.properties["Status"]
        print(f"Status: {status_prop.get_value()}")
```

### ページの取得と操作

```python
from src.core.adapter.notion.parser import NotionPage

# ページ取得
page_id = "your-page-id"
response = await client.pages.retrieve(page_id=page_id)

# 型安全にパース
page = NotionPage(**response)

# メタデータとプロパティにアクセス
print(f"Page ID: {page.id}")
print(f"Created: {page.created_time}")
print(f"Icon: {page.icon}")
print(f"Cover: {page.cover}")

# プロパティを処理
for prop_name, prop_value in page.properties.items():
    value = prop_value.get_value() if hasattr(prop_value, 'get_value') else None
    print(f"{prop_name}: {value}")
```

### ブロックの取得と解析

```python
from src.core.adapter.notion.parser import (
    BlockObject,
    ParagraphBlock,
    Heading1Block,
    CodeBlock,
    ImageBlock,
)

# ブロック取得
block_id = "your-block-id"
response = await client.blocks.retrieve(block_id=block_id)

# 型安全にパース
block = BlockObject(**response)  # 自動的に適切なブロックタイプに変換

# ブロックタイプごとに処理
match block:
    case ParagraphBlock():
        print(f"Paragraph: {block.paragraph.rich_text[0].plain_text}")
    case Heading1Block():
        print(f"Heading 1: {block.heading_1.rich_text[0].plain_text}")
    case CodeBlock():
        print(f"Code ({block.code.language}): {block.code.rich_text[0].plain_text}")
    case ImageBlock():
        if block.image.type == "external":
            print(f"Image URL: {block.image.external.url}")
        else:
            print(f"Image File: {block.image.file.url}")
    case _:
        print(f"Other block type: {block.type}")
```

### 子ブロックの一覧取得

```python
from src.core.adapter.notion.parser.block import BlockObject

# 子ブロック一覧取得
block_id = "parent-block-id"
response = await client.blocks.children.list(block_id=block_id)

# 各ブロックを型安全に処理
for block_data in response["results"]:
    block = BlockObject(**block_data)

    # 共通フィールドにアクセス
    print(f"Block ID: {block.id}")
    print(f"Type: {block.type}")
    print(f"Has Children: {block.has_children}")
    print(f"Created: {block.created_time}")
```

### 個別プロパティの使用例

```python
from src.core.adapter.notion.parser.properties.base_properties import (
    TitleProperty,
    RichTextProperty,
    NumberProperty,
    SelectProperty,
    StatusProperty,
    DateProperty,
)
```

# title プロパティの作成と使用

title_data = {
"id": "title",
"type": "title",
"title": [
{
"type": "text",
"text": {
"content": "サンプルタイトル",
"link": None
},
"annotations": {
"bold": False,
"italic": False,
"strikethrough": False,
"underline": False,
"code": False,
"color": "default"
},
"plain_text": "サンプルタイトル",
"href": None
}
]
}

title_property = TitleProperty(\*\*title_data)
print(title_property.get_value()) # "サンプルタイトル"

# Status プロパティ

status_property = StatusProperty(\*\*status_data)
status_value = status_property.get_value()
print(f"Status: {status_value}") # "In Progress" など

# Date プロパティ

date_property = DateProperty(\*\*date_data)
date_value = date_property.get_value()
if date_value:
print(f"Date: {date_value.start} - {date_value.end}")

```

## アーキテクチャ

### 設計原則

1. **DRY (Don't Repeat Yourself)**: 重複コードを排除し、共通モデルを再利用
2. **単一責任の原則**: 各ファイルは明確な役割を持つ
3. **型安全性**: Pydantic v2による厳密な型検証
4. **Enum + Literal パターン**: 基底クラスでEnum、サブクラスでLiteralオーバーライド

### 共通モデルの分離

Icon、Cover、Parentなどの共通モデルは`models/`ディレクトリに分離:

- `models/icon.py`: NotionIcon, IconType (emoji/external/file)
- `models/cover.py`: NotionCover, CoverType (external/file)
- `models/parent.py`: NotionParent, ParentType (page_id/workspace/block_id/database_id/data_source_id)

これらは`NotionDatabase`, `DataSource`, `NotionPage`, `BlockObject`で共有されます。

### ブロックの階層構造

```

BaseBlockObject (基底クラス)
├── object: Literal["block"]
├── id: str
├── type: BlockType (Enum)
├── created_time: str
├── created_by: PartialUser
├── last_edited_time: str
├── last_edited_by: PartialUser
├── parent: NotionParent
├── has_children: bool
├── archived: bool
└── in_trash: bool

各ブロックタイプが BaseBlockObject を継承:
├── ParagraphBlock
│ └── type: Literal[BlockType.PARAGRAPH]
│ └── paragraph: ContentWithRichTextAndColor
├── CodeBlock
│ └── type: Literal[BlockType.CODE]
│ └── code: CodeContent
└── ...

````

## 型の特徴

### 型安全性

- すべてのクラスは Pydantic の BaseModel を継承
- 厳密な型チェック（StrictStr、StrictInt 等を使用）
- 自動的なデータ検証
- Discriminated Union による型の自動判別

### Enum + Literal パターン

```python
class BlockType(str, Enum):
    PARAGRAPH = "paragraph"
    CODE = "code"
    # ...

class BaseBlockObject(BaseModel):
    type: BlockType  # Enum型

class ParagraphBlock(BaseBlockObject):
    type: Literal[BlockType.PARAGRAPH]  # Literalでオーバーライド
    paragraph: ContentWithRichTextAndColor

class CodeBlock(BaseBlockObject):
    type: Literal[BlockType.CODE]  # Literalでオーバーライド
    code: CodeContent
````

このパターンにより:

- IDE の補完サポート
- 型チェッカーによる厳密な検証
- 自動的な Union 型の判別

### 日本語対応

- フィールドの説明は日本語で記述
- 日本語のプロパティ名にも対応
- docstring による詳細な説明

### 拡張性

新しいプロパティタイプやブロックタイプを簡単に追加可能:

- BaseProperty クラスを継承して独自プロパティを作成
- BaseBlockObject クラスを継承して独自ブロックを作成

## 開発者向け

### 新しいブロックタイプの追加

1. 適切な`blocks/`配下のファイルにクラスを追加（または新規ファイル作成）
2. `BaseBlockObject`を継承したクラスを定義
3. `type`フィールドを`Literal[BlockType.XXX]`でオーバーライド
4. ブロック固有のコンテンツモデルを定義
5. `blocks/__init__.py`にエクスポートを追加

例:

```python
# blocks/custom_blocks.py
from typing import Literal
from pydantic import Field, BaseModel
from .base import BaseBlockObject, BlockType
from ..models.rich_text_item import RichTextItem

class CustomContent(BaseModel):
    """カスタムコンテンツ"""

    text: list[RichTextItem] = Field(..., description="テキスト")
    custom_field: str = Field(..., description="カスタムフィールド")

class CustomBlock(BaseBlockObject):
    """カスタムブロック"""

    type: Literal[BlockType.CUSTOM] = Field(BlockType.CUSTOM, description="ブロックタイプ")
    custom: CustomContent = Field(..., description="カスタムコンテンツ")
```

### 新しいプロパティタイプの追加

1. `properties/base_properties/`ディレクトリに新しいファイルを作成
2. `BaseProperty`を継承したクラスを定義
3. `type`フィールドを`Literal["property_type"]`で定義
4. `get_value()`メソッドを実装
5. `properties/base_properties/__init__.py`にエクスポートを追加
6. `datasource.py`の`PropertyType`Union に追加

例:

```python
# properties/base_properties/custom_property.py
from typing import Literal
from pydantic import Field
from ._base_property import BaseProperty

class CustomProperty(BaseProperty):
    """カスタムプロパティ"""

    type: Literal["custom"] = Field("custom", description="プロパティタイプ")
    custom: str = Field(..., description="カスタム値")

    def get_value(self) -> str:
        """カスタムプロパティの値を取得"""
        return self.custom
```

### 新しい共通モデルの追加

共通で使用されるモデルは`models/`ディレクトリに配置:

1. `models/`ディレクトリに新しいファイルを作成
2. Pydantic の`BaseModel`を継承したクラスを定義
3. 必要に応じて Enum も定義
4. `models/__init__.py`にエクスポートを追加

例:

```python
# models/custom_model.py
from enum import Enum
from pydantic import BaseModel, Field, StrictStr

class CustomType(str, Enum):
    """カスタムタイプ"""

    TYPE_A = "type_a"
    TYPE_B = "type_b"

class CustomModel(BaseModel):
    """カスタム共通モデル"""

    type: CustomType = Field(..., description="タイプ")
    name: StrictStr = Field(..., description="名前")
    value: StrictStr = Field(..., description="値")
```

### コーディング規約

- **Python 3.9 以降**の文法を使用
- **typing モジュールは最小限**に抑制
  - `List` → `list`
  - `Dict` → `dict`
  - `Optional[T]` → `T | None`
  - `Union[A, B]` → `A | B`
- **Pydantic Field**を使用してフィールドを定義
- **日本語**でのドキュメント記述
- **Enum + Literal パターン**
  - 基底クラス: `type: EnumType`
  - サブクラス: `type: Literal[EnumType.SPECIFIC_VALUE]`
- **DRY 原則**: 重複コードは共通モジュールに抽出
- **単一責任**: 1 ファイル 1 役割を基本とする

### ファイル命名規則

- **モデルファイル**: `{model_name}.py` (例: `icon.py`, `cover.py`)
- **プロパティファイル**: `{property_type}_property.py` (例: `title_property.py`)
- **ブロックファイル**: `{category}_blocks.py` (例: `text_blocks.py`, `media_blocks.py`)

### Import 規約

- 基本的にファイルのトップレベルで import
- やむを得ない場合（循環 import 回避など）のみ関数内 import
- 不要な import は削除してメンテナンス性を向上

### テスト

テストファイルは`test/test_notion_parser.py`に配置されています。以下のテストが含まれています：

- 各プロパティタイプの個別テスト
- Database、DataSource、Page、Block オブジェクトのパーステスト
- エラーハンドリングテスト
- 複数アイテムを持つプロパティのテスト
- ブロックタイプの判別テスト

テストの実行:

```bash
# 全テスト実行
uv run pytest test/test_notion_parser.py -v

# 特定のテストのみ実行
uv run pytest test/test_notion_parser.py::test_paragraph_block -v

# カバレッジ付きで実行
uv run pytest test/test_notion_parser.py --cov=src/core/adapter/notion/parser
```

## パフォーマンス考慮事項

- **大きなレスポンスの処理**: メモリ使用量に注意
- **バッチ処理**: 大量のページやブロックを処理する際は非同期処理を活用
- **キャッシング**: 頻繁にアクセスするデータベース設定などはキャッシュを検討

## トラブルシューティング

### よくある問題

1. **型エラー (Pydantic ValidationError)**

   - Notion API のレスポンス構造が期待と異なる
   - 解決策: レスポンスデータを確認し、モデル定義を更新

2. **Import エラー**

   - モジュールのパスが正しいか確認
   - `__init__.py`でのエクスポートを確認

3. **Union 型の判別失敗**
   - `type`フィールドが正しく設定されているか確認
   - Discriminated Union のタグ（`type`）が一意であることを確認

## 注意事項

- Notion の API レスポンス構造の変更に注意してください
- 型チェックが厳密なため、データの形式が正確である必要があります
- Pydantic の discriminated union を使用しているため、各クラスで`type`フィールドを`Literal`型で定義する必要があります
- ブロックの`has_children`が`True`の場合、子ブロックは別途`blocks.children.list` API で取得する必要があります
- データベースのプロパティ設定とデータソース/ページのプロパティ値は異なるモデルです

## 参考資料

- [Notion API 公式ドキュメント](https://developers.notion.com/)
- [Notion API TypeScript 型定義](https://github.com/makenotion/notion-sdk-js)
- [Pydantic v2 ドキュメント](https://docs.pydantic.dev/)

## 変更履歴

### v2.1.0 (2025-10-05)

- ✨ AbstractNotionRepository クラスの追加
  - ドメインモデル中心のリポジトリパターン実装
  - 双方向変換（Notion ⇄ Domain）をサポート
  - 型安全な CRUD 操作（create, update, query）
- ✨ Request タイプシステムの追加（14 種類のプロパティリクエスト）
  - PropertyRequest union 型
  - CreatePageParameters, UpdatePageParameters
- 📝 詳細なドキュメント追加
  - abstract-repository-guide.md（実装ガイド）
  - abstract-repository-changes.md（変更履歴）
  - openapi-issues.md（OpenAPI 問題点）

### v2.0.0 (2025-10-05)

- ✨ Database、DataSource、Page、Block (33 種類) の完全実装
- ✨ 共通モデルの分離 (Icon, Cover, Parent)
- ✨ ブロックを役割ごとにファイル分割
- ✨ Enum + Literal パターンの採用
- ✨ 23 種類のプロパティタイプをサポート
- 🔧 DRY 原則に基づくリファクタリング
- 📝 TypeScript 公式型定義に準拠

### v1.0.0

- 🎉 初期リリース
- ✨ 基本的なプロパティタイプのサポート
- ✨ NotionPage クラスの実装

## ライセンス

このプロジェクトのライセンスに従います。
