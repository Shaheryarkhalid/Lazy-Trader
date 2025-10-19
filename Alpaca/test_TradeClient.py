import unittest
from Alpaca.TradeClient import TradeClient
from internals.config import Config


# class TestTradeClient(unittest.TestCase):
#     def __init__(self, methodName: str = "runTest") -> None:
#         super().__init__(methodName)
#         self.config = Config()
#
#     def test_get_all_assets(self):
#         trade_client = TradeClient(self.config)
#         assets = trade_client.get_all_assets()
#         self.assertNotIsInstance(assets, str)
#         self.assertGreater(len(assets), 0)
#         print(assets)
#         print(len(assets))
