import unittest
from AI.Context import Context
from colorama import Fore, init

init(autoreset=True)


class TestContext(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        try:
            super().__init__(methodName)
            self.context = None
            self.initialize_context_chat_client()
        except Exception as e:
            print(Fore.RED + f"{e}")
            self.fail("")

    def initialize_context_chat_client(self):
        try:
            context = Context()
            self.assertNotEqual(context.ChatClient, None)
            self.context = context
        except Exception as e:
            print(Fore.RED + f"{e}")
            self.fail("")

    def test_get_context(self):
        try:
            self.assertIsNotNone(self.context)
            assert self.context is not None
            resp = self.context.get_context()
            assert resp is not None
            self.assertFalse(resp.startswith("Error: "))
            print(f"Context AI Response: {resp[:100]}...")
        except Exception as e:
            print(Fore.RED + f"{e}")
            self.fail("")
