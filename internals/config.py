import os
import sqlite3
from dotenv import load_dotenv


class Config:
    def __init__(self) -> None:
        self.DB_Url = None
        self.DB_Connection = None
        self.AI_Article_Parser_API_Key = None
        self.Alpaca_Stream_Url = None
        self.Alpaca_API_Key_ID = None
        self.Alpaca_API_Key_Secret = None
        self.__get_config()
        self.__validate_config()
        self.__get_db_connection()

    def __exit__(self):
        if self.DB_Connection is not None:
            self.DB_Connection.close()

    def __get_config(self):
        load_dotenv()
        self.AI_Article_Parser_API_Key = os.getenv("AI_Article_Parser_API_Key")
        self.DB_Url = os.getenv("DB_Url")
        self.Alpaca_API_Key_ID = os.getenv("Alpaca_API_Key_ID")
        self.Alpaca_API_Key_Secret = os.getenv("Alpaca_API_Key_Secret")
        self.Alpaca_Stream_Url = os.getenv("Alpaca_Stream_Url")

    def __validate_config(self):
        assert self.AI_Article_Parser_API_Key != None
        assert self.AI_Article_Parser_API_Key != ""
        assert self.DB_Url != None
        assert self.DB_Url != ""
        assert self.Alpaca_API_Key_ID != None
        assert self.Alpaca_API_Key_ID != ""
        assert self.Alpaca_API_Key_Secret != None
        assert self.Alpaca_API_Key_Secret != ""
        assert self.Alpaca_Stream_Url != None
        assert self.Alpaca_Stream_Url != ""

    def __get_db_connection(self):
        con = sqlite3.connect(self.DB_Url)
        if con == None:
            raise Exception(
                "Couldn't connect with db. Please check environment variables."
            )
        else:
            self.DB_Connection = con
