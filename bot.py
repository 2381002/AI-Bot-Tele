import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import openai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hai! Saya chatbot AI. Kirimkan pesanmu!")

def chat(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        bot_reply = response.choices[0].message.content
        update.message.reply_text(bot_reply)
    except Exception as e:
        print(f"Error: {e}")
        update.message.reply_text("Maaf, terjadi kesalahan.")

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, chat))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
