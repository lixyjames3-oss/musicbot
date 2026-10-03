import os
import yt_dlp
from pyrogram import Client, filters

# قراءة معلومات البوت بأمان من منصة الاستضافة
app = Client(
    "music_bot",
    bot_token=os.environ.get("8576088538:AAFr-Fvas0pzH2ZkJmNdlYlF_dB7fkafteQ"),
    api_id=int(os.environ.get("21129853")),
    api_hash=os.environ.get("383d64cb0d0bda6c3d8c6a5dae596d63")
)

@app.on_message(filters.command("start"))
def start_command(client, message):
    message.reply_text(
        "أهلاً بك في بوت تحميل الأغاني! 🎵\nأرسل لي اسم الأغنية أو رابط من يوتيوب وسأقوم بتحميلها لك."
    )

@app.on_message(filters.text & ~filters.command("start"))
def download_music(client, message):
    query = message.text
    status_msg = message.reply_text("جاري البحث والتحميل... ⏳")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_query = query if query.startswith("http") else f"ytsearch:{query}"
            info = ydl.extract_info(search_query, download=True)
            
            if 'entries' in info:
                info = info['entries'][0]
                
            filename = ydl.prepare_filename(info)
            audio_file = os.path.splitext(filename)[0] + ".mp3"

        status_msg.edit_text("جاري الإرسال... 📤")
        message.reply_audio(audio_file, title=info.get('title'))
        
        if os.path.exists(audio_file):
            os.remove(audio_file)
            
        status_msg.delete()

    except Exception as e:
        status_msg.edit_text(f"حدث خطأ أثناء التحميل: {str(e)}")

if __name__ == "__main__":
    print("البوت يعمل الآن...")
    app.run()
  
