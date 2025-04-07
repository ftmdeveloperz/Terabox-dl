import os
import aiohttp
import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from progress import ProgressBar, cancel_task
from info import START_TEXT, REPO_TEXT, BOT_USERNAME, OWNER_ID, TERABOX_API

# Logger setup
logger = logging.getLogger("Fᴛᴍ Dᴇᴠᴇʟᴏᴘᴇʀᴢ")

# Utility functions

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

# Handlers

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
        reply_markup=InlineKeyboardMarkup([ [InlineKeyboardButton("↩️ Bᴀᴄᴋ", callback_data="start")] ])
    )

@Client.on_callback_query(filters.regex("repo"))
async def repo_cb(_, query):
    await query.message.edit(REPO_TEXT, reply_markup=InlineKeyboardMarkup([ [InlineKeyboardButton("↩️ Bᴀᴄᴋ", callback_data="start")] ]))

@Client.on_message(filters.command("queue"))
async def queue_cmd(_, message: Message):
    queue_text = get_queue(message.from_user.id)
    await message.reply_text(queue_text)

@Client.on_message(filters.command("stats"))
async def stats_cmd(_, message: Message):
    stats_text = get_stats()
    await message.reply_text(stats_text)

@Client.on_message(filters.command("cancel"))
async def cancel_cmd(_, message: Message):
    result = await cancel_task(message.from_user.id)
    await message.reply_text(result)

@Client.on_message(filters.private & filters.text & ~filters.command(["start", "help", "repo", "stats", "queue", "cancel"]))
async def handle_link(client, message: Message):
    if "terabox.com" not in message.text:
        return await message.reply("❌ Sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ ᴛᴇʀᴀʙᴏx ʟɪɴᴋ.")
    
    await handle_task(client, message)
