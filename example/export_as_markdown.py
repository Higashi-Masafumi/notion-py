from notion_py_client import NotionAsyncClient
from notion_py_client.utils import is_full_block
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()  # Load environment variables from .env file

client = NotionAsyncClient(auth=os.environ["NOTION_API_TOKEN"])


async def recursive_get_blocks(block_id: str) -> list:
    """Recursively get all blocks under a given block ID."""
    blocks = []
    children = await client.blocks.children.list(block_id=block_id)
    for block in children.results:
        blocks.append(block)
        if is_full_block(block):
            if block.has_children:
                child_blocks = await recursive_get_blocks(block.id)
                blocks.extend(child_blocks)
    return blocks


async def export_page_as_markdown(page_id: str) -> str:
    """Export a Notion page as Markdown."""
    blocks = await recursive_get_blocks(page_id)
    markdown_content = ""
    for block in blocks:
        if is_full_block(block):
            markdown_content += block.to_markdown() + "\n\n"
    return markdown_content


if __name__ == "__main__":
    page_id = "your_page_id_here"  # Replace with your Notion page ID
    markdown_content = asyncio.run(export_page_as_markdown(page_id))
    print(markdown_content)
