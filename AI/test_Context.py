import unittest
from AI.Context import Context
from internals.config import Config


class TestContext(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.context = None
        self.initialize_context_chat_client()

    def initialize_context_chat_client(self):
        config = Config()
        self.assertNotEqual(config.Context_AI_API_Key, None)
        self.assertNotEqual(config.Context_AI_API_Key, "")
        context = Context(config)
        self.assertNotEqual(context.ChatClient, None)
        self.context = context

    def test_get_context(self):
        self.assertIsNotNone(self.context)
        assert self.context is not None
        resp = self.context.get_context()
        assert resp is not None
        self.assertFalse(resp.startswith("Error: "))
        print(f"Context AI Response: {resp[:100]}...")
