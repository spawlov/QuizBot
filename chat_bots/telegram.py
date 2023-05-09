from loguru import logger
from telegram import ReplyKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
    Updater,
)

from handlers.files_handler import get_random_question

CHOOSING, TYPING_REPLY = range(2)


def start(bot, context):
    custom_keyboard = [['Новый вопрос', 'Сдаться']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
    user = bot.effective_user
    context.bot_data['redis'].delete(user.id)
    firstname = user.first_name if user.first_name else ''
    lastname = user.last_name if user.last_name else ''
    bot.message.reply_text(f'Здравствуйте, {firstname} {lastname}!')
    bot.message.reply_text(
        text='Чтобы начать нажмите "Новый вопрос"',
        reply_markup=reply_markup
    )
    return CHOOSING


def handle_new_question_request(bot, context):
    redis = context.bot_data['redis']
    questions = context.bot_data['questions']
    bot.message.reply_text(
        get_random_question(redis, bot.effective_user.id, questions)
    )
    return TYPING_REPLY


def handle_solution_attempt(bot, context):
    redis = context.bot_data['redis']
    answer = redis.hgetall(bot.effective_user.id)[b'answer'].decode('utf-8')
    answer_for_verify = answer.split('.')[0].replace('"', '')
    if answer_for_verify.lower() != bot.message.text.lower():
        bot.message.reply_text('Неверно.\nПопробуте другой вариант...')
        return TYPING_REPLY
    bot.message.reply_text(f'Поздравляем, вы верно ответили на вопрос.\n\n'
                           f'Полный вариант ответа:\n\n'
                           f'{answer}'
                           )
    bot.message.reply_text('Для продолжения нажмите "Новый вопрос"')
    return TYPING_REPLY


def handle_no_answer(bot, context):
    redis = context.bot_data['redis']
    answer = redis.hgetall(bot.effective_user.id)[b'answer'].decode('utf-8')
    bot.message.reply_text(f'Правильный ответ: {answer}')
    bot.message.reply_text('Для продолжения нажмите "Новый вопрос"')
    return CHOOSING


def tg_bot(token, redis_client, questions):
    bot = Updater(token)
    dispatcher = bot.dispatcher
    dispatcher.bot_data['redis'] = redis_client
    dispatcher.bot_data['questions'] = questions
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(
                    Filters.regex(r'Новый вопрос'), handle_new_question_request
                ),
            ],
            TYPING_REPLY: [
                MessageHandler(Filters.regex(r'Сдаться'), handle_no_answer),
                MessageHandler(Filters.text, handle_solution_attempt),

            ],
        },
        fallbacks=[],
    )
    dispatcher.add_handler(conv_handler)
    logger.warning('Quiz telegram bot is running!')
    bot.start_polling()
    bot.idle()
