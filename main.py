import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN
from database import db

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    
    # Сохраняем информацию о пользователе в базу данных
    await db.add_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )
    
    await update.message.reply_text(
        f"Привет, {user.first_name}! Я сохранил твою информацию в базе данных.\n"
        f"Твой ID: {user.id}"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = """
Доступные команды:
/start - Начать работу с ботом
/help - Показать это сообщение
/myinfo - Показать твою информацию из базы данных
/stats - Показать статистику пользователей (только для разработчика)
    """
    await update.message.reply_text(help_text)

async def my_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать информацию о пользователе из базы данных"""
    user_id = update.effective_user.id
    user_data = await db.get_user(user_id)
    
    if user_data:
        info_text = f"""
Твоя информация в базе данных:
ID: {user_data['user_id']}
Username: @{user_data['username'] or 'не указан'}
Имя: {user_data['first_name'] or 'не указано'}
Фамилия: {user_data['last_name'] or 'не указана'}
Зарегистрирован: {user_data['created_at'].strftime('%d.%m.%Y %H:%M')}
Обновлен: {user_data['updated_at'].strftime('%d.%m.%Y %H:%M')}
        """
    else:
        info_text = "Информация о тебе не найдена в базе данных. Используй /start"
    
    await update.message.reply_text(info_text)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать статистику пользователей (только для разработчика)"""
    # Здесь можно добавить проверку на права администратора
    users = await db.get_all_users()
    stats_text = f"Всего пользователей в базе данных: {len(users)}"
    await update.message.reply_text(stats_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик обычных сообщений"""
    user = update.effective_user
    
    # Обновляем информацию о пользователе при каждом сообщении
    await db.add_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )
    
    await update.message.reply_text(
        f"Привет, {user.first_name}! Я получил твое сообщение и обновил твою информацию в базе данных."
    )

async def main():
    """Главная функция"""
    # Подключаемся к базе данных
    await db.connect()
    
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    print("Application created:", application)
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("myinfo", my_info))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запускаем бота
    logger.info("Бот запущен...")
    await application.run_polling()

if __name__ == '__main__':
    import nest_asyncio
    nest_asyncio.apply()
    import asyncio
    asyncio.get_event_loop().run_until_complete(main()) 