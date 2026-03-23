import os
import random
import threading

from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", "10000"))

WISHES = [
    "Этой весной Вас ждёт приятный сюрприз 🌸",
    "Скоро в Вашей жизни появится радостная новость ✨",
    "Вы окажетесь в нужное время в нужном месте 💫",
    "Весна принесёт Вам вдохновение и лёгкость 🌿",
    "Вас ждёт тёплая встреча с важным человеком 🤍",
    "Скоро исполнится маленькое, но очень важное желание 🌙",
    "Ваша энергия привлечёт новые возможности 💥",
    "В этом году Вы почувствуете настоящую гордость за себя 🌟",
    "Скоро Вы услышите слова, которые согреют сердце 💛",
    "Вас ждёт неожиданный повод для радости 🎉",
    "Весна откроет перед Вами новую дверь 🚪",
    "Скоро Вы сделаете шаг, который изменит многое 🔑",
    "Вас ждёт удача в важном деле 🍀",
    "Вы привлечёте в жизнь нужных людей 🤝",
    "Скоро Вы почувствуете внутреннюю уверенность 💎",
    "В этом году у Вас появится новая мечта 🌈",
    "Вас ждёт гармония и спокойствие 🕊",
    "Скоро в жизни станет больше лёгкости 🌬",
    "Вы найдёте ответ на важный вопрос 🔍",
    "Весна подарит Вам ясность и вдохновение ☀️",
    "Скоро Вас ждёт приятная неожиданность 🎁",
    "Вы сделаете правильный выбор 💡",
    "Ваша улыбка откроет новые возможности 😊",
    "Скоро в Вашей жизни станет больше радости 🌼",
    "Вы притянете удачные обстоятельства 🎯",
    "Весна принесёт финансовое улучшение 💰",
    "Вас ждёт успех в начатом деле 🚀",
    "Скоро Вы получите хорошие новости 📩",
    "Вы почувствуете прилив сил и энергии ⚡",
    "Вас ждёт вдохновляющее событие 🌟",
    "Скоро Вы порадуете себя чем-то долгожданным 💖",
    "Весна принесёт Вам внутреннее обновление 🌿",
    "Вы окажетесь среди правильных людей 👥",
    "Скоро в жизни появится новый шанс 🔓",
    "Вы почувствуете уверенность в своих решениях 🧠",
    "Вас ждёт период роста и развития 📈",
    "Скоро Вы достигнете маленькой победы 🏆",
    "Весна принесёт душевное тепло и радость 🌞",
    "Вы откроете в себе новую силу 💪",
    "Скоро произойдёт событие, которое Вас порадует 💫",
]

keyboard = ReplyKeyboardMarkup(
    [["Получить пожелание 🌸"]],
    resize_keyboard=True
)

user_predictions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌿 Добро пожаловать!\n\nНажмите кнопку и получите своё пожелание ✨",
        reply_markup=keyboard
    )

async def send_wish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in user_predictions:
        user_predictions[user_id] = random.choice(WISHES)

    wish = random.choice (WISHES)

    await update.message.reply_text(
        f"✨ Ваше пожелание на Навруз:\n\n💌 {wish}\n\n🌿 С Наврузом! Пусть этот год принесёт вам свет, радость и новые возможности ✨",
        reply_markup=keyboard
    )
    
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Получить пожелание 🌸":
        await send_wish(update, context)
    else:
        await update.message.reply_text(
            "Нажмите кнопку «Получить пожелание 🌸»",
            reply_markup=keyboard
        )

app_web = Flask(__name__)

@app_web.route("/")
def healthcheck():
    return "Navruz bot is running"

def run_web():
    app_web.run(host="0.0.0.0", port=PORT)

def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN не задан")

    thread = threading.Thread(target=run_web, daemon=True)
    thread.start()

    tg_app = ApplicationBuilder().token(TOKEN).build()
    tg_app.add_handler(CommandHandler("start", start))
    tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Бот запущен")
    tg_app.run_polling()

if __name__ == "__main__":
    main()
