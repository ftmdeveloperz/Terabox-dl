import math
import psutil
import asyncio
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import (
    FILLED, EMPTY, SPINNER_FRAMES, SPIN_SPEED,
)

def human_readable_size(size: int) -> str:
    if size == 0:
        return "0B"
    power = 1024
    n = 0
    units = ["B", "KB", "MB", "GB", "TB"]
    while size >= power and n < len(units) - 1:
        size /= power
        n += 1
    return f"{size:.2f}{units[n]}"

def progress_bar(current: int, total: int, width: int = 20) -> str:
    filled_len = int(width * current // total) if total else 0
    bar = FILLED * filled_len + EMPTY * (width - filled_len)
    percent = (current / total * 100) if total else 0
    return f"[{bar}] {percent:.2f}%"

def get_system_usage() -> str:
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    return f"🏮 ᴄᴘᴜ : {cpu}%  |  ʀᴀᴍ : {ram}%"

def get_eta(speed: float, remaining: int) -> str:
    if speed == 0:
        return "∞"
    eta = remaining / speed
    return time_formatter(eta)

def time_formatter(seconds) -> str:
    seconds = int(seconds)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

async def generate_progress_msg(task: str, filename: str, current: int, total: int, speed: float, frame: str):
    size_text = f"📁 sɪᴢᴇ : {human_readable_size(current)} ✗ {human_readable_size(total)}"
    progress_text = f"📦 ᴘʀᴏɢʀᴇꜱꜱ : {(current / total) * 100:.2f}%"
    speed_text = f"🚀 sᴘᴇᴇᴅ : {human_readable_size(speed)}/s"
    eta_text = f"⏱️ ᴇᴛᴀ : {get_eta(speed, total - current)}"
    sys_text = get_system_usage()
    bar = progress_bar(current, total)

    return (
        f"╭───────{task.upper()}{frame}───────〄\n"
        f"│\n"
        f"├{size_text}\n"
        f"├{progress_text}\n"
        f"├{speed_text}\n"
        f"├{eta_text}\n"
        f"├{sys_text}\n"
        f"╰─{bar}"
    )

async def progress_loop(task: str, message, filename: str, current: int, total: int, speed_func, user_id: int):
    i = 0
    while current < total:
        speed = speed_func()
        frame = SPINNER_FRAMES[i % len(SPINNER_FRAMES)]
        i += 1
        text = await generate_progress_msg(task, filename, current, total, speed, frame)

        try:
            await message.edit_text(
                text=text,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("❌ ᴄᴀɴᴄᴇʟ", callback_data=f"cancel_{user_id}")]
                ])
            )
        except:
            pass

        await asyncio.sleep(SPIN_SPEED)
