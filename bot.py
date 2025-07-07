import os
from pyrogram import Client, filters
from yt_dlp import YoutubeDL

API_ID = 22413148  # Replace with your Telegram API_ID
API_HASH = "a1f4b3e3eee10ba35a09f8df7cd91c29"  # Replace with your Telegram API_HASH
BOT_TOKEN = "8036088062:AAFaW2rQ1Xh0TtgE00s5S3ocBajsi9H2xv0"  # Replace with the token from @BotFather

app = Client("music_downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'quiet': True,
}

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("🎵 Send me a YouTube link and I'll send you the MP3!")

@app.on_message(filters.text & filters.private)
async def download_music(client, message):
    url = message.text.strip()

    if "youtube.com" not in url and "youtu.be" not in url:
        await message.reply("❌ Please send a valid YouTube link.")
        return

    await message.reply("⏳ Downloading, please wait...")

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")

        await message.reply_audio(audio=filename, title=info.get("title", None))
        os.remove(filename)

    except Exception as e:
        await message.reply(f"❌ Error occurred: {str(e)}")

app.run()
