import asyncio
import unittest
from internals.Config import Config
from Alpaca.NewsClient import NewsClient


class TestNewsClient(unittest.TestCase):

    def test_init(self):
        config = Config()
        asyncio.run(self.__run_news_client(config))

    async def __run_news_client(
        self,
    ):
        news_client = NewsClient()
        try:
            await news_client.run()
            self.assertNotEqual(news_client.connection, None)
            self.assertNotEqual(news_client.is_authenticated, False)
            self.assertNotEqual(news_client.is_subscribed, False)
        finally:
            await news_client.close()
