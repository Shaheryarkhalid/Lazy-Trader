import unittest

from colorama import Fore, init

from Alpaca.MarketDataClient import MarketDataClient
from internals.Config import Config

init(autoreset=True)


class TestMarketDataClient(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        try:
            super().__init__(methodName)
            self.config = Config()
            self.market_data_client = MarketDataClient()
            self.assertNotEqual(self.config, None)

        except Exception as e:
            print(Fore.RED + f"{e}")
            self.fail("")

    def test_initialization(self):
        try:
            self.assertNotEqual(self.market_data_client.client, None)
        except Exception as e:
            print(Fore.RED + f"{e}")
            self.fail("")

    def test_get_asset_history_week(self):
        try:
            bars = self.market_data_client.get_asset_history_week("GEVX")
            self.assertFalse(isinstance(bars, str))
        except Exception as e:
            print(Fore.RED + f"{e}")
            self.fail("")

    def test_get_asset_price(self):
        try:
            self.market_data_client.get_asset_price("AIXI")
            self.market_data_client.get_asset_price("AAPL")
            self.market_data_client.get_asset_price("SPY")
            self.market_data_client.get_asset_price("OPEN")
            self.market_data_client.get_asset_price("COIN")
            self.market_data_client.get_asset_price("ZZLL")
            self.market_data_client.get_asset_price("OPEN")
            self.market_data_client.get_asset_price("ZZLL")
            self.market_data_client.get_asset_price("ZZLL")
            self.market_data_client.get_asset_price("FAKE")
        except Exception as e:
            print(Fore.RED + f"{e}")
            self.fail("")
