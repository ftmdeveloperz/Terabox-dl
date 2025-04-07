<h1 align="center">TeraBox Downloader Bot</h1>
<p align="center">
  A powerful Telegram bot to fetch and upload files from TeraBox with full progress UI and controls.
</p>

---

<p align="center">
  <img src="https://img.shields.io/badge/Made%20By-Fᴛᴍ%20Dᴇᴠᴇʟᴏᴘᴇʀᴢ-ff69b4?style=for-the-badge" />
  <img src="https://img.shields.io/github/languages/top/ftmdeveloperz/terabox-dl?color=blue&style=for-the-badge" />
  <img src="https://img.shields.io/github/last-commit/ftmdeveloperz/terabox-dl?style=for-the-badge&color=orange" />
</p>

---

### 🎬 Demo

<p align="center">
  <img src="https://telegra.ph/file/f56aa1a54713dede9d938.gif" alt="Bot Demo" width="400"/>
</p>

---

### 🔗 Telegram Support

<p align="center">
  <a href="https://t.me/ftmdeveloperz"><img src="https://img.shields.io/badge/Contact-Developer-blue?style=for-the-badge&logo=telegram" /></a>
  <a href="https://t.me/YourBotUsername"><img src="https://img.shields.io/badge/Try%20Bot-Click%20Here-green?style=for-the-badge&logo=telegram" /></a>
</p>

---

## ✨ Features

- Direct TeraBox file downloads using **Boss's API**
- Upload to Telegram with:
  - ✅ Animated Unicode Progress Bars
  - ✅ File Size, Speed, ETA
  - ✅ ❌ Cancel Inline Button
- Real-time queue system (`/queue`)
- Full `/stats` with CPU/RAM tracking
- Auto deletion of downloaded file after upload
- Admin/Owner/User system
- Fully modular:
  - `info.py` for env and constants
  - `progress.py` for UI updates
  - `utils.py` for core functionality
  - `handlers.py` for commands
  - `ftm.py` main bot and Flask app

---

## ⚙️ Deployment (Railway / VPS)

### 1. Clone Repository

```bash
git clone https://github.com/ftmdeveloperz/Terabox-dl
cd Terabox-dl
```

### 2. Set Environment Variables

Create `.env` file or set these on Railway/VPS:

```env
BOT_TOKEN=your_telegram_bot_token
API_ID=your_api_id
API_HASH=your_api_hash
PORT=8080
OWNER_ID=your_telegram_id
```

All referenced from `info.py`.

---

### 3. Run Locally

```bash
pip install -r requirements.txt
python ftm.py
```

---

### 4. Docker Deployment

```bash
docker build -t terabox-bot .
docker run -d -p 8080:8080 --env-file .env terabox-bot
```

---

### 5. Railway Deployment

- Connect this repo to [Railway](https://railway.app)
- Add environment variables
- Deploy

Railway uses:
- `Procfile`
- `requirements.txt`
- `Dockerfile`

---

## 🧠 Commands

| Command        | Description                         |
|----------------|-------------------------------------|
| `/start`       | Show welcome message                |
| `/help`        | Show bot help                       |
| `/stats`       | Show bot RAM/CPU and usage stats    |
| `/queue`       | Show your position in the queue     |
| `/repo`        | Show repository disclaimer          |

---

## ⚠️ About /repo

> ɴᴏ, ᴡᴇ ᴀʀᴇ ɴᴏᴛ ꜰᴏᴏʟꜱ ᴛᴏ ɢɪᴠᴇ ʏᴏᴜ ᴏᴜʀ ʙᴏꜱꜱ'ꜱ ʜᴀʀᴅ ᴡᴏʀᴋ ꜰᴏʀ ꜰʀᴇᴇ ᴀɴᴅ ʀᴜɪɴ ʜɪꜱ ᴇꜰꜰᴏʀᴛꜱ.

> ᴛʜɪꜱ ʙᴏᴛ ᴜꜱᴇꜱ ᴏᴜʀ ʙᴏꜱꜱ'ꜱ ꜱᴘᴇᴄɪᴀʟ ᴀᴘɪ ᴀᴛ `https://tera-dl.vercel.app`, ɴᴏᴛ ᴀ ᴘᴜʙʟɪᴄ ᴀᴘɪ.

> ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ʙᴜʏ ᴏʀ ɴᴇᴇᴅ ᴀɴʏ ʜᴇʟᴘ, ᴄᴏɴᴛᴀᴄᴛ: [@ftmdeveloperz](https://t.me/ftmdeveloperz)

---

## ⚡ Credits

- API Service by: **ᴏᴜʀ ʙᴏꜱꜱ** via [tera-dl.vercel.app](https://tera-dl.vercel.app)
- Bot Developer: **Fᴛᴍ Dᴇᴠᴇʟᴏᴘᴇʀᴢ**
- Libraries: Pyrogram, Flask, Python3, psutil

---

## 🪄 License

This project is protected by Fᴛᴍ Dᴇᴠᴇʟᴏᴘᴇʀᴢ. Redistribution or copying the code/API without permission is strictly prohibited.

---