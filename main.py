import os
import threading
import time
from flask import Flask
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

TOKEN = "8359171444:AAEXpu0AWsJ-Jc0IwpRN38HjMB7ut9eYVzU"
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/')
def health_check():
    return "Brainful Hub Bot is running 24/7!", 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_first_name = message.from_user.first_name or "there"
    
    welcome_text = (
        f"Hey @{user_first_name}👋 Welcome to Brainful Hub! 🚀\n"
        "Our academy is dedicated to helping pre-engineering students achieve their dreams. "
        "We are also expanding our resources for freshman students. Stay tuned!"
    )
    
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("Register for pre engineering", web_app=WebAppInfo(url="https://brainfulhub.lovable.app")))
    markup.row(InlineKeyboardButton("Contact us", url="https://t.me/Brainful_support"))
    markup.row(InlineKeyboardButton("Learning web", web_app=WebAppInfo(url="https://brainful-hub.lovable.app")))
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)
    bot.send_message(message.chat.id, "🔝 Main Menu")

@bot.message_handler(commands=['contact'])
def send_contact(message):
    bot.reply_to(message, "📩 *Brainful Hub Support*\n\nReach out to us directly: @Brainful_support", parse_mode="Markdown")

def start_polling():
    # Wait briefly on startup to allow any stale Telegram sessions to disconnect
    time.sleep(3)
    while True:
        try:
            bot.remove_webhook()
            bot.polling(none_stop=True, interval=1, timeout=20)
        except Exception as e:
            print(f"Session conflict or network drop: {e}. Retrying in 7 seconds...")
            time.sleep(7)

if __name__ == '__main__':
    threading.Thread(target=start_polling, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
