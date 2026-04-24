import telebot, yt_dlp, os, zipfile, shutil, threading
from flask import Flask

# Render Free Tier ke liye Flask server
server = Flask(__name__)
@server.route("/")
def hello(): return "Tauseef Music Bot is Running!"

# Aapka Bot Token
BOT_TOKEN = '8336625978:AAEtTv5IuuuyMr_x7w3SJV00gv9hcDmv_EQ'
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(regexp=r'(https?://)?(www\.)?youtube\.com/playlist\?list=.*')
def download_playlist_zip(message):
    url, chat_id = message.text, message.chat.id
    msg = bot.reply_to(message, "⏳ Tauseef bhai, Playlist check ho rahi hai... thoda wait karein.")
    folder = f"playlist_{chat_id}"
    if not os.path.exists(folder): os.makedirs(folder)
    
    # Virtual DJ ke liye High Quality Settings
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/best',
        'outtmpl': f'{folder}/%(title)s.%(ext)s',
        'writethumbnail': True,
        'postprocessors': [
            {'key': 'FFmpegExtractAudio', 'preferredcodec': 'm4a', 'preferredquality': '320'},
            {'key': 'EmbedThumbnail'}, 
            {'key': 'FFmpegMetadata'}
        ],
        'ignoreerrors': True, 'quiet': True
    }
    
    try:
        bot.edit_message_text("🎧 Gane high-quality m4a mein download ho rahe hain...", chat_id, msg.message_id)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'Tauseef_Playlist').replace(" ", "_")
        
        bot.edit_message_text("📦 ZIP file ban rahi hai...", chat_id, msg.message_id)
        zip_n = f"{title}.zip"
        with zipfile.ZipFile(zip_n, 'w', zipfile.ZIP_DEFLATED) as z:
            for r, d, f in os.walk(folder):
                for file in f:
                    if file.endswith('.m4a'): 
                        z.write(os.path.join(r, file), file)
        
        with open(zip_n, 'rb') as doc:
            bot.send_document(chat_id, doc, caption=f"💿 {title}\n- Tauseef Music ATS")
        bot.delete_message(chat_id, msg.message_id)
        
    except Exception as e:
        bot.edit_message_text(f"❌ Error: {str(e)}", chat_id, msg.message_id)
    finally:
        shutil.rmtree(folder, ignore_errors=True)
        if os.path.exists(zip_n): os.remove(zip_n)

if __name__ == "__main__":
    # Bot aur Server ek sath chalu karne ke liye
    threading.Thread(target=lambda: bot.infinity_polling()).start()
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
