import psutil
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from info import START_TEXT, BOT_USERNAME
from utils import (
    start_download, cancel_tasks_for_user,
    get_user_queue, format_bytes
)


@Client.on_message(filters.command("start"))
async def start_cmd(bot, message: Message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Sᴇɴᴅ Lɪɴᴋ", switch_inline_query_current_chat="")],
        [InlineKeyboardButton("👑 Dᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/ftmdeveloperz")]
    ])
    await message.reply_text(
        text=f"**ʜᴇʏ {message.from_user.first_name}!\n\nɪ'ᴍ ᴀ ғᴀsᴛ & sᴍᴀʀᴛ Tᴇʀᴀʙᴏx ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴏʀ.**\n\n⏬ Sᴇɴᴅ ᴍᴇ ᴀɴʏ Tᴇʀᴀʙᴏx ʟɪɴᴋ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ᴀ ᴅɪʀᴇᴄᴛ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ.",
        reply_markup=buttons,
        disable_web_page_preview=True
    )


@Client.on_message(filters.command("repo"))
async def repo_cmd(bot, message: Message):
    await message.reply_text(
        "**🤖 Rᴇᴘᴏ Iɴꜰᴏ**\n\n"
        "ɴᴀʜ ᴅᴜᴅᴇ... ᴡᴇ'ʀᴇ ɴᴏᴛ ꜰᴏᴏʟs ᴛᴏ ɢɪᴠᴇ ᴀᴡᴀʏ ᴏᴜʀ ʀᴇᴘᴏ ꜰᴏʀ ꜰʀᴇᴇ.\n"
        "ᴍʏ ʙᴏss ʜᴀs ꜱᴘᴇɴᴛ ʜᴏᴜʀꜱ ᴏꜰ ʜᴀʀᴅ ᴡᴏʀᴋ ⌛ ᴛᴏ ᴍᴀᴋᴇ ᴛʜɪꜱ ʙᴏᴛ ⚙️.\n"
        "ᴡᴇ ᴅᴏɴ'ᴛ ʀᴜɪɴ ᴏᴜʀ ᴏᴡɴ ᴘʀᴏᴊᴇᴄᴛ ʙʏ ᴅʀᴏᴘᴘɪɴɢ ᴛʜᴇ ᴄᴏᴅᴇ ꜰᴏʀ ꜰʀᴇᴇ 🚫.\n\n"
        "💬 ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ʙᴜʏ ᴏʀ ɴᴇᴇᴅ ᴀɴʏ ʜᴇʟᴘ, ᴄᴏɴᴛᴀᴄᴛ ᴍʏ ᴅᴇᴠᴇʟᴏᴘᴇʀ @ftmdeveloperz ✅",
        disable_web_page_preview=True
    )


@Client.on_message(filters.command("help"))
async def help_cmd(bot, message: Message):
    await message.reply_text(
        "**🆘 Hᴇʟᴘ Mᴇɴᴜ**\n\n"
        "`/start` - Wᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇ\n"
        "`/repo` - Rᴇᴘᴏ ᴇxᴘʟᴀɪɴᴀᴛɪᴏɴ\n"
        "`/queue` - Sʜᴏᴡ ʏᴏᴜʀ ᴅᴏᴡɴʟᴏᴀᴅ Qᴜᴇᴜᴇ\n"
        "`/cancel` - Cᴀɴᴄᴇʟ ᴀʟʟ ʏᴏᴜʀ ᴛᴀsᴋs\n"
        "`/stats` - Bᴏᴛ ᴜsᴀɢᴇ sᴛᴀᴛs\n"
        "`/help` - Tʜɪs ᴍᴇɴᴜ\n\n"
        "Sᴇɴᴅ ᴀɴʏ Tᴇʀᴀʙᴏx ʟɪɴᴋ ᴛᴏ ɢᴇᴛ ꜰɪʟᴇ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ᴛᴏ Tᴇʟᴇɢʀᴀᴍ!",
        disable_web_page_preview=True
    )


@Client.on_message(filters.command("stats"))
async def stats_cmd(bot, message: Message):
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    await message.reply_text(
        f"**📊 Sʏsᴛᴇᴍ Sᴛᴀᴛs**\n\n"
        f"🖥️ CPU : `{cpu}%`\n"
        f"🧠 RAM : `{ram}%`\n"
        f"💾 Dɪsᴋ : `{disk}%`"
    )


@Client.on_message(filters.command("queue"))
async def queue_cmd(bot, message: Message):
    user_id = message.from_user.id
    queue_list = get_user_queue(user_id)
    if not queue_list:
        await message.reply_text("📭 Nᴏ ᴀᴄᴛɪᴠᴇ Qᴜᴇᴜᴇ ꜰᴏʀ ʏᴏᴜ.")
    else:
        msg = "📦 **Yᴏᴜʀ Dᴏᴡɴʟᴏᴀᴅ Qᴜᴇᴜᴇ:**\n\n"
        for i, item in enumerate(queue_list, 1):
            msg += f"`{i}.` {item}\n"
        await message.reply_text(msg)


@Client.on_message(filters.command("cancel"))
async def cancel_cmd(bot, message: Message):
    user_id = message.from_user.id
    result = cancel_tasks_for_user(user_id)
    await message.reply_text(
        "❌ Aʟʟ ᴏɴɢᴏɪɴɢ ᴛᴀꜱᴋs ʜᴀᴠᴇ ʙᴇᴇɴ ᴄᴀɴᴄᴇʟʟᴇᴅ." if result else "⚠️ Nᴏ ᴀᴄᴛɪᴠᴇ ᴛᴀꜱᴋs ꜰᴏᴜɴᴅ."
    )
