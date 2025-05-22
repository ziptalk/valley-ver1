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
    application.add_handler(CommandHandler("help", handlers._handle_help_action))
    application.add_handler(CommandHandler("points", handlers._handle_points_action))
    application.add_handler(CommandHandler("point", handlers._handle_points_action))
    application.add_handler(CommandHandler("ads", handlers._handle_ad_action))
    application.add_handler(CommandHandler("ad", handlers._handle_ad_action))
    application.add_handler(CommandHandler("language", handlers._handle_language_action))
    
    application.add_handler(CallbackQueryHandler(handlers.claim_val_callback, pattern="^claim_val_"))
    application.add_handler(CallbackQueryHandler(handlers.menu_callback, pattern="^menu_"))
    application.add_handler(CallbackQueryHandler(handlers.language_callback, pattern="^lang_"))
    
    application.add_error_handler(error_handler)

    application.run_polling()

if __name__ == '__main__':
    main() 