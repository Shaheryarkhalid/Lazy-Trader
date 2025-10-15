import unittest
import sqlite3
from RssFeed import RssFeed
from internals.config import Config


class TestRssFeed(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.config = Config()
        err = self.config.get_config()
        if err is not None and err.startswith("Error:"):
            self.fail(f"Unable to get Config: \n{err}")

    def __get_rss_feed_sources(self):
        conn = sqlite3.connect(self.config.DB_Url)
        cursor = conn.execute("Select * from RSSFeedSources;")
        sources = cursor.fetchall()
        pass

    def test_single_RssFeed(self):
        if self.config == None:
            self.fail("Config not found")
        rss_feed = RssFeed(
            "Market Watch",
            "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114",
            self.config,
        )
        err = rss_feed.get_feed()
        if err is not None:
            self.fail(f"{err}")

    def test_all_RssFeeds_from_sources(self):
        pass
