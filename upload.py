import os
import aiohttp
from pyrogram.types import Message
from utils import progress_bar, readable_bytes, time_formatter
from queue import check_cancel, clear_cancel

CHUNK_SIZE = 64 * 1024  # 64 KB


async def download_file(url, path, message: Message, user_id):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return f"ERROR: Failed to fetch file. Status code {resp.status}"

                total = int(resp.headers.get("Content-Length", 0))
                downloaded = 0
                start_time = time_formatter()

                with open(path, "wb") as f:
                    while True:
                        chunk = await resp.content.read(CHUNK_SIZE)
                        if not chunk:
                            break

                        f.write(chunk)
                        downloaded += len(chunk)

                        if downloaded % (CHUNK_SIZE * 8) == 0:
                            if await check_cancel(user_id):
                                return "CANCELLED"
                            await message.edit_text(
                                f"⬇️ Dᴏᴡɴʟᴏᴀᴅɪɴɢ...\n\n"
                                f"{progress_bar(downloaded, total)}\n"
                                f"📦 Sɪᴢᴇ: {readable_bytes(downloaded)} / {readable_bytes(total)}\n"
                                f"⏱️ Tɪᴍᴇ: {time_formatter(start_time)}"
                            )

        return "COMPLETED"

    except Exception as e:
        return f"ERROR: {str(e)}"


async def upload_to_telegram(path, message: Message, user_id):
    try:
        file_size = os.path.getsize(path)
        file_name = os.path.basename(path)
        ext = os.path.splitext(file_name)[1].lower()

        await message.edit_text("⬆️ Uᴘʟᴏᴀᴅɪɴɢ ᴛᴏ Tᴇʟᴇɢʀᴀᴍ...")

        caption = f"✅ Fɪʟᴇ: `{file_name}`\n📦 Sɪᴢᴇ: {readable_bytes(file_size)}"

        if ext in [".mp4", ".mkv", ".webm"]:
            await message.reply_video(path, caption=caption, supports_streaming=True)
        elif ext in [".mp3", ".wav", ".flac"]:
            await message.reply_audio(path, caption=caption)
        else:
            await message.reply_document(path, caption=caption)

        await message.delete()
        clear_cancel(user_id)
        os.remove(path)

    except Exception as e:
        await message.edit_text(f"❌ Eʀʀᴏʀ ᴡʜɪʟᴇ ᴜᴘʟᴏᴀᴅɪɴɢ:\n`{str(e)}`")
