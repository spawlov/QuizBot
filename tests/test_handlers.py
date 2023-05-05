import os

from dotenv import find_dotenv, load_dotenv

from handlers.files_handler import get_dict_from_files, get_random_question
from handlers.redis_handler import set_question_info

import pytest

import redis

load_dotenv(find_dotenv())


def get_redis_client():
    rd = redis.Redis(
        host=os.getenv('REDIS_HOST'),
        port=int(os.getenv('REDIS_PORT')),
        username=os.getenv('REDIS_USER'),
        password=os.getenv('REDIS_PASSWORD'),
    )
    return rd


def test_type_result_get_dict_from_files():
    assert isinstance(
        get_dict_from_files('tests/questions/', 'koi8-r'), dict)


def test_length_result_get_dict_from_files():
    assert len(get_dict_from_files('tests/questions/', 'koi8-r')) == 48


def test_type_result_get_random_question():
    questions = get_dict_from_files('tests/questions/', 'koi8-r')
    assert isinstance(
        get_random_question(get_redis_client(), 'test_user', questions), str)
    get_redis_client().delete('test_user')


def test_not_empty_result_get_random_question():
    questions = get_dict_from_files('tests/questions/', 'koi8-r')
    assert len(
        get_random_question(get_redis_client(), 'test_user', questions)) != 0
    get_redis_client().delete('test_user')


def test_result_set_question_info():
    questions = get_dict_from_files('tests/questions/', 'koi8-r')
    question = get_random_question(get_redis_client(), 'test_user', questions)
    answer = questions[question]['answer']
    filename = questions[question]['filename']
    assert set_question_info(
        get_redis_client(), 'test_user', filename, question, answer) == 3
    get_redis_client().delete('test_user')


if __name__ == '__main__':
    pytest.main()
