import os
from unittest import TestCase, main

from dotenv import find_dotenv, load_dotenv

from handlers.files_handler import from_file_to_dict, get_next_question

import redis

load_dotenv(find_dotenv())


class HandlersTest(TestCase):
    @staticmethod
    def get_redis_client():
        rd = redis.Redis(
            host=os.getenv('REDIS_HOST'),
            port=int(os.getenv('REDIS_PORT')),
            username=os.getenv('REDIS_USER'),
            password=os.getenv('REDIS_PASSWORD'),
        )
        return rd

    def test_from_file_to_dict_type_result(self):
        self.assertEqual(
            isinstance(from_file_to_dict('questions/test.txt'), dict), True
        )

    def test_from_file_to_dict_len_dict(self):
        self.assertEqual(len(from_file_to_dict('questions/test.txt')), 48)

    def test_get_next_question_type_result(self):
        self.assertEqual(isinstance(
            get_next_question(self.get_redis_client(), 'test_user'), str
        ), True)
        self.get_redis_client().delete('test_user')

    def test_get_next_question_len_result(self):
        self.assertNotEqual(
            len(get_next_question(self.get_redis_client(), 'test_user')), 0
        )
        self.get_redis_client().delete('test_user')


if __name__ == '__main__':
    main()
