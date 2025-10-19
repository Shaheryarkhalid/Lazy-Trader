import asyncio
import json
import unittest
from internals.config import Config
from Alpaca.NewsClient import NewsClient


class TestNewsClient(unittest.TestCase):

    def test_init(self):
        config = Config()
        asyncio.run(self.__run_news_client(config))

    async def __run_news_client(self, config):
        news_client = NewsClient(config)
        await news_client.run()
        self.assertNotEqual(news_client.connection, None)
        assert news_client.connection != None
        while True:
            data = await news_client.connection.recv()
            print(data)
