import json
from typing import ForwardRef
from google import genai
from google.genai import types
from Alpaca.TradeClient import TradeClient
from Alpaca.MarketDataClient import MarketDataClient
from functions.Trade import Trade
from helpers import Singleton
from Constants import TRADE_AI_SYSTEM_PROMPT, TRADE_AI_SYSTEM_PROMPT_REMINDER
from colorama import Fore, init

from AI.Context import Context
from internals.Config import Config

init(autoreset=True)


@Singleton
class TradeAgent:

    def __init__(self) -> None:
        try:
            self.Config = Config()
            self.Config.validate_config()
            assert self.Config is not None

            self.Context = Context()
            self.TradeClient = TradeClient()
            self.MarketDataClient = MarketDataClient()
            self.TradeDBClient = Trade()

            self.ChatClient = None
            self.__initialize()
            assert self.ChatClient is not None

            self.available_functions = self.__get_available_functions()
            assert isinstance(self.available_functions, types.Tool)
            assert self.available_functions.function_declarations is not None
            assert len(self.available_functions.function_declarations) > 0

            self.trade_agent_config = types.GenerateContentConfig(
                system_instruction=TRADE_AI_SYSTEM_PROMPT,
                tools=[self.available_functions],
            )
        except Exception as e:
            print(Fore.RED + f"{e}")
            exit(1)

    async def trade(self, article):
        news_data = json.loads(article)
        print(Fore.WHITE + f"💬 Article: {news_data[0]['headline']}")
        messages = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=str(article))],
            )
        ]
        assert self.ChatClient is not None
        try:
            while True:
                resp = self.ChatClient.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=messages,
                    config=self.trade_agent_config,
                )
                if not resp.candidates:
                    print(Fore.GREEN + "🟢 Task has been finished.")
                    return
                candidate = resp.candidates[0]
                part = candidate.content.parts[0]
                messages += [types.ModelContent(parts=candidate.content.parts)]

                text = part.text if hasattr(part, "text") else None
                function_call = (
                    part.function_call if hasattr(part, "function_call") else None
                )

                if not text and not function_call:
                    print(Fore.GREEN + "🟢 Task has been finished.")
                    return

                if text:
                    messages += [
                        types.UserContent(
                            parts=types.Part.from_text(
                                text=TRADE_AI_SYSTEM_PROMPT_REMINDER
                            )
                        )
                    ]
                    continue
                if function_call:
                    try:
                        function_call_response = self.__call_function(function_call)
                        messages += [
                            types.UserContent(
                                parts=[
                                    types.Part.from_text(text=function_call_response)
                                ]
                            )
                        ]
                    except Exception as e:
                        print(
                            Fore.RED + f"🔴 Error while trying to call function: \n{e}"
                        )
                        messages += [
                            types.Content(
                                role="Tool",
                                parts=[
                                    types.Part.from_function_response(
                                        name=function_call.name,
                                        response={"error": e},
                                    )
                                ],
                            )
                        ]

        except Exception as e:
            return (
                f"🔴 Error: Trying to get response from Trade Agent Chat Client.\n{e}"
            )

    def __initialize(self):
        print(Fore.LIGHTWHITE_EX + "⏳ Initializing Trade Agent Chat Client...")
        try:
            chat_client = genai.Client(api_key=self.Config.Trade_AI_API_Key)
            models = chat_client.models.list()
            if len(models) < 1:
                print(
                    Fore.RED
                    + "🔴 Error: Unable to create genai.client. Please check your environment variables or your internet connection."
                )
                self.ChatClient = None
                return
            self.ChatClient = chat_client
            print(Fore.GREEN + "🟢 Trade Agent Chat Client Successfully initialized.")
            return
        except Exception as e:
            self.ChatClient = None
            print(
                Fore.RED
                + "🔴 Error: Something went wrong while trying to initialize Trade Agent Chat Client. Most likely API Key or  Network Error."
            )
            print(e)
            return

    def __get_available_functions(self):

        get_context = types.FunctionDeclaration(
            name="get_context",
            description="Will give you Context(What is happening arround the world, stock market codition, political landscape, and other important data related to the current state of the world).",
        )

        get_available_assets = types.FunctionDeclaration(
            name="get_available_assets",
            description="Will give you list of all available assets to trade(Only includes in US Market).",
        )

        get_asset_price = types.FunctionDeclaration(
            name="get_asset_price",
            description="Will give you the latest price of the given asset.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "symbol": types.Schema(
                        type=types.Type.STRING,
                        description="symbol of the asset for which price will be returned.",
                    )
                },
            ),
        )

        get_asset_history_week = types.FunctionDeclaration(
            name="get_asset_history_week",
            description="Will give you past week's performance of given stock.).",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "symbol": types.Schema(
                        type=types.Type.STRING,
                        description="symbol of the asset for which performance will be returned. You will get this symbol from get_available_assets function.",
                    )
                },
            ),
        )

        get_older_bets = types.FunctionDeclaration(
            name="get_older_bets",
            description="Will give you older bets for given symbol. And will also provide you the reason why you made this decision.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "symbol": types.Schema(
                        type=types.Type.STRING,
                        description="symbol of the asset for which older bets will be returned. You will get this symbol from get_available_assets function.",
                    )
                },
            ),
        )

        make_trade = types.FunctionDeclaration(
            name="make_trade",
            description="Will make a trade based on your given parameters. This trade will automatically be closed after 24 hours. If make_trade function reutrns error with base_price use that base price as asset price and adjust profit and stop_loss accordingly.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "symbol": types.Schema(
                        type=types.Type.STRING,
                        description="symbol of the asset for which trade will be placed.",
                    ),
                    "qty": types.Schema(
                        type=types.Type.INTEGER,
                        description="No of stocks to buy.",
                    ),
                    "side": types.Schema(
                        type=types.Type.STRING,
                        description="What kind of trade to place. 'BUY' or 'SELL'. ",
                    ),
                    "profit": types.Schema(
                        type=types.Type.INTEGER,
                        description="At which price to stop the trade if profitable. if side is 'BUY' then it will be greater than current price, if side is 'SELL' then it will be lower than current price of asset.",
                    ),
                    "stop_loss": types.Schema(
                        type=types.Type.INTEGER,
                        description="At which price to stop the trade if not profitable. if side is 'BUY' then it will be less than current price , if side is 'SELL' then it will be greater than current price of asset. ",
                    ),
                },
            ),
        )
        save_trade_locally = types.FunctionDeclaration(
            name="save_trade_locally",
            description="Will save a local copy of trade which will be used as context later it will also include the reason behind the trade.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "trade_id": types.Schema(
                        type=types.Type.STRING,
                        description="id of the trade.",
                    ),
                    "symbol": types.Schema(
                        type=types.Type.STRING,
                        description="symbol of the asset for which trade will be placed.",
                    ),
                    "price": types.Schema(
                        type=types.Type.INTEGER,
                        description="current price at which trade is made.",
                    ),
                    "position": types.Schema(
                        type=types.Type.STRING,
                        description="What kind of trade is placed. 'BUY' or 'SELL'. ",
                    ),
                    "profit_limit": types.Schema(
                        type=types.Type.INTEGER,
                        description="At which price to stop the trade if profitable. greater than current price if buy, less than current price if sell",
                    ),
                    "stop_loss": types.Schema(
                        type=types.Type.INTEGER,
                        description="At which price to stop the trade if not profitable. less than current price if buy, greater than current price if sell",
                    ),
                    "reason": types.Schema(
                        type=types.Type.INTEGER,
                        description="What is the reason behind the trade. Must only be one paragraph long short one.",
                    ),
                },
            ),
        )

        available_functions = types.Tool(
            function_declarations=[
                get_context,
                get_available_assets,
                get_asset_price,
                get_asset_history_week,
                get_older_bets,
                make_trade,
                save_trade_locally,
            ]
        )
        return available_functions

    def __call_function(self, function_call_part):
        functions = {
            "get_context": self.Context.get_context,
            "get_available_assets": self.TradeClient.get_all_assets,
            "get_asset_price": self.MarketDataClient.get_asset_price,
            "get_asset_history_week": self.MarketDataClient.get_asset_history_week,
            "get_older_bets": self.TradeClient.get_active_trades_for_asset,
            "make_trade": self.TradeClient.make_trade,
            "save_trade_locally": self.TradeDBClient.save_trade_locally,
        }
        if not functions[function_call_part.name]:
            return types.Content(
                role="Tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={
                            "error": f"Unknown function: {function_call_part.name}"
                        },
                    )
                ],
            )
        print(
            Fore.LIGHTWHITE_EX
            + f"🛠️ Calling function: {function_call_part.name} Args : f{function_call_part.args}"
        )
        try:
            resp = functions[function_call_part.name](**function_call_part.args)
            return f"{resp}"
        except Exception as e:
            return f"Error: {e}"
