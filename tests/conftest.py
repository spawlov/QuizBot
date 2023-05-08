import os

import pytest
import redis
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


@pytest.fixture
def get_redis_client():
    return redis.Redis(
        host=os.getenv('REDIS_HOST'),
        port=int(os.getenv('REDIS_PORT')),
        username=os.getenv('REDIS_USER'),
        password=os.getenv('REDIS_PASSWORD'),
    )
