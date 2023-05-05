def set_question_info(redis, user, filename, question, answer):
    data = {'file': filename, 'question': question, 'answer': answer}
    redis.delete(user)
    return redis.hset(user, mapping=data)


def get_question_info(redis, user):
    redis_data = redis.hgetall(user)
    return (
        redis_data[b'file'].decode('utf-8'),
        redis_data[b'question'].decode('utf-8'),
        redis_data[b'answer'].decode('utf-8')
    )
