from redis.asyncio.client import Redis


def set_question_info(
        rd: Redis,
        user: [int, str],
        filename: str,
        question: str,
        answer: str
) -> any:
    data = {
        'file': filename,
        'question': question,
        'answer': answer,
    }
    rd.delete(user)
    return rd.hset(user, mapping=data)


def get_question_info(rd: Redis, user: [int, str]) -> tuple:
    redis_data = rd.hgetall(user)
    return (
        redis_data[b'file'].decode('utf-8'),
        redis_data[b'question'].decode('utf-8'),
        redis_data[b'answer'].decode('utf-8')
    )
