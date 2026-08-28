import os
from flask import Flask, request
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

TOKEN = "8359171444:AAHSrMJYaw3IBrQjXU1tCZ2nMzarBGVrzH4"
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

# Webhook route that receives updates directly from Telegram
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    return 'Forbidden', 403

if __name__ == '__main__':
    # Automatically bind webhook to Render's live external URL
    render_url = os.environ.get("RENDER_EXTERNAL_URL")
    if render_url:
        bot.remove_webhook()
        bot.set_webhook(url=f"{render_url}/{TOKEN}")
        
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
