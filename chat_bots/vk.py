import random

import requests
from loguru import logger
import vk_api as vk
from vk_api.longpoll import VkEventType, VkLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from handlers.redis_handler import get_question_info
from handlers.files_handler import get_random_question


def send_message(vk_api, event, keyboard, text):
    vk_api.messages.send(
        user_id=event.user_id,
        message=text,
        random_id=random.randint(1, 1000),
        keyboard=keyboard.get_keyboard(),
    )


def handler_user_action(event, questions, vk_api, keyboard, redis):
    if event.text == 'Новый вопрос':
        send_message(
            vk_api,
            event,
            keyboard,
            get_random_question(redis, event.user_id, questions)
        )
        return
    if event.text == 'Сдаться':
        answer = redis.hgetall(event.user_id)[b'answer'].decode('utf-8')
        send_message(vk_api, event, keyboard, f'Правильный ответ: {answer}')
        send_message(
            vk_api, event, keyboard, 'Для продолжения нажмите "Новый вопрос"'
        )
        return
    answer = get_question_info(redis, event.user_id)[2]
    answer_for_verify = answer.split('.')[0].replace('"', '')
    if answer_for_verify.lower() != event.text.lower():
        send_message(
            vk_api, event, keyboard, 'Неверно.\nПопробуте другой вариант...'
        )
        return
    send_message(
        vk_api,
        event,
        keyboard,
        f'Поздравляем, вы верно ответили на вопрос.\n\n'
        f'Полный вариант ответа:\n\n'
        f'{answer}'
    )
    send_message(
        vk_api, event, keyboard, 'Для продолжения нажмите "Новый вопрос"'
    )
    return


def vk_bot(vk_token, redis_client, questions):
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()

    keyboard = VkKeyboard()
    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)

    long_poll = VkLongPoll(vk_session)
    logger.warning('Quiz VK bot is running!')
    try:
        for event in long_poll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                handler_user_action(
                    event, questions, vk_api, keyboard, redis_client
                )
    except (
            requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
    ) as error:
        logger.error(error)
        logger.error('Quiz VK bot is down!')
