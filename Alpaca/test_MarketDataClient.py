import unittest

from Alpaca.MarketDataClient import MarketDataClient
from internals.Config import Config


class TestMarketDataClient(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.config = Config()
        self.market_data_client = MarketDataClient()
        self.assertNotEqual(self.config, None)

    def test_initialization(self):
        self.assertNotEqual(self.market_data_client.client, None)

    def test_get_asset_history_week(self):
        bars = self.market_data_client.get_asset_history_week("GEVX")
        self.assertFalse(isinstance(bars, str))

    def test_get_asset_price(self):
        price = self.market_data_client.get_asset_price("AIXI")
        print("--------------------------------------------------------------")
        print(price)
        print("--------------------------------------------------------------")
