import unittest
from AI.TradeAgent import TradeAgent
from internals.Config import Config


class TestTradeAgent(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.config = Config()
        self.trade_agent = TradeAgent()
        assert self.trade_agent is not None
        assert self.trade_agent.ChatClient is not None

    def test_trade(self):
        try:
            assert self.trade_agent is not None
            assert self.trade_agent.ChatClient is not None
            text = self.trade_agent.trade(
                """

                                        Tech Startup Launches AI-Powered Study App
October 26, 2025

A new educational technology startup, LearnSmart, has unveiled an AI-powered study app designed to help students improve learning efficiency. The app uses adaptive algorithms to create personalized study plans, track progress, and provide real-time feedback.

According to the company, early beta testers reported a 30% increase in retention rates compared to traditional study methods. LearnSmart plans to roll out the app nationwide next month, aiming to make AI-driven learning accessible to students of all ages.

Education experts say the app represents a growing trend of AI integration in classrooms, though they caution that technology should complement, not replace, traditional teaching methods.

                                        """
            )
            print(text)
            print(f"Trade AI Agent Response: {text}...")

        except Exception as e:
            self.fail(e)
