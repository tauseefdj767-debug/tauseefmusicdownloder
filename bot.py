import telebot, yt_dlp, os, zipfile, shutil, threading
from flask import Flask

server = Flask(__name__)
@server.route("/")
def hello(): return "DJ Tauseef Bot is Live!"

BOT_TOKEN = '8336625978:AAFH-SR6axF8X2kY73_EPc39FiaT8JVUMA'
bot = telebot.TeleBot(8336625978:AAFOs3dVnrY2vDBed24WzX3Qk5p1h2UEmEU)

@bot.message_handler(regexp=r'(https?://)?(www\.)?youtube\.com/playlist\?list=.*')
def download_playlist_zip(message):
    url, chat_id = message.text, message.chat.id
    msg = bot.reply_to(message, "⏳ Tauseef bhai, Playlist check ho rahi hai...")
    folder = f"playlist_{chat_id}"
    if not os.path.exists(folder): os.makedirs(folder)
    
    # Bina conversion wala settings (Sabse fast aur safe)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{folder}/%(title)s.%(ext)s',
        'ignoreerrors': True,
        'quiet': True,
        'no_warnings': True
    }
    
    try:
        bot.edit_message_text("🎧 Gane download ho rahe hain... thoda sabr rakhein.", chat_id, msg.message_id)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Tauseef_Playlist').replace(" ", "_")
        
        bot.edit_message_text("📦 ZIP file ban rahi hai...", chat_id, msg.message_id)
        zip_n = f"{title}.zip"
        
        # Check karein ki folder khali toh nahi hai
        files = os.listdir(folder)
        if not files:
            bot.edit_message_text("❌ Error: Gane download nahi ho paye. Playlist check karein.", chat_id, msg.message_id)
            return

        with zipfile.ZipFile(zip_n, 'w', zipfile.ZIP_DEFLATED) as z:
            for file in files:
                z.write(os.path.join(folder, file), file)
        
        with open(zip_n, 'rb') as doc:
            bot.send_document(chat_id, doc, caption=f"💿 {title}\n- Tauseef Music ATS")
        bot.delete_message(chat_id, msg.message_id)
        
    except Exception as e:
        bot.send_message(chat_id, f"❌ Error aa gaya: {str(e)}")
    finally:
        shutil.rmtree(folder, ignore_errors=True)
        if os.path.exists(zip_n): os.remove(zip_n)

if __name__ == "__main__":
    threading.Thread(target=lambda: bot.infinity_polling()).start()
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
