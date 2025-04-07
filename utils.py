import os
import aiohttp
import asyncio
import logging
from pyrogram.types import Message
from progress import ProgressBar
from info import TERABOX_API

# Logger setup
logger = logging.getLogger("Fᴛᴍ Dᴇᴠᴇʟᴏᴘᴇʀᴢ")

async def fetch_direct_link(terabox_url: str) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{TERABOX_API}{terabox_url}") as resp:
                data = await resp.json()
                return data.get("downloadUrl")
    except Exception as e:
        logger.error(f"[Fetch Error] {e}")
        return None

async def download_file(url: str, filename: str, progress: ProgressBar, message: Message):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                total = int(response.headers.get('Content-Length', 0))
                downloaded = 0

                with open(filename, 'wb') as f:
                    async for chunk in response.content.iter_chunked(1024):
                        f.write(chunk)
                        downloaded += len(chunk)
                        await progress.update_progress(
                            current=downloaded,
                            total=total,
                            status="ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ",
                            message=message
                        )
        return filename
    except Exception as e:
        logger.error(f"[Download Error] {e}")
        return None

async def upload_to_telegram(filepath: str, message: Message, progress: ProgressBar):
    try:
        total = os.path.getsize(filepath)
        sent = await message.reply_document(
            document=filepath,
            caption="✔️ ᴜᴘʟᴏᴀᴅᴇᴅ ʙʏ Fᴛᴍ Dᴇᴠᴇʟᴏᴘᴇʀᴢ",
            progress=progress.upload_progress,
        )
        return sent
    except Exception as e:
        logger.error(f"[Upload Error] {e}")
        return None
    finally:
        await asyncio.sleep(3)
        os.remove(filepath)
        logger.info(f"[Auto Deleted] {filepath}")
