import os
import sqlite3
from dotenv import load_dotenv
from helpers import Singleton


@Singleton
class Config:
    def __init__(self) -> None:
        self.DB_Url = None
        self.DB_Connection = None
        self.Context_AI_API_Key = None
        self.Trade_AI_API_Key = None
        self.Alpaca_Stream_Url = None
        self.Alpaca_API_Key_ID = None
        self.Alpaca_API_Key_Secret = None
        self.__get_config()
        self.validate_config()
        self.__get_db_connection()

    def validate_config(self):
        assert self.DB_Url is not None
        assert self.DB_Url != ""

        assert self.Context_AI_API_Key is not None
        assert self.Context_AI_API_Key != ""

        assert self.Trade_AI_API_Key is not None
        assert self.Trade_AI_API_Key != ""

        assert self.Alpaca_API_Key_ID is not None
        assert self.Alpaca_API_Key_ID != ""
        assert self.Alpaca_API_Key_Secret is not None
        assert self.Alpaca_API_Key_Secret != ""
        assert self.Alpaca_Stream_Url is not None
        assert self.Alpaca_Stream_Url != ""

    def __del__(self):
        self.__clean_up()

    def __exit__(self):
        self.__clean_up()

    def __clean_up(self):
        print("Closing Database Connection...")
        if self.DB_Connection is not None:
            self.DB_Connection.close()
            self.DB_Connection = None
        print("Database Connection Closed Successsfully.")

    def __get_config(self):
        load_dotenv()
        self.DB_Url = os.getenv("DB_Url")

        self.Context_AI_API_Key = os.getenv("Context_AI_API_Key")
        self.Trade_AI_API_Key = os.getenv("Trade_AI_API_Key")

        self.Alpaca_API_Key_ID = os.getenv("Alpaca_API_Key_ID")
        self.Alpaca_API_Key_Secret = os.getenv("Alpaca_API_Key_Secret")
        self.Alpaca_Stream_Url = os.getenv("Alpaca_Stream_Url")

    def __get_db_connection(self):
        print("Opening Database Connection...")
        assert self.DB_Url is not None
        con = sqlite3.connect(self.DB_Url)
        assert con is not None
        self.DB_Connection = con
        print("Database Connection Opened Successsfull.")
