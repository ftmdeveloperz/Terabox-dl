from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
from threading import Thread
import asyncio
import os

from download import download_from_terabox
from upload import upload_to_telegram
from queue import add_to_queue, remove_from_queue, get_queue_position, cancel_task, active_tasks
from utils import time_formatter

API_ID = 12345678  # Your API_ID here
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"

app = Flask(__name__)
bot = Client("ftm_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@app.route('/')
def home():
    return "Fᴛᴍ Dᴇᴠᴇʟᴏᴘᴇʀᴢ Tᴇʀᴀʙᴏx Bᴏᴛ Iꜱ Rᴜɴɴɪɴɢ!"


def run_flask():
    app.run(host="0.0.0.0", port=8080)


@bot.on_message(filters.command("start") & filters.private)
async def start(_, msg):
    await msg.reply_text(
        "ʜᴇʏ, ɪ'ᴍ ʀᴇᴀᴅʏ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴛᴇʀᴀʙᴏx ғɪʟᴇꜱ ғᴏʀ ʏᴏᴜ.\n\nᴊᴜꜱᴛ ꜱᴇɴᴅ ᴀ ʟɪɴᴋ.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("ᴍʏ Qᴜᴇᴜᴇ", callback_data="queue")]
        ])
    )


@bot.on_callback_query(filters.regex("queue"))
async def show_queue(_, cb):
    user_id = cb.from_user.id
    queue_text = active_tasks(user_id)
    await cb.message.edit_text(queue_text)


@bot.on_message(filters.private & filters.regex(r'https?://(?:www\.)?(terabox|4funbox)\.com/[^\s]+'))
async def handle_link(_, msg):
    user_id = msg.from_user.id
    url = msg.text.strip()

    added = add_to_queue(user_id, url)
    if not added:
        await msg.reply_text("⛔ ʏᴏᴜ ᴀʟʀᴇᴀᴅʏ ʜᴀᴠᴇ ᴀɴ ᴀᴄᴛɪᴠᴇ ᴛᴀꜱᴋ.")
        return

    pos = get_queue_position(user_id, url)
    m = await msg.reply_text(f"✅ ᴀᴅᴅᴇᴅ ᴛᴏ Qᴜᴇᴜᴇ! ᴘᴏꜱɪᴛɪᴏɴ: {pos}")

    await asyncio.sleep(pos * 3)  # Small delay for queue handling

    start_time = time_formatter()
    try:
        file_path, file_name, is_video = await download_from_terabox(url, m)
        await upload_to_telegram(bot, msg, file_path, file_name, is_video, start_time)
    except Exception as e:
        await msg.reply_text(f"❌ ᴇʀʀᴏʀ: {e}")
    finally:
        remove_from_queue(user_id, url)
        if os.path.exists(file_path):
            os.remove(file_path)


@bot.on_message(filters.command("cancel") & filters.private)
async def cancel_request(_, msg):
    user_id = msg.from_user.id
    success = cancel_task(user_id)
    if success:
        await msg.reply_text("✅ ʏᴏᴜʀ ᴛᴀꜱᴋ ʜᴀꜱ ʙᴇᴇɴ ᴄᴀɴᴄᴇʟᴇᴅ.")
    else:
        await msg.reply_text("⚠️ ɴᴏ ᴀᴄᴛɪᴠᴇ ᴛᴀꜱᴋ ᴛᴏ ᴄᴀɴᴄᴇʟ.")


def main():
    Thread(target=run_flask).start()
    print("✅ Fʟᴀꜱᴋ Sᴇʀᴠᴇʀ Rᴜɴɴɪɴɢ ᴏɴ Pᴏʀᴛ 8080")
    bot.run()


if __name__ == "__main__":
    main()
