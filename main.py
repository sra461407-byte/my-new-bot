import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Token-ኑን ከ Render Environment Variables ላይ ያነባል
TOKEN = os.environ.get("TOKEN")
# የቴሌግራም ቻናልህ ሊንክ
CHANNEL_LINK = "https://t.me/TokSaveHub"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Send me a TikTok link and I will download the video for you.")

async def download_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    
    # ሊንኩ TikTok መሆኑን ማረጋገጫ
    if "tiktok.com" not in url:
        return

    msg = await update.message.reply_text("Downloading your video... ⏳")
    
    # TikWM API - ፈጣንና አስተማማኝ ነው
    api_url = f"https://www.tikwm.com/api/?url={url}"
    
    try:
        response = requests.get(api_url).json()
        
        if response.get("code") == 0:
            video_url = response["data"]["play"]
            title = response["data"].get("title", "TikTok Video")
            
            # ከቪዲዮው ጋር የሚላክ ጽሁፍ (Caption)
            caption_text = f"✅ Video: {title}\n\n🚀 Downloaded via: @TokSaveBot\n📢 Join our channel: {CHANNEL_LINK}"
            
            await update.message.reply_video(video=video_url, caption=caption_text)
            await msg.delete()
        else:
            await update.message.reply_text("Sorry, I couldn't find the video. Please check the link.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    if not TOKEN:
        print("Error: TOKEN not found in environment variables!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_tiktok))

        print("Bot is running...")
        
        # Render ላይ 'No open ports' ስህተት ለማስቀረት
        port = int(os.environ.get("PORT", 8080))
        app.run_polling()
