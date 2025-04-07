from pyrogram import Client
from flask import Flask
from threading import Thread
from info import BOT_TOKEN, API_ID, API_HASH, PORT
from handlers import *

# Create Flask app
app = Flask("Fᴛᴍ Dᴇᴠᴇʟᴏᴘᴇʀᴢ")

@app.route('/')
def home():
    return "Fᴛᴍ Dᴇᴠᴇʟᴏᴘᴇʀᴢ Terabox Bot is Running!"

# Function to run Flask app in background
def run():
    app.run(host="0.0.0.0", port=PORT)

# Start the web server thread
Thread(target=run).start()

# Initialize Pyrogram Bot
bot = Client(
    "FtmTeraboxBot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

print(f"⚡ Bᴏss! Yᴏᴜʀ Bᴏᴛ ɪs sᴛᴀʀᴛᴇᴅ ᴀᴛ Pᴏʀᴛ {PORT} ✅")
print(f"🌐 Uʀʟ: http://localhost:{PORT}/")
print("🤖 Lᴏɢɢɪɴɢ ɪɴ...")

bot.run()
