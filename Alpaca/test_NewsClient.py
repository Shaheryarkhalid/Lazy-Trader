import asyncio
import unittest

from colorama import Fore, init
from Alpaca.NewsClient import NewsClient

init(autoreset=True)


class TestNewsClient(unittest.TestCase):

    def test_init(self):
        try:
            asyncio.run(self.__run_news_client())
        except Exception as e:
            print(Fore.RED + f"{e}")
            self.fail("")

    async def __run_news_client(
        self,
    ):
        news_client = NewsClient()
        try:
            await news_client.run()
            self.assertNotEqual(news_client.connection, None)
            self.assertNotEqual(news_client.is_authenticated, False)
            self.assertNotEqual(news_client.is_subscribed, False)
        except Exception as e:
            print(Fore.RED + f"{e}")
            self.fail("")
        finally:
            await news_client.close()
