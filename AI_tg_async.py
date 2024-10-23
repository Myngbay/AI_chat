import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import asyncio

# Токены для OpenAI и Telegram
openai.api_key = "ВАШ_OPENAI_API_КЛЮЧ"
TELEGRAM_BOT_TOKEN = "ВАШ_TELEGRAM_API_КЛЮЧ"

# Хранение истории беседы
conversation = [{"role": "system", "content": "Ты помощник, который помогает пользователям."}]


# Асинхронная функция для генерации ответа
async def generate_response(user_message):
    conversation.append({"role": "user", "content": user_message})
    # Оставляем только последние 10 сообщений (если нужно)
    if len(conversation) > 10:
        conversation.pop(1)  # Удаляем самое старое сообщение, кроме системного
    try:
        response = await asyncio.to_thread(openai.ChatCompletion.create,
                                           model="gpt-3.5-turbo",
                                           messages=conversation)
        bot_message = response.choices[0].message['content']
        conversation.append({"role": "assistant", "content": bot_message})
        return bot_message
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return "Извините, сейчас я не могу ответить на ваш запрос."


# Асинхронный обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    bot_response = await generate_response(user_message)
    await update.message.reply_text(bot_response)


# Асинхронный обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я ваш помощник. Чем могу помочь?")


# Основная функция для запуска бота
async def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Обработчики для команды /start и текстовых сообщений
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен. Ожидание сообщений...")
    await app.run_polling()


if __name__ == '__main__':
    asyncio.run(main())
