import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv
from handler.button_handlers import ButtonHandlers

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Update {update} caused error {context.error}")

def main():
    handlers = ButtonHandlers()
    
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", handlers.start_handler))
    application.add_handler(CommandHandler("menu", handlers.menu_handler))
    application.add_handler(CommandHandler("help", handlers.help_handler))
    application.add_handler(CommandHandler("points", handlers.points_handler))
    application.add_handler(CommandHandler("point", handlers.points_handler))
    application.add_handler(CommandHandler("ads", handlers.ads_handler))
    application.add_handler(CommandHandler("ad", handlers.ads_handler))
    application.add_handler(CommandHandler("language", handlers.language_handler))
    
    application.add_handler(CallbackQueryHandler(handlers.menu_callback, pattern="^menu_"))
    application.add_handler(CallbackQueryHandler(handlers.language_callback, pattern="^lang_"))
    
    application.add_error_handler(error_handler)

    application.run_polling()

if __name__ == '__main__':
    main() 