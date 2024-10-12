import nest_asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackContext, CallbackQueryHandler
from datetime import time
import random

nest_asyncio.apply()

TOKEN = 'XXXXXXXX' # Reemplaza con el TOKEN
CHAT_ID = 'XXXXXXXX'  # Reemplaza con el chat ID que obtuviste

questions = [

    {
        "question": "¿Cuántas veces has utilizado la IA hoy?",
        "options": ["No la he usado", "Menos de 2 veces", "Más de 2 veces"]
    }
]

async def send_daily_question(context: CallbackContext):
    question = random.choice(questions)
    keyboard = [[InlineKeyboardButton(option, callback_data=option) for option in question["options"]]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(chat_id=CHAT_ID, text=question["question"], reply_markup=reply_markup)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Tu chat ID es: {CHAT_ID}')

async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    response = query.data
    await query.edit_message_text(text=f"Has seleccionado: {response}")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    job_queue = app.job_queue
    job_queue.run_daily(send_daily_question, time(hour=11, minute=10, second=0))  # Ajusta la hora según tu zona horaria (UTC) 20 son las 22 de España a 11 de octubre

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
