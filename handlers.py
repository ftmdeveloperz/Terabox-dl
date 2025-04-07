import os
import aiohttp
import asyncio
import time
import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Logger setup
logger = logging.getLogger("Fᴛᴍ Dᴇᴠᴇʟᴏᴘᴇʀᴢ")

# ProgressBar class to manage download/upload progress
class ProgressBar:
    def __init__(self, message: Message):
        self.message = message
        self.total = 0
        self.current = 0

    # Update progress bar during download/upload
    async def update_progress(self, current: int, total: int, status: str, message: Message):
        self.current = current
        self.total = total
        percent = (current / total) * 100
        progress = '■' * int(percent / 5) + '□' * (20 - int(percent / 5))
        await message.edit(f"{status}\n{progress} {percent:.2f}%")

    # For uploading progress bar
    async def upload_progress(self, current: int, total: int):
        percent = (current / total) * 100
        progress = '■' * int(percent / 5) + '□' * (20 - int(percent / 5))
        return f"{progress} {percent:.2f}%"

# Function to cancel task
async def cancel_task(user_id: int, message: Message):
    # Add task cancellation logic here, e.g., cancel a download task
    await message.edit(f"Task for user {user_id} has been canceled.")
    # Implement any additional logic to stop ongoing tasks
    return f"Task for user {user_id} has been canceled."

# Fetch direct download link from Terabox
async def fetch_direct_link(terabox_url: str) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{TERABOX_API}{terabox_url}") as resp:
                data = await resp.json()
                return data.get("downloadUrl")
    except Exception as e:
        logger.error(f"[Fetch Error] {e}")
        return None

# Function to download file with progress
async def download_file(url: str, filename: str, progress: ProgressBar, message: Message, task_id: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                total = int(response.headers.get('Content-Length', 0))
                downloaded = 0
                start_time = time.time()

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
                        # Check if task is canceled
                        if await is_task_cancelled(task_id):
                            await cancel_task(task_id, message)
                            break
        return filename
    except Exception as e:
        logger.error(f"[Download Error] {e}")
        return None

# Function to check if a task is canceled
async def is_task_cancelled(task_id: str) -> bool:
    # Logic to check if a task is canceled based on the task_id
    # This could involve checking a database, cache, or in-memory task state.
    return False  # Placeholder for actual task cancellation check

# Upload the file to Telegram
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

# Command Handlers

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message: Message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⚙️ Hᴇʟᴘ", callback_data="help")],
        [InlineKeyboardButton("🔗 Sᴇɴᴅ Lɪɴᴋ", switch_inline_query_current_chat="")],
        [InlineKeyboardButton("🛠️ Sᴏᴜʀᴄᴇ / Rᴇᴘᴏ", callback_data="repo")],
        [InlineKeyboardButton("👑 Dᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/ftmdeveloperz")]
    ])
    await message.reply_text(START_TEXT.format(message.from_user.first_name), reply_markup=keyboard, disable_web_page_preview=True)

@Client.on_callback_query(filters.regex("help"))
async def help_cb(_, query):
    await query.message.edit(
        "🔧 Hᴏᴡ Tᴏ Usᴇ TᴇʀᴀBᴏx Bᴏᴛ:\n\n"
        "1. Sᴇɴᴅ ᴀɴʏ Tᴇʀᴀʙᴏx Lɪɴᴋ\n"
        "2. Wᴀɪᴛ ғᴏʀ ᴅᴏᴡɴʟᴏᴀᴅ & ᴜᴘʟᴏᴀᴅ\n"
        "3. Rᴇᴄᴇɪᴠᴇ ғɪʟᴇ ᴅɪʀᴇᴄᴛʟʏ ɪɴ ᴛɪɴʏ ᴘᴀᴄᴋᴀɢᴇ", 
        reply_markup=InlineKeyboardMarkup([ 
            [InlineKeyboardButton("↩️ Bᴀᴄᴋ", callback_data="start")]
        ])
    )

@Client.on_callback_query(filters.regex("repo"))
async def repo_cb(_, query):
    await query.message.edit(REPO_TEXT, reply_markup=InlineKeyboardMarkup([ 
        [InlineKeyboardButton("↩️ Bᴀᴄᴋ", callback_data="start")]
    ]))

@Client.on_message(filters.command("queue"))
async def queue_cb(_, message: Message):
    # Show queue status
    await message.reply_text("Queue is empty. No tasks currently in progress.")

# Additional handlers as required
