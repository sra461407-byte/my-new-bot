import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Token-ኑን ከ Render Environment Variables ላይ ያነባል
TOKEN = os.environ.get("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ሰላም! የTikTok ሊንክ ላክልኝና ቪዲዮውን ላውርድልህ።")

async def download_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    
    # ሊንኩ TikTok መሆኑን ማረጋገጫ
    if "tiktok.com" not in url:
        return

    msg = await update.message.reply_text("ቪዲዮው በመውረድ ላይ ነው... ⏳")
    
    # TikWM API - በጣም ፈጣንና አስተማማኝ ነው
    api_url = f"https://www.tikwm.com/api/?url={url}"
    
    try:
        response = requests.get(api_url).json()
        
        if response.get("code") == 0:
            # ቪዲዮው ያለ Watermark ይገኛል
            video_url = response["data"]["play"]
            caption = response["data"].get("title", "የወረደ TikTok ቪዲዮ")
            
            await update.message.reply_video(video: video_url, caption: caption)
            await msg.delete() # 'በመውረድ ላይ ነው' የሚለውን ጽሁፍ ያጠፋዋል
        else:
            await update.message.reply_text("ይቅርታ፣ ቪዲዮውን ማግኘት አልቻልኩም። ሊንኩን አረጋግጥ።")
    except Exception as e:
        await update.message.reply_text(f"ስህተት አጋጥሟል፦ {str(e)}")

if __name__ == '__main__':
    if not TOKEN:
        print("Error: TOKEN not found in environment variables!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_tiktok))

        print("Bot is running...")
        
        # Render ላይ 'No open ports' የሚለውን ስህተት ለማስቀረት
        # 8080 ፖርት ላይ እንዲያዳምጥ ያደርገዋል
        port = int(os.environ.get("PORT", 8080))
        app.run_polling()
