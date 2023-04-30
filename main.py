import os
import random

from dotenv import load_dotenv, find_dotenv
from loguru import logger
from notifiers.logging import NotificationHandler

from chat_bots.telegram import tg_bot


def from_file_to_dict(path: str) -> dict:
    with open(path, 'r', encoding='KOI8-R') as file:
        questions_lines = file.readlines()

    result = {}
    count = 0
    while count < len(questions_lines):
        if questions_lines[count].startswith('Вопрос '):
            question_index = count + 1
            question = answer = ''
            while question_index < len(questions_lines) - 1 \
                    and not questions_lines[question_index].startswith('Ответ'):
                question += questions_lines[question_index].replace('\n', ' ')
                question_index += 1
            answer_index = question_index + 1
            while answer_index < len(questions_lines) - 1 \
                    and not questions_lines[answer_index].startswith('Вопрос '):
                answer += questions_lines[answer_index]
                answer_index += 1
            result[question.rstrip()] = answer.rstrip().split('.')
        count += 1

    return result


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

    tg_bot(os.getenv('TG_BOT_TOKEN'))


if __name__ == '__main__':
    main()
    # print(filename := random.choice(os.listdir('questions/')))
    # theme = from_file_to_dict(f'questions/{filename}')
    # print('*' * 100)
    # print(key := random.choice(list(theme.keys())))
    # print('=' * 100)
    # print(theme[key][0])
    # print('*' * 100)
