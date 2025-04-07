from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from info import START_TEXT, REPO_TEXT, BOT_USERNAME, OWNER_ID
from utils import handle_task, get_stats, get_queue
from progress import cancel_task
import asyncio

# Start command
@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message: Message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⚙️ Hᴇʟᴘ", callback_data="help")],
        [InlineKeyboardButton("🔗 Sᴇɴᴅ Lɪɴᴋ", switch_inline_query_current_chat="")],
        [InlineKeyboardButton("🛠️ Sᴏᴜʀᴄᴇ / Rᴇᴘᴏ", callback_data="repo")],
        [InlineKeyboardButton("👑 Dᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/ftmdeveloperz")]
    ])
    await message.reply_text(START_TEXT.format(message.from_user.first_name), reply_markup=keyboard, disable_web_page_preview=True)


# Help callback
@Client.on_callback_query(filters.regex("help"))
async def help_cb(_, query):
    await query.message.edit(
        "**🔧 Hᴏᴡ Tᴏ Usᴇ TᴇʀᴀBᴏx Bᴏᴛ:**\n\n"
        "1. Sᴇɴᴅ ᴀɴʏ Tᴇʀᴀʙᴏx Lɪɴᴋ\n"
        "2. Wᴀɪᴛ ғᴏʀ ᴅᴏᴡɴʟᴏᴀᴅ & ᴜᴘʟᴏᴀᴅ\n"
        "3. Rᴇᴄᴇɪᴠᴇ ғɪʟᴇ ᴅɪʀᴇᴄᴛʟʏ ɪɴ ᴛɪɴʏ ᴘᴀᴄᴋᴀɢᴇ",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("↩️ Bᴀᴄᴋ", callback_data="start")]
        ])
    )

# Repo callback
@Client.on_callback_query(filters.regex("repo"))
async def repo_cb(_, query):
    await query.message.edit(REPO_TEXT, reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("↩️ Bᴀᴄᴋ", callback_data="start")]
    ]))

# Queue command
@Client.on_message(filters.command("queue"))
async def queue_cmd(_, message: Message):
    queue_text = get_queue(message.from_user.id)
    await message.reply_text(queue_text)

# Stats command
@Client.on_message(filters.command("stats"))
async def stats_cmd(_, message: Message):
    stats_text = get_stats()
    await message.reply_text(stats_text)

# Cancel command
@Client.on_message(filters.command("cancel"))
async def cancel_cmd(_, message: Message):
    result = await cancel_task(message.from_user.id)
    await message.reply_text(result)

# Handle Terabox links
@Client.on_message(filters.private & filters.text & ~filters.command(["start", "help", "repo", "stats", "queue", "cancel"]))
async def handle_link(client, message: Message):
    if "terabox.com" not in message.text:
        return await message.reply("❌ Sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ ᴛᴇʀᴀʙᴏx ʟɪɴᴋ.")
    
    await handle_task(client, message)
