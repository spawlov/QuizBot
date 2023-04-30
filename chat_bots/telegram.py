from loguru import logger
from telegram import Update
from telegram.ext import (
    CallbackContext,
    Updater,
    CommandHandler,
    MessageHandler,
    Filters
)


def tg_start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    firstname = user.first_name if user.first_name else ''
    lastname = user.last_name if user.last_name else ''
    update.message.reply_text(
        f'Здравствуйте, {firstname} {lastname}!'
    )


def tg_send_message(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def tg_bot(token: str) -> None:
    bot = Updater(token)
    dispatcher = bot.dispatcher
    dispatcher.add_handler(CommandHandler("start", tg_start))
    dispatcher.add_handler(
        MessageHandler(
            Filters.text & ~Filters.command,
            tg_send_message
        )
    )
    bot.start_polling()
    logger.warning('QuizBot is running!')
