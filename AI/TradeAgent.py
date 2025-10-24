from typing import Type
from google import genai
from google.genai import types
from helpers import Singleton
from Constants import TRADE_AI_SYSTEM_PROMPT


@Singleton
class TradeAgent:

    def __init__(self, config) -> None:
        self.config = config
        self.config.validate_config()
        assert self.config is not None

        self.ChatClient = None
        self.__initialize()
        assert self.ChatClient is not None

        self.available_functions = self.__get_available_functions()
        assert isinstance(self.available_functions, types.Tool)
        assert self.available_functions.function_declarations is not None
        assert len(self.available_functions.function_declarations) > 0

        self.trade_agent_config = types.GenerateContentConfig(
            system_instruction=TRADE_AI_SYSTEM_PROMPT, tools=[self.available_functions]
        )

    def run(self):
        try:
            assert self.ChatClient is not None
            resp = self.ChatClient.models.generate_content(
                model="gemini-2.0-flash",
                contents=genai.types.Part.from_text(text="Hi, How are you."),
            )
            return resp.text
        except Exception as e:
            return f"Error: Trying to get response from Trade Agent Chat Client.\n{e}"

    def __initialize(self):
        print("Initializing Trade Agent Chat Client...")
        try:
            chat_client = genai.Client(api_key=self.config.Trade_AI_API_Key)
            models = chat_client.models.list()
            if len(models) < 1:
                print(
                    "Error: Unable to create genai.client. Please check your environment variables or your internet connection."
                )
                self.ChatClient = None
                return
            self.ChatClient = chat_client
            print("Trade Agent Chat Client Successfully initialized.")
            return
        except Exception as e:
            self.ChatClient = None
            print(
                "Error: Something went wrong while trying to initialize Trade Agent Chat Client. Most likely API Key or  Network Error."
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
                        description="symbol of the asset for which price will be returned. You will get this symbol from get_available_assets function.",
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
            description="Will make a trade based on your given parameters. This trade will automatically be closed after 24 hours.",
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
                        description="At which price to stop the trade if profitable. greater than current price if buy, less than current price if sell",
                    ),
                    "stop_loss": types.Schema(
                        type=types.Type.INTEGER,
                        description="At which price to stop the trade if not profitable. less than current price if buy, greater than current price if sell",
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
