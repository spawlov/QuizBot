import random

from handlers.files_handler import get_next_question

from loguru import logger

from redis.client import Redis

import requests

import vk_api as vk
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import Event, VkEventType, VkLongPoll
from vk_api.vk_api import VkApiMethod


def send_message(
        vk_api: VkApiMethod, event: Event, keyboard:  VkKeyboard, text: str
) -> None:
    vk_api.messages.send(
        user_id=event.user_id,
        message=text,
        random_id=random.randint(1, 1000),
        keyboard=keyboard.get_keyboard(),
    )


def handler_user_action(
        event: Event, vk_api: VkApiMethod, keyboard:  VkKeyboard, rd: Redis
) -> None:
    if event.text == 'Новый вопрос':
        send_message(
            vk_api, event, keyboard, get_next_question(rd, event.user_id)
        )
        return
    elif event.text == 'Сдаться':
        answer = rd.hgetall(event.user_id)[b'answer'].decode('utf-8')
        send_message(vk_api, event, keyboard, f'Правильный ответ: {answer}')
        send_message(
            vk_api, event, keyboard, get_next_question(rd, event.user_id)
        )
        return
    answer = rd.hgetall(event.user_id)[b'answer'].decode('utf-8')
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
        vk_api, event, keyboard, get_next_question(rd, event.user_id)
    )
    return


def vk_bot(vk_token: str, redis_client: Redis) -> None:
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()

    keyboard = VkKeyboard()
    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Мой счёт', color=VkKeyboardColor.PRIMARY)

    long_poll = VkLongPoll(vk_session)
    logger.warning('Quiz VK bot is running!')
    try:
        for event in long_poll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                handler_user_action(event, vk_api, keyboard, redis_client)
    except (
            requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
    ) as e:
        logger.error(e)
        logger.error('Quiz VK bot is down!')
