import telebot
import yt_dlp
import os
import zipfile
import shutil

BOT_TOKEN = '8336625978:AAEtTv5IuuuyMr_x7w3SJV00gv9hcDmv_EQ'
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(regexp=r'(https?://)?(www\.)?youtube\.com/playlist\?list=.*')
def download_playlist_zip(message):
    url = message.text
    chat_id = message.chat.id
    msg = bot.reply_to(message, "⏳ Tauseef bhai, Playlist check kar raha hoon... thoda wait karein.")

    folder_name = f"playlist_{chat_id}"
    os.makedirs(folder_name, exist_ok=True)

    # Virtual DJ ke liye 320kbps M4A aur Album Art ki settings
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/best',
        'outtmpl': f'{folder_name}/%(title)s.%(ext)s',
        'writethumbnail': True,
        'postprocessors': [
            {'key': 'FFmpegExtractAudio', 'preferredcodec': 'm4a', 'preferredquality': '320'},
            {'key': 'EmbedThumbnail'},
            {'key': 'FFmpegMetadata'},
        ],
        'ignoreerrors': True,
        'quiet': True,
        'no_warnings': True
    }

    try:
        bot.edit_message_text("🎧 Gane high-quality m4a (Virtual DJ Ready!) mein download ho rahe hain...", chat_id=chat_id, message_id=msg.message_id)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            playlist_title = info_dict.get('title', 'Tauseef_Music_Playlist').replace(" ", "_")

        bot.edit_message_text("📦 Download poora hua! Ab ZIP file bana raha hoon...", chat_id=chat_id, message_id=msg.message_id)

        zip_filename = f"{playlist_title}.zip"
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_name):
                for file in files:
                    if file.endswith('.m4a'):
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.basename(file_path))

        bot.edit_message_text("🚀 ZIP taiyar hai, bhej raha hoon...", chat_id=chat_id, message_id=msg.message_id)
        
        with open(zip_filename, 'rb') as doc:
            bot.send_document(
                chat_id, 
                doc, 
                caption=f"🎧 Playlist: **{playlist_title}**\n💿 Format: M4A (320kbps)\n🖼️ Thumbnail: Embedded\n\n- Tauseef Music ATS"
            )
        
        bot.delete_message(chat_id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ Error aaya: {str(e)}", chat_id=chat_id, message_id=msg.message_id)

    finally:
        shutil.rmtree(folder_name, ignore_errors=True)
        if os.path.exists(zip_filename):
            os.remove(zip_filename)

bot.infinity_polling()
