from google import genai
from Constants import CONTEXT_AI_SYSTEM_PROMPT


class Context:

    def __init__(self, config) -> None:
        self.config = config
        self.config.validate_config()
        self.ChatClient = None
        self.__initialize_chat_client()
        assert self.ChatClient != None

    def get_context(self):
        try:
            assert self.ChatClient != None
            resp = self.ChatClient.models.generate_content(
                model="gemini-2.0-flash",
                contents=genai.types.Part.from_text(text=CONTEXT_AI_SYSTEM_PROMPT),
            )
            print(resp.text)
        except Exception as e:
            print(e)

    def __initialize_chat_client(self):
        print("Initializing AI Context Client...")
        try:
            chat_client = genai.Client(api_key=self.config.Context_AI_API_Key)
            models = chat_client.models.list()
            if len(models) < 1:
                print(
                    "Error: Unable to create genai.client. Please check your environment variables or your internet connection."
                )
                self.ChatClient = None
                return
            self.ChatClient = chat_client
            print("Context Client Successfully initialized.")
        except Exception as e:
            self.ChatClient = None
            print(
                "Error: Something went wrong while trying to initialize AI Context Client. Most likely API Key or  Network Error."
            )
            print(e)
