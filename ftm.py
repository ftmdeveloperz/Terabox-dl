import logging
from pyrogram import Client
from pyrogram.enums import ParseMode
from handlers import *
from flask import Flask
from threading import Thread
from info import API_ID, API_HASH, BOT_TOKEN, BOT_SESSION, PORT

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("Fᴛᴍ Dᴇᴠᴇʟᴏᴘᴇʀᴢ")

# Pyrogram Client
bot = Client(
    name=BOT_SESSION,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    parse_mode=ParseMode.MARKDOWN
)

# Flask Web App
app = Flask("Fᴛᴍ Dᴇᴠᴇʟᴏᴘᴇʀᴢ")

@app.route('/')
def home():
    return "Fᴛᴍ Tᴇʀᴀʙᴏx Bᴏᴛ Rᴜɴɴɪɴɢ ✅"

def run_flask():
    app.run(host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    logger.info("🧠 Bᴏꜱꜱ, ʏᴏᴜʀ ꜰʟᴀꜱᴋ ᴀᴘᴘ sᴛᴀʀᴛᴇᴅ ᴀᴛ ➤ http://0.0.0.0:%s", PORT)
    logger.info("⚡ Bᴏꜱꜱ, ʏᴏᴜʀ ʙᴏᴛ ɪs ɴᴏᴡ ᴏɴʟɪɴᴇ ᴀɴᴅ ʀᴇᴀᴅʏ ꜰᴏʀ ᴀᴄᴛɪᴏɴ!")
    bot.run()
