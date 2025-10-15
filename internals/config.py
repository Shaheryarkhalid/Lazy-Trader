import os
import sqlite3
from dotenv import load_dotenv


class Config:
    def __init__(self) -> None:
        self.DB_Url = "./trader_db.sql"
        self.DB_Connection = None
        self.AI_Article_Parser_API_Key = None
        self.get_config()
        self.get_db_connection()

    def __exit__(self):
        if self.DB_Connection is not None:
            self.DB_Connection.close()

    def get_config(self):
        load_dotenv()
        self.AI_Article_Parser_API_Key = os.getenv("AI_Article_Parser_API_Key")
        if (
            self.AI_Article_Parser_API_Key == None
            or self.AI_Article_Parser_API_Key == ""
        ):
            raise Exception(
                "Error: couldn't get AI_Article_Parser_API_Key. Please check environment variables."
            )

    def get_db_connection(self):
        con = sqlite3.connect(self.DB_Url)
        if con == None:
            raise Exception(
                "Couldn't connect with db. Please check environment variables."
            )
        else:
            self.DB_Connection = con
