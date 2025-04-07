import math
import time
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatAction

PROGRESS_EMOJIS = ["□", "■"]
CANCEL_BUTTON = InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]])

def format_size(size):
    power = 2**10
    n = 0
    units = ["B", "KB", "MB", "GB", "TB"]
    while size > power and n < len(units)-1:
        size /= power
        n += 1
    return f"{size:.2f}{units[n]}"

def get_progress_bar(percent):
    filled = int(percent // 5)
    empty = 20 - filled
    return f"[{'■' * filled}{'□' * empty}] {percent:.2f}%"

async def update_progress(
    message,
    current,
    total,
    speed,
    start_time,
    task="ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ",
    tag="",
    keyboard=None
):
    if not keyboard:
        keyboard = CANCEL_BUTTON
    percent = current * 100 / total if total else 0
    elapsed = time.time() - start_time
    eta = (total - current) / speed if speed != 0 else 0

    bar = get_progress_bar(percent)
    text = f"""╭───────{task.upper()}───────〄
│
├📁 sɪᴢᴇ : {format_size(current)} ✗ {format_size(total)}
├📦 ᴘʀᴏɢʀᴇꜱꜱ : {percent:.2f}%
├🚀 sᴘᴇᴇᴅ : {format_size(speed)}/s
├⏱️ ᴇᴛᴀ : {time.strftime('%H:%M:%S', time.gmtime(eta))}
╰─{bar}
{tag}
"""

    try:
        await message.edit(text, reply_markup=keyboard)
    except Exception:
        pass

async def progress_hook(current, total, message, start_time, task="ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ", tag=""):
    now = time.time()
    elapsed_time = now - start_time
    speed = current / elapsed_time if elapsed_time > 0 else 0

    if elapsed_time % 5 == 0 or current == total:
        await update_progress(
            message=message,
            current=current,
            total=total,
            speed=speed,
            start_time=start_time,
            task=task,
            tag=tag,
        )

async def send_action(bot, chat_id, action):
    try:
        await bot.send_chat_action(chat_id, action)
    except Exception:
        pass
