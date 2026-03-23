import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "ВСТАВЬ_СЮДА_НОВЫЙ_ТОКЕН"

WISHES = [
    "Скоро тебя ждёт радостная новость, которая поднимет настроение!",
    "Этой весной в твоей жизни появится повод для улыбки.",
    "Ты окажешься в нужное время в нужном месте.",
    "Скоро тебя ждёт приятный сюрприз.",
    "В этом году тебя ждёт удача и радость.",
    "Ты скоро получишь хорошую новость.",
    "Твоя энергия притянет новые возможности.",
    "Скоро ты порадуешь себя чем-то приятным.",
    "Тебя ждёт тёплая встреча.",
    "В этом году у тебя будет повод гордиться собой."
]

keyboard = ReplyKeyboardMarkup(
    [["Получить пожелание 🌸"]],
    resize_keyboard=True
)

user_predictions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌿 Добро пожаловать!\n\nНажмите кнопку и получите пожелание ✨",
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

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
