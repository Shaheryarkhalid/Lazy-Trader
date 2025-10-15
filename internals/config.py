import os
from dotenv import load_dotenv


class Config:
    def __init__(self) -> None:
        self.DB_Url = "./trader_db.sql"
        self.AI_Article_Parser_API_Key = None

    def get_config(self):
        load_dotenv()
        self.AI_Article_Parser_API_Key = os.getenv("AI_Article_Parser_API_Key")
        if (
            self.AI_Article_Parser_API_Key == None
            or self.AI_Article_Parser_API_Key == ""
        ):
            return "Error: couldn't get AI_Article_Parser_API_Key. Please check environment variables."
