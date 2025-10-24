import unittest
import sqlite3
from RssFeed import RssFeed
from internals.Config import Config


class TestRssFeed(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.config = Config()

    def __get_rss_feed_sources(self):
        conn = sqlite3.connect(self.config.DB_Url)
        cursor = conn.execute("Select * from RSSFeedSources;")
        sources = cursor.fetchall()
        if len(sources) < 1:
            self.fail("Unable to get Feed Sources from db.")
        conn.close()
        return sources

    def test_single_RssFeed(self):
        if (
            self.config.AI_Article_Parser_API_Key is None
            or self.config.DB_Connection is None
        ):
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
        if (
            self.config.AI_Article_Parser_API_Key is None
            or self.config.DB_Connection is None
        ):
            self.fail("Config not found")

        sources = self.__get_rss_feed_sources()
        for source in sources:
            rss_feed = RssFeed(
                source[1],
                source[2],
                self.config,
            )
            err = rss_feed.get_feed()
            if err is not None:
                self.fail(f"{err}")
