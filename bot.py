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
    "Этой весной тебя ждёт приятный сюрприз 🌸",
    "Скоро в твоей жизни появится радостная новость ✨",
    "Ты окажешься в нужное время в нужном месте 💫",
    "Весна принесёт тебе вдохновение и лёгкость 🌿",
    "Тебя ждёт тёплая встреча с важным человеком 🤍",
    "Скоро исполнится маленькое, но очень важное желание 🌙",
    "Твоя энергия привлечёт новые возможности 💥",
    "В этом году ты почувствуешь настоящую гордость за себя 🌟",
    "Скоро ты услышишь слова, которые согреют сердце 💛",
    "Тебя ждёт неожиданный повод для радости 🎉",
    "Весна откроет перед тобой новую дверь 🚪",
    "Скоро ты сделаешь шаг, который изменит многое 🔑",
    "Тебя ждёт удача в важном деле 🍀",
    "Ты привлечёшь в жизнь нужных людей 🤝",
    "Скоро ты почувствуешь внутреннюю уверенность 💎",
    "В этом году у тебя появится новая мечта 🌈",
    "Тебя ждёт гармония и спокойствие 🕊",
    "Скоро в жизни станет больше лёгкости 🌬",
    "Ты найдёшь ответ на важный вопрос 🔍",
    "Весна подарит тебе ясность и вдохновение ☀️",
    "Скоро тебя ждёт приятная неожиданность 🎁",
    "Ты сделаешь правильный выбор 💡",
    "Твоя улыбка откроет новые возможности 😊",
    "Скоро в твоей жизни станет больше радости 🌼",
    "Ты притянешь удачные обстоятельства 🎯",
    "Весна принесёт финансовое улучшение 💰",
    "Тебя ждёт успех в начатом деле 🚀",
    "Скоро ты получишь хорошие новости 📩",
    "Ты почувствуешь прилив сил и энергии ⚡",
    "Тебя ждёт вдохновляющее событие 🌟",
    "Скоро ты порадуешь себя чем-то долгожданным 💖",
    "Весна принесёт тебе внутреннее обновление 🌿",
    "Ты окажешься среди правильных людей 👥",
    "Скоро в жизни появится новый шанс 🔓",
    "Ты почувствуешь уверенность в своих решениях 🧠",
    "Тебя ждёт период роста и развития 📈",
    "Скоро ты достигнешь маленькой победы 🏆",
    "Весна принесёт душевное тепло и радость 🌞",
    "Ты откроешь в себе новую силу 💪",
    "Скоро произойдёт событие, которое тебя порадует 💫",
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

    wish = user_predictions[user_id]

    await update.message.reply_text(
        f"✨ Ваше пожелание:\n\n💌 {wish}",
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
