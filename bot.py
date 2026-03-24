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
    "💫 Сделайте сегодня маленький шаг к своему желанию, даже если он кажется незначительным.",
    "💫 Обратите внимание на свои мысли и замените сомнения на более поддерживающие формулировки.",
    "💫 Начните действовать там, где Вы давно откладываете первый шаг.",
    "💫 Позвольте себе немного замедлиться и восстановить внутренний ресурс.",
    "💫 Скажите «да» новой возможности или неожиданному предложению.",
    "💫 Честно ответьте себе, чего Вы действительно хотите.",
    "💫 Установите границу там, где Вам сейчас некомфортно.",
    "💫 Сделайте чуть больше, чем обычно, в важном для Вас деле.",
    "💫 Запишите своё желание и определите три простых шага к нему.",
    "💫 Позвольте себе двигаться без стремления к идеалу.",
    "💫 Сделайте то, что давно вызывает у Вас внутреннее сопротивление.",
    "💫 Обратите внимание на своё окружение и выберите поддерживающее.",
    "💫 Сфокусируйтесь на одном важном деле и доведите его до конца.",
    "💫 Дайте себе паузу, чтобы услышать свои настоящие желания.",
    "💫 Попробуйте новый способ решения привычной задачи.",
    "💫 Снизьте ожидания от себя и позвольте себе быть в процессе.",
    "💫 Поблагодарите себя за уже сделанные шаги.",
    "💫 Начните день с чёткого намерения и маленького действия.",
    "💫 Перестаньте ждать идеального момента и начните сейчас.",
    "💫 Поддержите себя словами, которые Вы сказали бы близкому человеку.",
    "💫 Сделайте выбор в пользу своего развития, даже если это непросто.",
    "💫 Обратите внимание на сигналы своего тела и дайте ему отдых.",
    "💫 Сделайте одно действие, которое приблизит Вас к результату.",
    "💫 Разрешите себе ошибаться и учиться на этом опыте.",
    "💫 Упростите задачу и начните с самого лёгкого шага.",
    "💫 Обратите внимание на то, что у Вас уже получается.",
    "💫 Сделайте паузу и пересмотрите свои приоритеты.",
    "💫 Переведите внимание с тревоги на конкретные действия.",
    "💫 Позвольте себе попросить поддержку, если она нужна.",
    "💫 Начните с того, что находится в зоне Вашего контроля.",
    "💫 Сделайте сегодня один шаг в сторону своих целей.",
    "💫 Отпустите лишний контроль и доверьтесь процессу.",
    "💫 Обратите внимание на возможности, которые уже рядом.",
    "💫 Сконцентрируйтесь на результате, а не на страхах.",
    "💫 Дайте себе разрешение двигаться в своём темпе.",
    "💫 Сделайте выбор в пользу того, что даёт Вам энергию.",
    "💫 Перестаньте сравнивать себя с другими и сосредоточьтесь на себе.",
    "💫 Определите один приоритет и уделите ему внимание сегодня.",
    "💫 Сделайте шаг навстречу тому, чего Вы хотите избежать.",
    "💫 Завершите начатое, чтобы освободить энергию для нового."
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
