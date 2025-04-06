# utils.py

import math
import time

def format_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def time_formatter(seconds):
    seconds = int(seconds)
    periods = [
        ('h', 3600),
        ('m', 60),
        ('s', 1)
    ]
    time_str = ""
    for suffix, length in periods:
        value = seconds // length
        if value:
            time_str += f"{value}{suffix} "
        seconds %= length
    return time_str.strip()

def progress_bar(current, total, speed=0, start_time=0):
    percent = current * 100 / total
    bar_length = 15
    filled_length = int(bar_length * percent / 100)
    bar = '■' * filled_length + '□' * (bar_length - filled_length)

    elapsed_time = time.time() - start_time
    speed_str = format_size(speed) + "/s" if speed else "0B/s"
    eta = (total - current) / speed if speed else 0
    eta_str = time_formatter(eta)

    current_str = format_size(current)
    total_str = format_size(total)

    return (
        f"📦 ꜰɪʟᴇ: {current_str} / {total_str}\n"
        f"🚀 ꜱᴘᴇᴇᴅ: {speed_str}\n"
        f"⏳ ᴇᴛᴀ: {eta_str}\n"
        f"[{bar}] {round(percent, 2)}%"
    )
