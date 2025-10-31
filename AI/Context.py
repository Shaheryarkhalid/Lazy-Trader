from google import genai
from Constants import CONTEXT_AI_SYSTEM_PROMPT
from helpers import Singleton
from internals.Config import Config
from colorama import Fore


@Singleton
class Context:

    def __init__(self) -> None:
        self.config = Config()
        self.config.validate_config()
        self.ChatClient = None
        self.__initialize_chat_client()
        assert self.ChatClient is not None

    def get_context(self):
        try:
            assert self.ChatClient is not None
            resp = self.ChatClient.models.generate_content(
                model="gemini-2.0-flash",
                contents=genai.types.Part.from_text(text=CONTEXT_AI_SYSTEM_PROMPT),
            )
            return resp.text
        except Exception as e:
            return Fore.RED + f"🔴 Error: Trying to get response from LLM.\n{e}"

    def __initialize_chat_client(self):
        print(Fore.LIGHTWHITE_EX + "⏳Initializing AI Context Client...")
        try:
            chat_client = genai.Client(api_key=self.config.Context_AI_API_Key)
            models = chat_client.models.list()
            if len(models) < 1:
                print(
                    Fore.RED
                    + "🔴 Error: Unable to create genai.client. Please check your environment variables or your internet connection."
                )
                self.ChatClient = None
                return
            self.ChatClient = chat_client
            print(Fore.GREEN + "🟢 Context Client Successfully initialized.")
            return
        except Exception as e:
            self.ChatClient = None
            print(
                Fore.RED
                + "🔴 Error: Something went wrong while trying to initialize AI Context Client. Most likely API Key or  Network Error."
            )
            print(Fore.RED + str(e))
            return
