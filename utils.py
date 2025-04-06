import math
import time
from datetime import timedelta


def readable_bytes(size: int) -> str:
    if size == 0:
        return "0 B"
    power = 1024
    n = 0
    units = ["B", "KB", "MB", "GB", "TB"]
    while size >= power and n < len(units) - 1:
        size /= power
        n += 1
    return f"{size:.2f} {units[n]}"


def time_formatter(start_time=None):
    if start_time is None:
        return time.time()
    elapsed = time.time() - start_time
    return str(timedelta(seconds=int(elapsed)))


def progress_bar(current, total):
    percent = 0
    try:
        percent = current * 100 / total
    except ZeroDivisionError:
        pass
    filled = int(percent / 5)
    empty = 20 - filled
    bar = "■" * filled + "□" * empty
    return f"[{bar}] {percent:.2f}%"
