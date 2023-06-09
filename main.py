import os
from sys import argv

import redis
from loguru import logger
from dotenv import find_dotenv, load_dotenv
from notifiers.logging import NotificationHandler

from chat_bots.vk import vk_bot
from chat_bots.telegram import tg_bot
from handlers.files_handler import get_dict_from_files

logger.remove()


def main():
    load_dotenv(find_dotenv())
    tg_handler_params = {
        'token': os.getenv('LOGGER_BOT_TOKEN'),
        'chat_id': int(os.getenv('ALLOWED_CHAT_ID'))
    }
    tg_handler = NotificationHandler('telegram', defaults=tg_handler_params)
    logger.add(
        f'{os.getcwd()}/debug.log',
        format='{level}::{time}::{message}',
        level='DEBUG',
        rotation='0:00',
        compression='zip',
    )
    logger.add(
        f'{os.getcwd()}/info.log',
        format='{level}::{time}::{message}',
        level='INFO',
        rotation='0:00',
        compression='zip',
    )
    logger.add(
        f'{os.getcwd()}/error.log',
        format='{level}::{time}::{message}',
        level='ERROR',
        rotation='0:00',
        compression='zip',
    )
    logger.add(tg_handler, level='WARNING')

    redis_client = redis.Redis(
        host=os.getenv('REDIS_HOST'),
        port=int(os.getenv('REDIS_PORT')),
        username=os.getenv('REDIS_USER'),
        password=os.getenv('REDIS_PASSWORD'),
    )
    questions_dir = os.getenv('QUESTIONS_DIR', 'questions')
    questions_path = os.path.normpath(f'{os.getcwd()}/{questions_dir}')
    questions_encode = os.getenv('QUESTIONS_ENCODE', 'utf-8')
    questions = get_dict_from_files(questions_path, questions_encode)

    try:
        bot = argv[1]
    except IndexError as error:
        logger.error(f'{error}: bot not defined')
        return

    if bot == 'vk_bot':
        vk_bot(os.getenv('VK_TOKEN'), redis_client, questions)
    elif bot == 'tg_bot':
        tg_bot(os.getenv('TG_TOKEN'), redis_client, questions)
    logger.error(f'Bot "{bot}" not available')


if __name__ == '__main__':
    main()
