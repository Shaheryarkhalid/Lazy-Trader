import unittest
from AI.TradeAgent import TradeAgent
from internals.Config import Config


class TestTradeAgent(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.config = Config()
        self.trade_agent = TradeAgent(self.config)
        assert self.trade_agent is not None
        assert self.trade_agent.ChatClient is not None

    def test_run(self):
        try:
            assert self.trade_agent is not None
            assert self.trade_agent.ChatClient is not None
            text = self.trade_agent.run()
            self.assertFalse(text.startswith("Error"))
            print(f"Trade AI Agent Response: {text[:100]}...")

        except Exception as e:
            self.fail(e)
