import os
import time
import logging
import aiohttp
import asyncio
import shutil

from pyrogram import Client
from pyrogram.types import Message
from progress import progress_loop
from info import API_URL, DOWNLOAD_DIR, HEADERS, LOGGER, queue, user_tasks, is_downloading

async def fetch_download_link(terabox_url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}?link={terabox_url}", headers=HEADERS) as resp:
            if resp.status != 200:
                LOGGER.error(f"API request failed: {resp.status}")
                return {"status": False, "error": "API Error"}
            return await resp.json()

async def download_file(url: str, file_name: str, user_id: int, message: Message) -> str:
    path = os.path.join(DOWNLOAD_DIR, file_name)
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    start = time.time()

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            total = int(resp.headers.get("Content-Length", 0))
            downloaded = 0
            speed = 0
            chunk_size = 1024 * 64  # 64KB

            with open(path, "wb") as f:
                async for chunk in resp.content.iter_chunked(chunk_size):
                    if user_tasks.get(user_id) == "cancelled":
                        LOGGER.info(f"Download cancelled: {file_name}")
                        return "cancelled"
                    f.write(chunk)
                    downloaded += len(chunk)
                    elapsed = time.time() - start
                    speed = downloaded / elapsed if elapsed > 0 else 0

                    await progress_loop("ᴅᴏᴡɴʟᴏᴀᴅ", message, file_name, downloaded, total, lambda: speed, user_id)

    return path

async def upload_file(bot: Client, path: str, message: Message, user_id: int):
    file_name = os.path.basename(path)
    total = os.path.getsize(path)
    uploaded = 0
    start = time.time()

    def speed_func():
        elapsed = time.time() - start
        return uploaded / elapsed if elapsed > 0 else 0

    async def update_progress(current, total_):
        nonlocal uploaded
        uploaded = current
        await progress_loop("ᴜᴘʟᴏᴀᴅ", message, file_name, uploaded, total_, speed_func, user_id)

    try:
        await bot.send_document(
            chat_id=message.chat.id,
            document=path,
            caption=f"**ᴜᴘʟᴏᴀᴅᴇᴅ ʙʏ Fᴛᴍ Dᴇᴠᴇʟᴏᴘᴇʀᴢ**",
            progress=update_progress
        )
    except Exception as e:
        LOGGER.error(f"Upload failed: {e}")
        await message.edit_text("❌ Upload failed.")
        return

    if os.path.exists(path):
        os.remove(path)
        LOGGER.info(f"File deleted after upload: {file_name}")

async def handle_task(bot: Client, message: Message, url: str, user_id: int):
    if is_downloading.get(user_id):
        await message.reply_text("⏳ Wait for your previous task to finish.")
        return

    is_downloading[user_id] = True
    try:
        data = await fetch_download_link(url)
        if not data["status"]:
            await message.edit_text("❌ Failed to get download link.")
            return

        file_name = data["name"]
        direct_url = data["url"]

        await message.edit_text("📥 Starting download...")

        path = await download_file(direct_url, file_name, user_id, message)
        if path == "cancelled":
            await message.edit_text("❌ Task cancelled.")
            return

        await message.edit_text("📤 Uploading to Telegram...")
        await upload_file(bot, path, message, user_id)

    finally:
        is_downloading.pop(user_id, None)
        user_tasks.pop(user_id, None)
