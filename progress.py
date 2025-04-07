import math
import time
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client
from utils import cancel_task, is_task_cancelled

PROGRESS_BAR = ["□"] * 20

def create_cancel_button(task_id: str):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_{task_id}")
    ]])

def human_readable_size(size):
    if not size:
        return "0B"
    power = 1024
    n = 0
    Dic_powerN = {0: '', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {Dic_powerN[n]}"

def format_bar(percent):
    done = round(percent / 5)
    return "▣" * done + "□" * (20 - done)

async def progress_hook(
    current: int,
    total: int,
    message,
    task_id: str,
    action: str = "Uploading",
    start_time: float = None
):
    if is_task_cancelled(task_id):
        await cancel_task(task_id, message)
        return

    now = time.time()
    speed = current / (now - start_time) if start_time else 0
    eta = (total - current) / speed if speed else 0

    percentage = current * 100 / total
    bar = format_bar(percentage)
    current_read = human_readable_size(current)
    total_read = human_readable_size(total)
    speed_read = human_readable_size(speed)
    eta_read = time.strftime("%H:%M:%S", time.gmtime(eta))

    text = f"""
╭───────{action}───────〄
│
├📁 sɪᴢᴇ : {current_read} ✗ {total_read}
├📦 ᴘʀᴏɢʀᴇꜱꜱ : {round(percentage, 2)}%
├🚀 sᴘᴇᴇᴅ : {speed_read}/s
├⏱️ ᴇᴛᴀ : {eta_read}
╰─[{bar}] {round(percentage, 2)}%
"""

    try:
        await message.edit(text, reply_markup=create_cancel_button(task_id))
    except Exception:
        pass
