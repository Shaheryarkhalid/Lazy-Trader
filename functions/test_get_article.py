import unittest
from functions.get_atricle import get_article
from internals.config import Config


class TestGetArticle(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.config = Config()

    def test_get_article(self):
        article = get_article(self.config)
        print(article)
