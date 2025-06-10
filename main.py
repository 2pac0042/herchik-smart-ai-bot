import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")

menu_ru = ReplyKeyboardMarkup(
    [['📈 Тарифы', '📹 Курсы'], ['ℹ️ О проекте', '🌐 Сменить язык']], resize_keyboard=True)
menu_uz = ReplyKeyboardMarkup(
    [['📈 Tariflar', '📹 Kurslar'], ['ℹ️ Loyihamiz haqida', '🌐 Tilni o‘zgartirish']], resize_keyboard=True)

users_lang = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = users_lang.get(user_id, 'ru')
    if lang == 'ru':
        await update.message.reply_text("Добро пожаловать в Herchik Smart AI 🤖", reply_markup=menu_ru)
    else:
        await update.message.reply_text("Herchik Smart AI ga xush kelibsiz 🤖", reply_markup=menu_uz)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    lang = users_lang.get(user_id, 'ru')

    if text == "🌐 Сменить язык" or text == "🌐 Tilni o‘zgartirish":
        users_lang[user_id] = 'uz' if lang == 'ru' else 'ru'
        lang = users_lang[user_id]
        await update.message.reply_text(
            "Язык изменён ✅" if lang == 'ru' else "Til o‘zgartirildi ✅",
            reply_markup=menu_ru if lang == 'ru' else menu_uz
        )
    elif text in ["📈 Тарифы", "📈 Tariflar"]:
        await update.message.reply_text(
            "💼 Тарифы:
1 мес — 99,000 сум
3 мес — 199,000 сум
Lifetime — 499,000 сум

Напишите @forex0042 после оплаты."
        )
    elif text in ["📹 Курсы", "📹 Kurslar"]:
        await update.message.reply_text("🎓 Курсы пока недоступны. Скоро будут загружены.")
    elif text in ["ℹ️ О проекте", "ℹ️ Loyihamiz haqida"]:
        await update.message.reply_text("🤖 Herchik Smart AI — индикатор нового поколения.
Поддержка: @forex0042")
    else:
        await update.message.reply_text("❓ Неизвестная команда." if lang == 'ru' else "❓ Nomaʼlum buyruq.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, message_handler))

if __name__ == "__main__":
    app.run_polling()
