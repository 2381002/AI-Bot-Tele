import os
import openai
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Load environment variables from .env
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Pastikan API Key tidak None
if not TELEGRAM_BOT_TOKEN or not OPENAI_API_KEY:
    raise ValueError("API Key untuk Telegram atau OpenAI tidak ditemukan. Periksa file .env")

openai.api_key = OPENAI_API_KEY

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hai! Saya chatbot AI. Kirimkan pesanmu!")

async def chat(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        bot_reply = response["choices"][0]["message"]["content"]
        await update.message.reply_text(bot_reply)

    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("Maaf, terjadi kesalahan.")

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("Bot berjalan...")
    app.run_polling()

if __name__ == '__main__':
    main()
