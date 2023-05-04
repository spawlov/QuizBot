import os
import random

from redis.client import Redis


def from_file_to_dict(path: str) -> dict:
    with open(path, 'r', encoding='KOI8-R') as file:
        questions = file.readlines()
    result = dict()
    count = 0
    for count, question in enumerate(questions):
        if question.startswith('Вопрос '):
            question_index = count + 1
            question = answer = ''
            while question_index < len(questions) - 1 \
                    and not questions[question_index].startswith('Ответ'):
                question += questions[question_index].replace('\n', ' ')
                question_index += 1
            answer_index = question_index + 1
            while answer_index < len(questions) - 1 \
                    and not questions[answer_index].startswith('Вопрос '):
                answer += questions[answer_index]
                answer_index += 1
            result[question.rstrip()] = answer.rstrip()
    return result


def get_next_question(rd: Redis, user_id: [int, str]) -> str:
    filename = random.choice(os.listdir('questions/'))
    questions = from_file_to_dict(f'questions/{filename}')
    question = random.choice(list(questions.keys()))
    data = {
        'filename': filename,
        'question': question,
        'answer': questions[question],
    }
    rd.delete(user_id)
    rd.hset(user_id, mapping=data)
    return question
