import os
from os import getenv, environ

# Telegram Bot & API Configuration
BOT_TOKEN = getenv("BOT_TOKEN", "7575260816:AAGQeiKMKUGZF19yid7LylIL9CG4zIy135w")
API_ID = int(environ.get("API_ID", "22141398"))
API_HASH = environ.get("API_HASH", "0c8f8bd171e05e42d6f6e5a6f4305389")

# Bot Details
BOT_NAME = getenv("BOT_NAME", "Fᴛᴍ TᴇʀᴀBᴏx")
BOT_USERNAME = os.getenv("BOT_USERNAME", "FtmTeraboxBot")
OWNER_ID = int(getenv("OWNER_ID", "7744665378"))

# External API for TeraBox Direct Link
TERABOX_API = getenv("TERABOX_API", "https://tera-dl.vercel.app/api?link=")

# Flask Port
PORT = int(getenv("PORT", "8080"))

# Start Text
START_TEXT = """
ʜᴇʟʟᴏ {user_mention} !

ɪ ᴀᴍ ᴀ ᴘᴏᴡᴇʀꜰᴜʟ ᴛᴇʀᴀʙᴏx ᴅᴏᴡɴʟᴏᴀᴅᴇʀ ʙᴏᴛ ⚡
ꜱᴇɴᴅ ᴍᴇ ᴀɴʏ ᴛᴇʀᴀʙᴏx ʟɪɴᴋ & ɪ'ʟʟ ᴅᴏ ᴛʜᴇ ᴍᴀɢɪᴄ

╭──ꜰᴇᴀᴛᴜʀᴇꜱ───➤
├ ᴀᴜᴛᴏ ʟɪɴᴋ ɢʀᴀʙ & ᴘᴀʀꜱᴇ
├ ꜰᴀꜱᴛ ᴜᴘʟᴏᴀᴅ ᴡɪᴛʜ ᴘʀᴏɢʀᴇꜱꜱ
├ ᴀᴅᴠᴀɴᴄᴇᴅ ϙᴜᴇᴜᴇ ꜱʏꜱᴛᴇᴍ
╰─────────────⍟
"""

# Repo Command Response
REPO_TEXT = """
ᴅᴏ ɴᴏᴛ ᴀꜱᴋ ꜰᴏʀ ᴛʜᴇ ꜱᴏᴜʀᴄᴇ ᴄᴏᴅᴇ ⛔

ɪ'ᴍ ɴᴏᴛ ꜰᴏᴏʟ ᴇɴᴏᴜɢʜ ᴛᴏ ʀᴜɪɴ ᴍʏ ʙᴏꜱꜱ'ꜱ ʜᴀʀᴅ ᴡᴏʀᴋ ꜰᴏʀ ꜰʀᴇᴇ ❌

ɪꜰ ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴜʏ ᴏʀ ᴡᴀɴᴛ ᴀɴʏ ʜᴇʟᴘ, ᴄᴏɴᴛᴀᴄᴛ ᴍʏ ʙᴏꜱꜱ ᴀᴛ ➤ @ftmdeveloperz
"""

HELP_TEXT = """
ʜᴇʟʟᴏ!

I'ᴍ ᴀ ᴘᴏᴡᴇʀꜰᴜʟ ᴛᴇʀᴀʙᴏx ᴅᴏᴡɴʟᴏᴀᴅᴇʀ ʙᴏᴛ ⚡
ᴄᴏᴍᴘʟᴇᴛᴇ ᴍʏ ᴛᴀsᴋs ᴏɴʟɪɴᴇ ᴇᴀsɪʟʏ!

╭──ꜰᴇᴀᴛᴜʀᴇꜱ───➤
├ 🌀 **ᴀᴜᴛᴏ ᴛᴇʀᴀʙᴏx ʟɪɴᴋ ᴘᴀʀꜱɪɴɢ**
├ 🚀 **ꜰᴀsᴛ ᴜᴘʟᴏᴀᴅ & ᴅᴏᴡɴʟᴏᴀᴅ ᴘʀᴏɢʀᴇss ʙᴀʀ**
├ 🎬 **ᴇɴᴏᴜɢʜ ᴍᴇᴛʜᴏᴅs ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ & ᴜᴘʟᴏᴀᴅ ᴀɴʏ ᴛᴇʀᴀʙᴏx ʟɪɴᴋ**
├ 💾 **ᴘʀᴏɢʀᴇss ʙᴀʀs ᴅᴜʀɪɴɢ ᴜᴘʟᴏᴀᴅ & ᴅᴏᴡɴʟᴏᴀᴅ**
╰────────────────────⍟

ɴᴏᴡ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴀ ᴛᴇʀᴀʙᴏx ꜱᴇᴛᴇᴍ:
➡ ᴊᴜsᴛ ᴍᴇɴᴛɪᴏɴ ᴍᴇ ᴀ ᴛᴇʀᴀʙᴏx ʟɪɴᴋ, ᴀɴᴅ ɪ'ʟʟ ʜᴀɴᴄʟᴇ ɪᴛ! 🌟

ɪғ ʏᴏᴜ ɴᴇᴇᴅ ᴇxᴘʟᴀɴᴀᴛɪᴏɴ ᴏʀ ᴛʀᴏᴜʙʟᴇs, ᴄᴏɴᴛᴀᴄᴛ ᴍʏ ʙᴏꜱꜱ @ftmdeveloperz

╭──ᵗʏᴘɪᴄᴀʟ ᴄᴏᴍᴍᴀɴᴅs───➤
├ /start - ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇ
├ /help - ᴘʀᴏᴠɪᴅᴇs ᴏᴠᴇʀᴠɪᴇᴡ ᴏꜰ ᴛʜᴇ ᴍᴏᴛᴏʀ
├ /repo - ɪɴꜰᴏ ᴀʙᴏᴜᴛ ᴛʜᴇ ʙᴏᴛ's ꜱᴏᴜʀᴄᴇ ᴄᴏᴅᴇ

ᴇɴᴊᴏʏ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ꜱᴇʀᴠɪᴄᴇs 🖤
"""
