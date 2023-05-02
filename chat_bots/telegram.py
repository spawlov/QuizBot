from handlers.files_handler import get_next_question

from loguru import logger

from redis.client import Redis

from telegram import (
    ReplyKeyboardMarkup,
    Update,
)
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
    Updater,
)

TYPING_REPLY = range(1)


def start(update: Update, context: CallbackContext) -> range:
    custom_keyboard = [['Начать']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
    user = update.effective_user
    context.bot_data['redis'].delete(user.id)
    firstname = user.first_name if user.first_name else ''
    lastname = user.last_name if user.last_name else ''
    update.message.reply_text(
        f'Здравствуйте, {firstname} {lastname}!'
    )
    update.message.reply_text(
        text='Начнем, пожалуй...',
        reply_markup=reply_markup
    )
    return TYPING_REPLY


def handle_new_quiz(update: Update, context: CallbackContext) -> range:
    rd = context.bot_data['redis']
    custom_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счёт']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
    update.message.reply_text(
        get_next_question(rd, update.effective_user.id),
        reply_markup=reply_markup,
    )
    return TYPING_REPLY


def handle_new_question_request(update: Update,
                                context: CallbackContext) -> range:
    rd = context.bot_data['redis']
    update.message.reply_text(get_next_question(rd, update.effective_user.id))
    return TYPING_REPLY


def handle_solution_attempt(update: Update, context: CallbackContext) -> range:
    rd = context.bot_data['redis']
    answer = rd.hgetall(update.effective_user.id)[b'answer'].decode('utf-8')
    answer_for_verify = answer.split('.')[0].replace('"', '')
    if answer_for_verify.lower() != update.message.text.lower():
        update.message.reply_text('Неверно.\nПопробуте другой вариант...')
        return TYPING_REPLY
    update.message.reply_text(f'Поздравляем, вы верно ответили на вопрос.\n\n'
                              f'Полный вариант ответа:\n\n'
                              f'{answer}'
                              )
    update.message.reply_text(get_next_question(rd, update.effective_user.id))
    return TYPING_REPLY


def handle_no_answer(update: Update, context: CallbackContext) -> range:
    rd = context.bot_data['redis']
    answer = rd.hgetall(update.effective_user.id)[b'answer'].decode('utf-8')
    update.message.reply_text(f'Правильный ответ: {answer}')
    update.message.reply_text(get_next_question(rd, update.effective_user.id))
    return TYPING_REPLY


def tg_bot(token: str, redis_client: Redis) -> None:
    bot = Updater(token)
    dispatcher = bot.dispatcher
    dispatcher.bot_data['redis'] = redis_client
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            TYPING_REPLY: [
                MessageHandler(Filters.regex(r'Начать'), handle_new_quiz),
                MessageHandler(
                    Filters.regex(r'Новый вопрос'),
                    handle_new_question_request
                ),
                MessageHandler(Filters.regex(r'Сдаться'), handle_no_answer),
                MessageHandler(Filters.text, handle_solution_attempt)
            ],
        },
        fallbacks=[],
    )
    dispatcher.add_handler(conv_handler)
    logger.warning('Quiz telegram bot is running!')
    bot.start_polling()
