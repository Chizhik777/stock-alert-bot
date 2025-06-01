
import time
import json
import os
import telebot
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Загрузка переменных из .env
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

OZON_API_KEY = os.getenv("OZON_API_KEY")
OZON_CLIENT_ID = os.getenv("OZON_CLIENT_ID")

# Загрузка chat_ids
try:
    with open("chat_ids.json", "r") as f:
        chat_ids = json.load(f)
except FileNotFoundError:
    chat_ids = []

@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    if chat_id not in chat_ids:
        chat_ids.append(chat_id)
        with open("chat_ids.json", "w") as f:
            json.dump(chat_ids, f)
    bot.send_message(chat_id, "✅ Бот подключён! Вы будете получать уведомления об остатках.")

def check_ozon_stock():
    # Примерная заглушка функции
    # Здесь будет запрос к Ozon API
    # Если остаток стал 0 — возвращает список товаров с нулевыми остатками
    return ["Товар X", "Товар Y"]

def notify_users(products):
    for chat_id in chat_ids:
        for product in products:
            bot.send_message(chat_id, f"🔔 Закончился товар: {product}")

if __name__ == "__main__":
    while True:
        zero_stock_products = check_ozon_stock()
        if zero_stock_products:
            notify_users(zero_stock_products)
        time.sleep(600)  # каждые 10 минут
