def set_question_info(rd, user, filename, question, answer):
    data = {'file': filename, 'question': question, 'answer': answer}
    rd.delete(user)
    return rd.hset(user, mapping=data)


def get_question_info(rd, user):
    redis_data = rd.hgetall(user)
    return (
        redis_data[b'file'].decode('utf-8'),
        redis_data[b'question'].decode('utf-8'),
        redis_data[b'answer'].decode('utf-8')
    )
