import telebot
import requests
import time

BOT_TOKEN = "PUT_YOUR_BOT_TOKEN_HERE"
API_URL = "https://your-api-url.up.railway.app/card"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ أرسل ملف يحتوي على بطاقات لفحصها بصيغة:
`4111111111111111|12|2026|123`", parse_mode="Markdown")

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open("cc.txt", "wb") as new_file:
            new_file.write(downloaded_file)

        result = process_cards("cc.txt")
        bot.reply_to(message, f"✅ تم الفحص:
{result}")
    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ: {e}")

def process_cards(filename):
    try:
        with open(filename, "r") as f:
            cards = [line.strip() for line in f if line.strip()]
        return f"عدد البطاقات: {len(cards)}"
    except Exception as e:
        return f"خطأ أثناء المعالجة: {e}"

bot.infinity_polling()
