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
