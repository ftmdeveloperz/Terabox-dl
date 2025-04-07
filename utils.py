import os
import time
import shutil
import aiofiles
import requests
from pyrogram import Client
from pyrogram.types import Message
from progress import progress_hook, send_action
from info import API_ENDPOINT, DOWNLOADS_DIR, EMOJIS

# Active task tracker
active_tasks = {}

# Cancel task
async def cancel_task(user_id):
    if user_id in active_tasks:
        active_tasks[user_id]["cancelled"] = True

# Download file using provided API
async def download_file(user_id, link, message: Message):
    start_time = time.time()
    msg = await message.reply(f"{EMOJIS['download']} Fetching download link...", quote=True)

    try:
        response = requests.get(f"{API_ENDPOINT}?link={link}")
        data = response.json()
        if not data.get("success"):
            return await msg.edit(f"{EMOJIS['error']} Failed to get download link.")

        file_url = data.get("download_link")
        file_name = data.get("file_name")
        file_size = int(data.get("file_size", 0))

        file_path = os.path.join(DOWNLOADS_DIR, f"{user_id}_{file_name}")
        active_tasks[user_id] = {"cancelled": False}

        async with aiofiles.open(file_path, "wb") as f:
            downloaded = 0
            with requests.get(file_url, stream=True) as r:
                for chunk in r.iter_content(chunk_size=4096):
                    if active_tasks[user_id]["cancelled"]:
                        await msg.edit(f"{EMOJIS['cancel']} Task cancelled.")
                        return None
                    await f.write(chunk)
                    downloaded += len(chunk)
                    await progress_hook(downloaded, file_size, msg, start_time, task="ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ")

        await msg.edit(f"{EMOJIS['done']} Download complete. Uploading...")
        return file_path

    except Exception as e:
        return await msg.edit(f"{EMOJIS['error']} Error: `{str(e)}`")

# Upload file to Telegram
async def upload_file(client: Client, message: Message, file_path: str):
    start_time = time.time()
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    await send_action(client, message.chat.id, "upload_document")

    msg = await message.reply(f"{EMOJIS['upload']} Uploading `{file_name}`...", quote=True)

    async def progress(current, total):
        await progress_hook(current, total, msg, start_time, task="ᴜᴘʟᴏᴀᴅɪɴɢ")

    try:
        await client.send_document(
            chat_id=message.chat.id,
            document=file_path,
            caption=f"{EMOJIS['done']} Uploaded: `{file_name}`",
            progress=progress,
        )
        await msg.delete()
    except Exception as e:
        await msg.edit(f"{EMOJIS['error']} Upload failed: `{e}`")
    finally:
        try:
            os.remove(file_path)
        except:
            pass
