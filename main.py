import asyncio
import sys

from colorama import Fore
import websockets
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

    async def reconnect_news_client():
        print(Fore.WHITE + "News Client: Reconnecting...")
        nonlocal news_client
        if news_client.connection:
            await news_client.connection.close()
        news_client = NewsClient()
        await news_client.run()

    while True:
        try:
            print(Fore.LIGHTWHITE_EX + "⏳ Waiting for news article...")
            assert news_client.connection is not None
            data = await news_client.connection.recv()
            asyncio.create_task(trade_agent.trade(article=data))
        except websockets.exceptions.ConnectionClosedOK:
            print("🔌 News Client: Connection closed cleanly by server.")
            await reconnect_news_client()
        except websockets.exceptions.ConcurrencyError:
            print("⚠️ News Client: Connection lost unexpectedly.")
            await reconnect_news_client()
        except Exception as e:
            print(Fore.RED + f"🔴 NewsClient: Unexpected Error: \n Error: {e}")
            await reconnect_news_client()


if __name__ == "__main__":
    asyncio.run(main())
