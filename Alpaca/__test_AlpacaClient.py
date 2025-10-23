import unittest
import asyncio
from internals.config import Config
from Alpaca.AlpacaClient import AlpacaClient


class TestAlpacaClient(unittest.TestCase):
    pass

    # def test_init(self):
    #     config = Config()
    #     asyncio.run(self.__run_news_client(config))
    #
    # async def __run_news_client(self, config):
    #     alpaca_client = AlpacaClient(config)
    #     assert alpaca_client != None
    #     self.assertNotEqual(alpaca_client.client, None)
