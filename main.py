import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

TOKEN = "8359171444:AAEXpu0AWsJ-Jc0IwpRN38HjMB7ut9eYVzU"
bot = telebot.TeleBot(TOKEN)

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

bot.infinity_polling(timeout=20, long_polling_timeout=10)
