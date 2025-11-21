"""
Notion Markdown Exporter

NotionページをMarkdown形式にエクスポートするツール。
すべての主要なブロックタイプをサポートし、親子関係を適切に反映します。

サポートされるブロックタイプ:
- テキストブロック: 段落、見出し（H1/H2/H3）、引用
- リスト: 箇条書き、番号付き、ToDoリスト（ネスト対応）
- コード: コードブロック、インラインコード
- 数式: ブロック数式、インライン数式
- テーブル: ヘッダー付きテーブル
- メディア: 画像、動画、音声、PDF、ファイル、ブックマーク、埋め込み
- レイアウト: カラム、区切り線、目次
- 特殊: トグル、コールアウト、同期ブロック、子ページ、子データベース

使用方法:
    python export_as_markdown.py --page-id YOUR_PAGE_ID --output output.md

必要な環境変数:
    NOTION_API_TOKEN: NotionインテグレーションのAPIトークン
"""

import argparse
import asyncio
import os

from dotenv import load_dotenv

from notion_py_client import NotionAsyncClient
from notion_py_client.models.rich_text_item import rich_text_to_markdown
from notion_py_client.utils import is_full_block

load_dotenv()  # Load environment variables from .env file

client = NotionAsyncClient(auth=os.environ["NOTION_API_TOKEN"])


async def convert_block_to_markdown(
    block_id: str, indent_level: int = 0, debug: bool = False
) -> str:
    """
    Notionブロックをマークダウンに変換する

    Args:
        block_id: 変換するブロックのID
        indent_level: インデントレベル（ネストされた要素用）
        debug: デバッグモード

    Returns:
        マークダウン形式の文字列
    """
    block = await client.blocks.retrieve(block_id=block_id)

    if not is_full_block(block):
        return ""

    indent = "  " * indent_level  # 2スペースでインデント
    children_markdown = ""

    # 子要素を持つ場合は再帰的に処理
    if block.has_children:
        children = await client.blocks.children.list(block_id=block_id)

        for i, child in enumerate(children.results):
            if is_full_block(child):
                # 子要素のインデントレベルを決定
                child_indent = indent_level + 1
                child_md = await convert_block_to_markdown(
                    child.id, child_indent, debug
                )
                children_markdown += child_md

    # ブロックタイプごとにマークダウンを生成
    result = ""

    # テキストブロック
    if block.type == "paragraph":
        text = rich_text_to_markdown(block.paragraph.rich_text)
        if text or children_markdown:
            result = f"{indent}{text}\n"
            if children_markdown:
                result += children_markdown
            result += "\n" if not children_markdown else ""

    elif block.type == "heading_1":
        text = rich_text_to_markdown(block.heading_1.rich_text)
        # トグル可能な見出しの場合
        if block.heading_1.is_toggleable and children_markdown:
            result = f"{indent}<details>\n{indent}<summary># {text}</summary>\n\n"
            result += children_markdown
            result += f"{indent}</details>\n\n"
        else:
            result = f"{indent}# {text}\n\n"
            if children_markdown:
                result += children_markdown

    elif block.type == "heading_2":
        text = rich_text_to_markdown(block.heading_2.rich_text)
        # トグル可能な見出しの場合
        if block.heading_2.is_toggleable and children_markdown:
            result = f"{indent}<details>\n{indent}<summary>## {text}</summary>\n\n"
            result += children_markdown
            result += f"{indent}</details>\n\n"
        else:
            result = f"{indent}## {text}\n\n"
            if children_markdown:
                result += children_markdown

    elif block.type == "heading_3":
        text = rich_text_to_markdown(block.heading_3.rich_text)
        # トグル可能な見出しの場合
        if block.heading_3.is_toggleable and children_markdown:
            result = f"{indent}<details>\n{indent}<summary>### {text}</summary>\n\n"
            result += children_markdown
            result += f"{indent}</details>\n\n"
        else:
            result = f"{indent}### {text}\n\n"
            if children_markdown:
                result += children_markdown

    # リストブロック
    elif block.type == "bulleted_list_item":
        text = rich_text_to_markdown(block.bulleted_list_item.rich_text)
        result = f"{indent}- {text}\n"
        if children_markdown:
            result += children_markdown

    elif block.type == "numbered_list_item":
        text = rich_text_to_markdown(block.numbered_list_item.rich_text)
        result = f"{indent}1. {text}\n"
        if children_markdown:
            result += children_markdown

    # ToDoブロック
    elif block.type == "to_do":
        checked = "x" if block.to_do.checked else " "
        text = rich_text_to_markdown(block.to_do.rich_text)
        result = f"{indent}- [{checked}] {text}\n"
        if children_markdown:
            result += children_markdown

    # 引用ブロック
    elif block.type == "quote":
        text = rich_text_to_markdown(block.quote.rich_text)
        result = f"{indent}> {text}\n"
        if children_markdown:
            # 引用の中の子要素も引用として扱う
            for line in children_markdown.split("\n"):
                if line:
                    result += f"{indent}> {line}\n"
        result += "\n"

    # トグルブロック
    elif block.type == "toggle":
        text = rich_text_to_markdown(block.toggle.rich_text)
        result = f"{indent}<details>\n{indent}<summary>{text}</summary>\n\n"
        if children_markdown:
            result += children_markdown
        result += f"{indent}</details>\n\n"

    # コールアウトブロック
    elif block.type == "callout":
        text = rich_text_to_markdown(block.callout.rich_text)
        icon = ""
        if block.callout.icon:
            if block.callout.icon.type == "emoji":
                icon = block.callout.icon.emoji + " "
        result = f"{indent}> {icon}{text}\n"
        if children_markdown:
            for line in children_markdown.split("\n"):
                if line:
                    result += f"{indent}> {line}\n"
        result += "\n"

    # コードブロック
    elif block.type == "code":
        text = rich_text_to_markdown(block.code.rich_text)
        lang = block.code.language
        result = f"{indent}```{lang}\n{text}\n{indent}```\n\n"
        if children_markdown:
            result += children_markdown

    # 数式ブロック
    elif block.type == "equation":
        result = f"{indent}$$\n{block.equation.expression}\n{indent}$$\n\n"
        if children_markdown:
            result += children_markdown

    # 区切り線
    elif block.type == "divider":
        result = f"{indent}---\n\n"

    # レイアウトブロック
    elif block.type == "column_list":
        # カラムリストは子要素（カラム）をそのまま表示
        if children_markdown:
            result = children_markdown

    elif block.type == "column":
        # カラムの内容をそのまま表示
        if children_markdown:
            result = children_markdown

    # テーブル
    elif block.type == "table":
        # テーブルは子要素（table_row）で構成される
        if children_markdown:
            lines = children_markdown.strip().split("\n")
            if len(lines) > 0:
                # 最初の行をヘッダーとして扱う
                header = lines[0].strip()
                # カラム数を数える
                col_count = header.count("|") - 1
                separator = indent + "|" + " --- |" * col_count

                # ヘッダー、区切り線、その他の行を結合
                result = indent + header + "\n" + separator + "\n"
                if len(lines) > 1:
                    for line in lines[1:]:
                        if line.strip():
                            result += indent + line.strip() + "\n"
                result += "\n"

    elif block.type == "table_row":
        # テーブル行（インデントなしで出力）
        cells = [rich_text_to_markdown(cell) for cell in block.table_row.cells]
        result = f"| {' | '.join(cells)} |\n"

    # メディアブロック
    elif block.type == "image":
        caption = (
            rich_text_to_markdown(block.image.caption) if block.image.caption else ""
        )
        url = (
            block.image.external.url
            if block.image.type == "external"
            else block.image.file.url
        )
        alt_text = caption if caption else "image"
        result = f"{indent}![{alt_text}]({url})\n\n"
        if children_markdown:
            result += children_markdown

    elif block.type == "video":
        caption = (
            rich_text_to_markdown(block.video.caption) if block.video.caption else ""
        )
        url = (
            block.video.external.url
            if block.video.type == "external"
            else block.video.file.url
        )
        result = f"{indent}[Video: {caption if caption else 'video'}]({url})\n\n"
        if children_markdown:
            result += children_markdown

    elif block.type == "file":
        caption = block.file.name if block.file.name else ""
        url = (
            block.file.external.url
            if block.file.type == "external"
            else block.file.file.url
        )
        result = f"{indent}[File: {caption if caption else 'file'}]({url})\n\n"
        if children_markdown:
            result += children_markdown

    elif block.type == "pdf":
        caption = rich_text_to_markdown(block.pdf.caption) if block.pdf.caption else ""
        url = (
            block.pdf.external.url
            if block.pdf.type == "external"
            else block.pdf.file.url
        )
        result = f"{indent}[PDF: {caption if caption else 'pdf'}]({url})\n\n"
        if children_markdown:
            result += children_markdown

    elif block.type == "audio":
        caption = (
            rich_text_to_markdown(block.audio.caption) if block.audio.caption else ""
        )
        url = (
            block.audio.external.url
            if block.audio.type == "external"
            else block.audio.file.url
        )
        result = f"{indent}[Audio: {caption if caption else 'audio'}]({url})\n\n"
        if children_markdown:
            result += children_markdown

    elif block.type == "bookmark":
        caption = (
            rich_text_to_markdown(block.bookmark.caption)
            if block.bookmark.caption
            else ""
        )
        url = block.bookmark.url
        result = f"{indent}[Bookmark: {caption if caption else url}]({url})\n\n"
        if children_markdown:
            result += children_markdown

    elif block.type == "embed":
        caption = (
            rich_text_to_markdown(block.embed.caption) if block.embed.caption else ""
        )
        url = block.embed.url
        result = f"{indent}[Embed: {caption if caption else url}]({url})\n\n"
        if children_markdown:
            result += children_markdown

    elif block.type == "link_preview":
        url = block.link_preview.url
        result = f"{indent}[Link Preview]({url})\n\n"

    # 特殊ブロック
    elif block.type == "child_page":
        result = f"{indent}[Page: {block.child_page.title}]\n\n"
        if children_markdown:
            result += children_markdown

    elif block.type == "child_database":
        result = f"{indent}[Database: {block.child_database.title}]\n\n"
        if children_markdown:
            result += children_markdown

    elif block.type == "table_of_contents":
        result = f"{indent}[Table of Contents]\n\n"

    elif block.type == "breadcrumb":
        result = f"{indent}[Breadcrumb]\n\n"

    elif block.type == "template":
        text = rich_text_to_markdown(block.template.rich_text)
        result = f"{indent}[Template: {text}]\n\n"
        if children_markdown:
            result += children_markdown

    elif block.type == "synced_block":
        # 同期ブロックの処理
        if block.synced_block.synced_from:
            synced_block_id = block.synced_block.synced_from.block_id
            synced_content = await convert_block_to_markdown(
                synced_block_id, indent_level, debug
            )
            result = synced_content
        else:
            # オリジナルの同期ブロック
            if children_markdown:
                result = children_markdown

    elif block.type == "link_to_page":
        page_info = block.link_to_page
        if page_info.page_id:
            result = f"{indent}[Link to Page](https://notion.so/{page_info.page_id.replace('-', '')})\n\n"
        elif page_info.database_id:
            result = f"{indent}[Link to Database](https://notion.so/{page_info.database_id.replace('-', '')})\n\n"

    # 未サポートのブロック
    elif block.type == "unsupported":
        result = f"{indent}[Unsupported Block]\n\n"

    else:
        # その他の未知のブロックタイプ
        result = f"{indent}[Unknown Block Type: {block.type}]\n\n"
        if children_markdown:
            result += children_markdown

    return result


async def export_page_as_markdown(
    page_id: str, output_file: str = None, debug: bool = False
) -> str:
    """
    Notionページ全体をマークダウンにエクスポートする

    Args:
        page_id: エクスポートするページのID
        output_file: 出力ファイルパス（オプション）
        debug: デバッグモード

    Returns:
        マークダウン形式の文字列
    """
    # ページ情報を取得
    page = await client.pages.retrieve({"page_id": page_id})

    # ページタイトルを取得
    for property in page.properties.values():
        if property.type == "title":
            title = rich_text_to_markdown(property.title)
            break
    else:
        title = ""
    markdown = f"# {title}\n\n"

    # ページの子ブロックを取得
    children = await client.blocks.children.list(block_id=page_id)

    for child in children.results:
        if is_full_block(child):
            child_markdown = await convert_block_to_markdown(
                child.id, indent_level=0, debug=debug
            )
            markdown += child_markdown

    # ファイルに出力
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown)
        print(f"マークダウンファイルを出力しました: {output_file}")

    return markdown


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--page-id", type=str, required=True)
    parser.add_argument("--output", type=str, required=False, default="output.md")
    parser.add_argument("--debug", action="store_true", default=False)
    args = parser.parse_args()
    asyncio.run(export_page_as_markdown(args.page_id, args.output, args.debug))
