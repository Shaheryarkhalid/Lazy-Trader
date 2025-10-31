import asyncio
import sys

from colorama import Fore
from AI.Context import Context
from AI.TradeAgent import TradeAgent
from Alpaca.MarketDataClient import MarketDataClient
from Alpaca.NewsClient import NewsClient
from Alpaca.TradeClient import TradeClient
from internals.Config import Config
from helpers import Logger


async def main():
    sys.stdout = Logger("output.log")
    Config()
    Context()
    MarketDataClient()
    TradeClient()
    trade_agent = TradeAgent()
    news_client = NewsClient()

    await news_client.run()
    assert news_client.connection is not None

    while True:
        try:
            print(Fore.LIGHTWHITE_EX + "⏳ Waiting for news article...")
            assert news_client.connection is not None
            data = await news_client.connection.recv()
            asyncio.create_task(trade_agent.trade(article=f"{data}"))
        except Exception as e:
            print(Fore.RED + f"🔴 Something went wrong: \n Error: {e}")
            print(Fore.WHITE + "Restarting News Client...")
            news_client = NewsClient()
            await news_client.run()


if __name__ == "__main__":
    asyncio.run(main())
