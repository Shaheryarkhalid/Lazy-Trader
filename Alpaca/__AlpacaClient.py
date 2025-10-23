from alpaca.trading.client import TradingClient
from helpers import Singleton


@Singleton
class AlpacaClient:
    def __init__(self, config) -> None:
        self.config = config
        self.config.validate_config()

        self.client = None
        self.__initialize()
        assert self.client != None

    def __initialize(self):
        print("Initializing Alpaca Client...")
        try:
            self.client = TradingClient(
                self.config.Alpaca_API_Key_ID, self.config.Alpaca_API_Key_Secret
            )
            account = self.client.get_account()
            print(
                "Successfully connected to alpaca client. account status: ",
                account.status,
            )
            return
        except Exception as e:
            print("Unable to establish connection to Alpaca Client.")
            print(e)
            self.client = None
