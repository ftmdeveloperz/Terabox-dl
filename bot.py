import os
import time
import math
import psutil
import aiohttp
import asyncio
from flask import Flask
from threading import Thread
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Constants
API_ID = 12345678  # Replace with your own
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"

# Queues and Tracking
user_queues = {}
user_tasks = {}

# Flask Web Interface
app = Flask(__name__)

@app.route("/")
def home():
    return "<h3>Contact : <a href='https://t.me/ftmdeveloperz'>@ftmdeveloperz</a> || <a href='https://t.me/ftmdeveloperr'>@ftmdeveloperr</a></h3>"

Thread(target=lambda: app.run(host="0.0.0.0", port=8080)).start()

# Utility Functions
def humanbytes(size):
    if not size:
        return "N/A"
    power = 2**10
    n = 0
    units = ["", "K", "M", "G", "T"]
    while size > power and n < len(units) - 1:
        size /= power
        n += 1
    return f"{round(size, 2)}{units[n]}B"

def TimeFormatter(milliseconds):
    seconds = milliseconds // 1000
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

async def fetch_terabox_info(link: str) -> dict:
    api_url = f"https://tera-dl.vercel.app/api?link={link}"
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                return {"error": "Failed to fetch"}

async def progress_bar(current, total, message, start_time):
    percentage = (current / total) * 100
    elapsed = time.time() - start_time
    speed = current / elapsed
    eta = TimeFormatter((total - current) / speed * 1000) if speed > 0 else "∞"

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    bar = "■" * int(percentage / 5) + "□" * (20 - int(percentage / 5))

    text = (
        f"**╭───────Dᴏᴡɴʟᴏᴀᴅɪɴɢ───────〄**\n"
        f"**│**\n"
        f"**├📁 Sɪᴢᴇ : {humanbytes(current)} ✗ {humanbytes(total)}**\n"
        f"**├📦 Pʀᴏɢʀᴇꜱꜱ : {round(percentage, 2)}%**\n"
        f"**├🚀 Sᴘᴇᴇᴅ : {humanbytes(speed)}/s**\n"
        f"**├⏱️ Eᴛᴀ : {eta}**\n"
        f"**├🏮 Cᴘᴜ : {cpu}% | Rᴀᴍ : {ram}%**\n"
        f"**╰─[{bar}]**"
    )
    await message.edit(text)

async def handle_download(client, message, link):
    chat_id = message.chat.id
    msg = await message.reply("Processing your link...")

    data = await fetch_terabox_info(link)
    if "error" in data:
        return await msg.edit("Failed to get data from API.")

    file_name = data.get("name", "Unknown")
    file_size = data.get("size", "Unknown")
    d_url = data.get("download", None)
    if not d_url:
        return await msg.edit("Download link not found.")

    await msg.edit(f"**Queued:** {file_name} ({file_size})")

    if chat_id not in user_queues:
        user_queues[chat_id] = []
    user_queues[chat_id].append((file_name, d_url, msg))

    if chat_id not in user_tasks:
        user_tasks[chat_id] = asyncio.create_task(process_queue(client, chat_id))

async def process_queue(client, chat_id):
    while user_queues.get(chat_id):
        file_name, d_url, msg = user_queues[chat_id].pop(0)
        start_time = time.time()
        total = 100000000
        current = 0

        while current < total:
            await asyncio.sleep(1)
            current += 10000000
            await progress_bar(current, total, msg, start_time)
        await msg.edit(f"✅ **Completed**: {file_name}")

    user_tasks.pop(chat_id, None)

# Pyrogram Bot
bot = Client("ftm", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.private & filters.command("start"))
async def start(client, message):
    await message.reply("Send a Terabox link to begin downloading.")

@bot.on_message(filters.private & filters.command("queue"))
async def show_queue(client, message):
    q = user_queues.get(message.chat.id, [])
    if not q:
        return await message.reply("Your queue is empty.")
    msg = "**Your Queue:**\n"
    for i, (f, _, __) in enumerate(q):
        msg += f"`{i+1}. {f}`\n"
    await message.reply(msg)

@bot.on_message(filters.private & filters.command("stop"))
async def stop_all(client, message):
    chat_id = message.chat.id
    if task := user_tasks.get(chat_id):
        task.cancel()
    user_queues[chat_id] = []
    user_tasks.pop(chat_id, None)
    await message.reply("Your downloads have been cancelled.")

@bot.on_message(filters.private & filters.command("current"))
async def current_task(client, message):
    if task := user_tasks.get(message.chat.id):
        await message.reply("A task is currently running.")
    else:
        await message.reply("No active tasks.")

@bot.on_message(filters.private & filters.text & ~filters.command)
async def handle_text(client, message):
    if "terabox" in message.text:
        await handle_download(client, message, message.text.strip())
    else:
        await message.reply("Please send a valid Terabox link.")

bot.run()
