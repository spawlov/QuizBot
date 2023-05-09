import os
import random


def get_dict_from_files(path, encode):
    result = {}
    list_files = [_ for _ in os.listdir(path) if _.endswith('.txt')]
    for filename in list_files:
        with open(
                os.path.normpath(f'{path}/{filename}'), 'r', encoding=encode
        ) as file:
            content = file.readlines()
        for count, line in enumerate(content):
            if line.startswith('Вопрос '):
                question = answer = str()
                question_line = count + 1
                while all([
                    question_line < len(content),
                    not content[question_line].startswith('Ответ')
                ]):
                    question += content[question_line].replace('\n', ' ')
                    question_line += 1
                answer_line = question_line + 1
                while all([
                    answer_line < len(content) - 1,
                    not content[answer_line].startswith('Вопрос ')
                ]):
                    answer += content[answer_line].replace('\n', ' ')
                    answer_line += 1
                result[question] = {'filename': filename, 'answer': answer}
    return result


def get_random_question(redis, user, questions):
    question = random.choice(list(questions.keys()))
    filename = questions[question]['filename']
    answer = questions[question]['answer']
    data = {'file': filename, 'question': question, 'answer': answer}
    redis.delete(user)
    redis.hset(user, mapping=data)
    return question
