import os
from threading import Thread

from chat_bots.telegram import tg_bot
from chat_bots.vk import vk_bot

from dotenv import find_dotenv, load_dotenv

from loguru import logger

from notifiers.logging import NotificationHandler

import redis


def main():
    load_dotenv(find_dotenv())
    tg_handler_params = {
        'token': os.getenv('LOGGER_BOT_TOKEN'),
        'chat_id': int(os.getenv('ALLOWED_CHAT_ID'))
    }
    tg_handler = NotificationHandler('telegram', defaults=tg_handler_params)
    logger.add(
        'debug.log',
        format='{level}::{time}::{message}',
        level='DEBUG',
        rotation='0:00',
        compression='zip',
    )
    logger.add(
        'info.log',
        format='{level}::{time}::{message}',
        level='INFO',
        rotation='0:00',
        compression='zip',
    )
    logger.add(
        'error.log',
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

    Thread(target=vk_bot, args=(os.getenv('VK_TOKEN'), redis_client)).start()
    Thread(target=tg_bot, args=(os.getenv('TG_TOKEN'), redis_client)).start()


if __name__ == '__main__':
    main()
