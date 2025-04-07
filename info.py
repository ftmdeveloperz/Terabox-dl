import os
from os import getenv, environ

# Telegram Bot & API Configuration
BOT_TOKEN = getenv("BOT_TOKEN", "7575260816:AAGQeiKMKUGZF19yid7LylIL9CG4zIy135w")
API_ID = int(environ.get("API_ID", "22141398"))
API_HASH = environ.get("API_HASH", "0c8f8bd171e05e42d6f6e5a6f4305389")

# Bot Details
BOT_NAME = getenv("BOT_NAME", "Fᴛᴍ TᴇʀᴀBᴏx")
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
