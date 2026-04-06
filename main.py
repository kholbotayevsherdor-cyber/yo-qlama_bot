import telebot
import os
from flask import Flask
from threading import Thread
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Render uchun soxta server
app = Flask('')
@app.route('/')
def home():
    return "Bot ishlayapti!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# Bot sozlamalari
TOKEN = '8769170916:AAGFbaBiTVPCHzb3b71UAZJf0QsTniwqzBU'
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 6958856545  

TALABALAR = {
    6958856545: "Xolbo'tayev Sherdor",
    5419668423: "Begimqulov Birodar",
    1668924733: "Abdujalilova Havasxon",
    7229151486: "Abdullayeva Nodirabegim",
    850097948: "Soipova Diyora",
    5659126133: "Zoyidjonova Mubinabonu",
    7653980018: "Quronboyeva Mashhura",
    6813785129: "Ruxullayeva Salima",
    8381649603: "Solixjonova Dildora",
    5985215529: "Xotamova Mubinabonu",
    6499764671: "Mirzaliyeva Sevinch",
    5844561442: "Nasriddinova Sitora",
    786826960: "Jumatova Nigina",
    1729555343: "Muhammadjonova Shaxnoza"
}

yoqlama_bazasi = {}

@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton("📊 Bugungi hisobot"))
        markup.add(KeyboardButton("🏃 Yo'ldaman"), KeyboardButton("🎓 Universitetdaman"))
        markup.add(KeyboardButton("❌ Darsga bormayman"))
        bot.send_message(user_id, "Xush kelibsiz, Sherdor!", reply_markup=markup)
    elif user_id in TALABALAR:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton("🏃 Yo'ldaman"), KeyboardButton("🎓 Universitetdaman"), KeyboardButton("❌ Darsga bormayman"))
        bot.send_message(user_id, f"Salom {TALABALAR[user_id]}! Holatni tanlang:", reply_markup=markup)
    else:
        bot.send_message(user_id, "Siz ro'yxatda yo'qsiz.")

@bot.message_handler(func=lambda message: message.text in ["🏃 Yo'ldaman", "🎓 Universitetdaman", "❌ Darsga bormayman"])
def save_status(message):
    if message.from_user.id in TALABALAR:
        yoqlama_bazasi[message.from_user.id] = message.text
        bot.send_message(message.from_user.id, "✅ Saqlandi!")

@bot.message_handler(func=lambda message: message.text == "📊 Bugungi hisobot")
def send_report(message):
    if message.from_user.id == ADMIN_ID:
        report = "📊 **Yo'qlama:**\n\n"
        for tid, ism in TALABALAR.items():
            status = yoqlama_bazasi.get(tid, "Belgilamadi")
            report += f"{ism}: {status}\n"
        bot.send_message(ADMIN_ID, report)

if __name__ == '__main__':
    # Soxta serverni alohida oqimda ishga tushiramiz
    t = Thread(target=run)
    t.start()
    bot.infinity_polling()
