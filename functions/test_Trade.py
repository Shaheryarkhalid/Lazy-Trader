from datetime import datetime, timezone
import json
import unittest


from alpaca.trading.enums import OrderSide

from functions.Trade import Trade
from internals.config import Config


class TestTrade(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.config = Config()
        self.trade = Trade(self.config)

    def test_save_trade_locally(self):

        msg = self.trade.save_trade_locally(
            "APPL",
            250,
            OrderSide.SELL,
            200,
            300,
            datetime.now(timezone.utc).isoformat(),
            "Looks good to me.",
        )
        self.assertTrue(msg.startswith("Success"))
        print(msg)

    def test_get_trades_from_db(self):
        trades = self.trade.get_trades_from_db("APPL")
        self.assertFalse(isinstance(trades, str))
        self.assertTrue(isinstance(trades, list))
        print(f"Database: Number of Trades for 'APPL': {len(trades)}")
