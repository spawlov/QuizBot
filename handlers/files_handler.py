import os
import random


def from_file_to_dict(path: str) -> dict:
    with open(path, 'r', encoding='KOI8-R') as file:
        questions = file.readlines()
    result = dict()
    count = 0
    while count < len(questions):
        if questions[count].startswith('Вопрос '):
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
        count += 1
    return result


def get_next_question(rd, user_id) -> str:
    filename = random.choice(os.listdir(f'{os.path.basename("questions")}/'))
    questions = from_file_to_dict(f'{os.path.basename("questions")}/{filename}')
    question = random.choice(list(questions.keys()))
    data = {
        'filename': filename,
        'question': question,
        'answer': questions[question],
    }
    rd.delete(user_id)
    rd.hset(user_id, mapping=data)
    return question
