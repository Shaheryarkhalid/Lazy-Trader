import feedparser
import time
import random
from urllib import request
from bs4 import BeautifulSoup
from google import genai


class RssFeed:
    def __init__(self, source, url, config) -> None:
        self.source = source
        self.url = url
        self.feed = []
        self.config = config

    def __get_random_user_agent(self):
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.90 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.137 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
            "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.15 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 13; SM-S926B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.65 Mobile Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/129.0.6668.90 Safari/537.36",
            "curl/8.4.0",
            "PostmanRuntime/7.39.0",
            "python-requests/2.32.3",
            "httpx/0.27.0",
        ]
        return {
            "User-Agent": random.choice(user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }

    def __get_full_article(self, url):
        try:
            req = request.Request(url=url, headers=self.__get_random_user_agent())
            resp = request.urlopen(req)
            html_parser = BeautifulSoup(resp, "html.parser")
            for tag in html_parser(["style", "script"]):
                tag.decompose()
        except Exception as e:
            return f"Error: Unable to get article: {e}"
        return html_parser.get_text()

    def __parse_article(self, full_article):
        llm_resp = None
        try:
            if (
                self.config.AI_Article_Parser_API_Key == None
                or self.config.AI_Article_Parser_API_Key == ""
            ):
                return "Error: Unable to get API Key for the LLM. Please check you environment variables."
            llm_client = genai.Client(api_key=self.config.AI_Article_Parser_API_Key)
            llm_config = genai.types.GenerateContentConfig(
                system_instruction="You will be given article that has been parsed from html which will include some unrelated text, ignore that and parse only the text that is article or related to article, just the article and then write a one paragraph of decent size paragraph of summary of that article. Please make sure to include all of the details as these details are very important and don't make up stuff on your own. Only return the summary of the article donot return any thing else nothing at all.",
            )
            llm_resp = llm_client.models.generate_content(
                model="gemini-2.0-flash",
                contents=genai.types.Part.from_text(text=full_article),
                config=llm_config,
            )
        except Exception as e:
            return f"Error: Trying to parse article:\n{e}"
        return llm_resp.text

    def __save_feed(self, title, source, url, description, published_at):
        try:
            db_con = self.config.DB_Connection
            if db_con == None:
                return "Error: Unable to get database connection."
            cursor = db_con.cursor()
            cursor.execute(
                "insert into RSSFeed(Title, Url, Source, PublishDate, Summary) values(?, ?, ?, ?, ?)",
                (title, url, source, published_at, description),
            )
            db_con.commit()
        except Exception as e:
            return f"Error: Trying to save feeds list to db:\n{e}"

    def get_feed(self):
        try:
            feed = feedparser.parse(self.url)
            for entry in feed.entries:
                description = ""
                try:
                    description = (
                        entry.description if entry.description else entry.summary
                    )
                except Exception as e:
                    print("")
                full_article = self.__get_full_article(entry.link)
                if full_article.startswith("Error:"):
                    print(full_article)
                else:
                    summary = self.__parse_article(full_article)
                    if summary.startswith("Error:"):
                        print(summary)
                    else:
                        description = summary
                self.feed.append(
                    {
                        "title": entry.title,
                        "description": description,
                        "url": entry.link,
                        "soruce": self.source,
                        "published_at": entry.published,
                    }
                )
                err = self.__save_feed(
                    entry.title, self.source, entry.link, description, entry.published
                )
                if err is not None:
                    print(err)
                print(f"Saved Article: {entry.title}")
                time.sleep(5)
        except Exception as e:
            return f"Error: Trying to get feed:\n{e}"
