import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Token and Admin Configuration
TOKEN = os.environ.get("TOKEN")
ADMIN_ID = 8157391333  # ያንተ መለያ ቁጥር
CHANNEL_LINK = "https://t.me/TokSaveHub"

# ተጠቃሚዎችን ለመመዝገብ የሚያገለግል ተግባር
def save_user(user_id):
    user_id_str = str(user_id)
    if not os.path.exists("users.txt"):
        with open("users.txt", "w") as f:
            f.write(user_id_str + "\n")
    else:
        with open("users.txt", "r+") as f:
            users = f.read().splitlines()
            if user_id_str not in users:
                f.seek(0, 2)
                f.write(user_id_str + "\n")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_user(update.effective_user.id)
    await update.message.reply_text("Welcome! Send me a TikTok link to download the video for you.")

async def download_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_user(update.effective_user.id)
    url = update.message.text.strip()
    
    if "tiktok.com" not in url:
        return

    msg = await update.message.reply_text("Downloading your video... ⏳")
    api_url = f"https://www.tikwm.com/api/?url={url}"
    
    try:
        response = requests.get(api_url).json()
        if response.get("code") == 0:
            video_url = response["data"]["play"]
            title = response["data"].get("title", "TikTok Video")
            caption_text = f"✅ Video: {title}\n\n📢 Join our channel: {CHANNEL_LINK}"
            
            await update.message.reply_video(video=video_url, caption=caption_text)
            await msg.delete()
        else:
            await update.message.reply_text("Sorry, I couldn't find the video. Please check the link.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

# ማስታወቂያ ለመላክ (ለአንተ ብቻ)
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized to use this command!")
        return

    message_to_send = " ".join(context.args)
    if not message_to_send:
        await update.message.reply_text("📝 Usage: /broadcast [your message]")
        return

    if not os.path.exists("users.txt"):
        await update.message.reply_text("ℹ️ No users found yet.")
        return

    with open("users.txt", "r") as f:
        users = f.read().splitlines()
    
    success = 0
    failed = 0
    await update.message.reply_text(f"🚀 Sending broadcast to {len(users)} users...")

    for user_id in users:
        try:
            await context.bot.send_message(chat_id=int(user_id), text=message_to_send)
            success += 1
        except:
            failed += 1
            continue
    
    await update.message.reply_text(f"✅ Done!\nSent: {success}\nFailed: {failed}")

if __name__ == '__main__':
    if not TOKEN:
        print("Error: TOKEN not found!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("broadcast", broadcast))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_tiktok))

        print("Bot is running...")
        port = int(os.environ.get("PORT", 8080))
        app.run_polling()
