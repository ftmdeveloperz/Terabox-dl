# handlers.py

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import requests
import time
import psutil
from info import TERABOX_API

# Function to format file sizes
def format_size(size):
    if size > 1e9:
        return f"{size / 1e9:.2f} GB"
    elif size > 1e6:
        return f"{size / 1e6:.2f} MB"
    elif size > 1e3:
        return f"{size / 1e3:.2f} KB"
    else:
        return f"{size} B"

# Function to calculate ETA
def calculate_eta(start_time, current, total):
    elapsed_time = time.time() - start_time
    if current == 0:
        return "calculating..."
    speed = current / elapsed_time  # bytes per second
    remaining = total - current
    eta = remaining / speed
    return time.strftime('%H:%M:%S', time.gmtime(eta))

# Handle download command (terabox link)
@Client.on_message(filters.regex(r'https://www\.terabox\.com/s/.+'))
async def download(client: Client, message: Message):
    user_id = message.from_user.id
    terabox_link = message.text.strip()

    # Fetch file details using your TeraBox API
    response = requests.get(f"{TERABOX_API}{terabox_link}")
    data = response.json()

    if data.get("status") == "success":
        file_name = data["file_name"]
        file_size = data["file_size"]
        download_link = data["download_link"]
        file_preview = data.get("thumbnail", "https://example.com/thumbnail.jpg")  # Simulated thumbnail URL

        # Format file size for better readability
        formatted_size = format_size(file_size)

        # Send file preview (thumbnail) along with file name and size
        await message.reply_photo(
            photo=file_preview,
            caption=f"📄 **File Name**: {file_name}\n📏 **File Size**: {formatted_size}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬇️ ᴅᴏᴡɴʟᴏᴀᴅ", url=download_link)]
            ])
        )

        # Simulate the download process with a progress bar
        total_size = file_size
        start_time = time.time()

        progress = 0
        while progress < total_size:
            progress += 1024 * 1024  # Simulating 1MB download per loop iteration
            speed = 1024 * 50  # Simulating speed of 50KB/s
            eta = calculate_eta(start_time, progress, total_size)
            cpu_usage = psutil.cpu_percent(interval=1)
            ram_usage = psutil.virtual_memory().percent

            # Display progress bar
            progress_bar = "■" * int(progress / total_size * 40) + "□" * (40 - int(progress / total_size * 40))
            status_message = f"""
╭───────ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ───────〄
│
├📁 sɪᴢᴇ : {formatted_size} ✗ {format_size(progress)}
├📦 ᴘʀᴏɢʀᴇꜱꜱ : {progress / total_size * 100:.2f}%
├🚀 sᴘᴇᴇᴅ : {speed / 1024:.2f}KB/s
├⏱️ ᴇᴛᴀ : {eta}
├🏮 ᴄᴘᴜ : {cpu_usage}%  |  ʀᴀᴍ : {ram_usage}%
╰─[{progress_bar}]─〄
            """

            await message.reply(status_message, quote=True)

            # Wait a bit before updating progress
            time.sleep(1)

        # Once done, send the download completion message
        await message.reply("🎉 ᴅᴏᴡɴʟᴏᴀᴅ ᴄᴏᴍᴘʟᴇᴛᴇ! ᴇɴᴏʏ ᴛʜᴇ ꜰɪʟᴇ 📥", quote=True)


# Handle upload command (terabox link)
@Client.on_message(filters.regex(r'https://www\.terabox\.com/s/.+'))
async def upload(client: Client, message: Message):
    user_id = message.from_user.id
    terabox_link = message.text.strip()

    # Fetch file details using your TeraBox API
    response = requests.get(f"{TERABOX_API}{terabox_link}")
    data = response.json()

    if data.get("status") == "success":
        file_name = data["file_name"]
        file_size = data["file_size"]
        upload_link = data["upload_link"]
        file_preview = data.get("thumbnail", "https://example.com/thumbnail.jpg")  # Simulated thumbnail URL

        # Format file size for better readability
        formatted_size = format_size(file_size)

        # Send file preview (thumbnail) along with file name and size
        await message.reply_photo(
            photo=file_preview,
            caption=f"📄 **File Name**: {file_name}\n📏 **File Size**: {formatted_size}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔼 ᴜᴘʟᴏᴀᴅ", url=upload_link)]
            ])
        )

        # Simulate the upload process with a progress bar
        total_size = file_size
        start_time = time.time()

        progress = 0
        while progress < total_size:
            progress += 1024 * 1024  # Simulating 1MB upload per loop iteration
            speed = 1024 * 50  # Simulating speed of 50KB/s
            eta = calculate_eta(start_time, progress, total_size)
            cpu_usage = psutil.cpu_percent(interval=1)
            ram_usage = psutil.virtual_memory().percent

            # Display progress bar
            progress_bar = "■" * int(progress / total_size * 40) + "□" * (40 - int(progress / total_size * 40))
            status_message = f"""
╭───────ᴜᴘʟᴏᴀᴅɪɴɢ───────〄
│
├📁 sɪᴢᴇ : {formatted_size} ✗ {format_size(progress)}
├📦 ᴘʀᴏɢʀᴇꜱꜱ : {progress / total_size * 100:.2f}%
├🚀 sᴘᴇᴇᴅ : {speed / 1024:.2f}KB/s
├⏱️ ᴇᴛᴀ : {eta}
├🏮 ᴄᴘᴜ : {cpu_usage}%  |  ʀᴀᴍ : {ram_usage}%
╰─[{progress_bar}]─〄
            """

            await message.reply(status_message, quote=True)

            # Wait a bit before updating progress
            time.sleep(1)

        # Once done, send the upload completion message
        await message.reply("🎉 ᴜᴘʟᴏᴀᴅ ᴄᴏᴍᴘʟᴇᴛᴇ! ᴇɴᴏʏ ᴛʜᴇ ᴜᴘʟᴏᴀᴅᴇᴅ ꜰɪʟᴇ 🔼", quote=True)
