# handlers.py

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import requests
import time
import psutil
from io import BytesIO
from info import TERABOX_API, START_TEXT, REPO_TEXT, HELP_TEXT


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

# Handle /start command
@Client.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    user_name = message.from_user.first_name
    await message.reply(f"Hello, {user_name}!\n{START_TEXT}")

# Handle /help command
@Client.on_message(filters.command("help"))
async def help(client: Client, message: Message):
    await message.reply(HELP_TEXT)

# Handle /repo command
@Client.on_message(filters.command("repo"))
async def repo(client: Client, message: Message):
    await message.reply(REPO_TEXT)
    
# Handle the download and then send the file to the user
@Client.on_message(filters.regex(r'https://www\.terabox\.com/s/.+'))
async def download_and_send(client: Client, message: Message):
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
        )

        # Simulate the download process with a progress bar
        total_size = file_size
        start_time = time.time()

        progress = 0
        download_response = requests.get(download_link, stream=True)

        # Create an empty BytesIO stream to store the downloaded file
        file_data = BytesIO()

        # Download the file in chunks and save it to the BytesIO buffer
        for chunk in download_response.iter_content(chunk_size=1024):
            file_data.write(chunk)
            progress += len(chunk)

            # Calculate the progress
            speed = len(chunk) / (time.time() - start_time)  # Speed in bytes per second
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

            # Send progress update to the user
            await message.reply(status_message, quote=True)

        # Once download is complete, upload the file to the user
        file_data.seek(0)  # Move the cursor to the beginning of the file

        # Now, send the file to the user
        await client.send_document(
            user_id,
            file_data,
            caption=f"📤 ᴜᴘʟᴏᴀᴅɪɴɢ: {file_name}",
        )

        # Send final message once the upload is complete
        await message.reply("🎉 ᴄᴏᴍᴘʟᴇᴛᴇ! ᴛʜᴇ ꜰɪʟᴇ ʜᴀs ʙᴇᴇɴ ᴜᴘʟᴏᴀᴅᴇᴅ 🔼", quote=True)
