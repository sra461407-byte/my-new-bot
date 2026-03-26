import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# --- Telegram bot token ---
# Tokenኑን Render ላይ በ Environment Variable በኩል እናስገባዋለን
TOKEN = os.environ.get("TOKEN")

# --- Telegram Bot Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("እንኳን ደህና መጡ! የቲከቶክ ሊንክ ይላኩና ቪዲዮውን ላውርድልዎ።")

async def download_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "tiktok.com" not in url:
        await update.message.reply_text("እባክዎ ትክክለኛ የቲከቶክ ሊንክ ይላኩ።")
        return
    
    await update.message.reply_text("ቪዲዮው በመውረድ ላይ ነው... ⏳")

    try:
        # ማሳሰቢያ፡ ይህ API ለምሳሌ ያህል የቀረበ ነው። የሚሰራ API መሆኑን ያረጋግጡ።
        api_url = f"https://api.tiktokdl.io/download?url={url}"
        response = requests.get(api_url)
        data = response.json()
        
        # የቪዲዮ ሊንኩን ማግኘት
        video_url = data.get('video', {}).get('url')
        
        if video_url:
            await context.bot.send_video(chat_id=update.message.chat_id, video=video_url)
        else:
            await update.message.reply_text("ቪዲዮውን ማግኘት አልተቻለም።")
            
    except Exception as e:
        await update.message.reply_text(f"ችግር አጋጥሟል: {e}")

# --- Telegram Bot Application ---
if __name__ == '__main__':
    if not TOKEN:
        print("Error: TOKEN not found in environment variables!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_tiktok))

        print("Bot is running...")
        app.run_polling()
