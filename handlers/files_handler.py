import os
import random

from handlers.redis_handler import set_question_info

from redis.client import Redis


def get_dict_from_files(path: str, encode: str) -> dict:
    result = dict()
    list_files = [_ for _ in os.listdir(path) if _.endswith('.txt')]
    for filename in list_files:
        with open(path + filename, 'r', encoding=encode) as file:
            content = file.readlines()
        for count, line in enumerate(content):
            if line.startswith('Вопрос '):
                question = answer = str()
                question_line = count + 1
                while all([
                    question_line < len(content),
                    not content[question_line].startswith('Ответ')
                ]):
                    question += content[question_line].strip()
                    question_line += 1
                answer_line = question_line + 1
                while all([
                    answer_line < len(content) - 1,
                    not content[answer_line].startswith('Вопрос ')
                ]):
                    answer += content[answer_line].strip()
                    answer_line += 1
                result[question] = {'filename': filename, 'answer': answer}
    return result


def get_random_question(rd: Redis, user: [int, str], questions: dict) -> str:
    question = random.choice(list(questions.keys()))
    set_question_info(
        rd,
        user,
        questions[question]['filename'],
        question,
        questions[question]['answer']
    )
    return question
