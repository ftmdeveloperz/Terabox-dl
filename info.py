

import os
from os import getenv, environ

# Telegram Bot & API Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "7575260816:AAGQeiKMKUGZF19yid7LylIL9CG4zIy135w")
API_ID = int(environ.get('API_ID', '22141398'))
API_HASH = environ.get('API_HASH', '0c8f8bd171e05e42d6f6e5a6f4305389')

# Bot Credentials 
BOT_NAME = os.getenv("BOT_NAME", "Fᴛᴍ TᴇʀᴀBᴏx")
OWNER_ID = int(os.getenv("OWNER_ID", "7744665378"))

# External API for TeraBox direct link
TERABOX_API = os.getenv("TERABOX_API", "https://tera-dl.vercel.app/api?link=")

# Symbols for Progress Bar
FILLED = os.getenv("FILLED", "■")
EMPTY = os.getenv("EMPTY", "□")



START_TEXT = "Welcome to the bot!"
BOT_USERNAME = "@your_bot"

ᴄʀᴇᴀᴛᴇᴅ ʙʏ: @ftmdeveloperz
"""
PORT = int(os.getenv("PORT", 8080))
