import websockets
import json

from helpers import Singleton


@Singleton
class NewsClient:
    def __init__(self, config) -> None:
        self.config = config
        self.connection = None
        self.is_authenticated = False
        self.is_subscribed = False
        self.config.validate_config()

    async def run(self):
        await self.__connect_alpaca()
        await self.__authenticate_alpaca()
        await self.__subscribe_alpaca_news()
        self.__validate_instance()

    def __validate_instance(self):
        assert self.connection != None
        assert self.is_authenticated != False
        assert self.is_subscribed != False

    async def __connect_alpaca(self):
        try:
            print("Connecting to Alpaca News Stream...")
            alpaca_connection = await websockets.connect(self.config.Alpaca_Stream_Url)
            data = await alpaca_connection.recv()
            events = json.loads(data)
            if events[0].get("T") == "success":
                print(f"Connection Succcessfull. {data}")
                self.connection = alpaca_connection
                return
            else:
                self.connection = None
                print("Error: Unable to connect to alpaca news stream url.")
                print(data)
                return

        except Exception as e:
            self.connection = None
            print("Error: Unable to connect to alpaca news stream url.")
            print(e)
            return

    async def __authenticate_alpaca(self):
        try:
            assert self.connection != None
            print("Authenticating Alpaca News Client...")
            auth_msg = {
                "action": "auth",
                "key": self.config.Alpaca_API_Key_ID,
                "secret": self.config.Alpaca_API_Key_Secret,
            }
            await self.connection.send(json.dumps(auth_msg))
            data = await self.connection.recv()
            events = json.loads(data)
            if (
                events[0].get("T") == "success"
                and events[0].get("msg") == "authenticated"
            ):
                print(f"Authentication Successfull.{data}")
                self.is_authenticated = True
                return
            else:
                print(f"Unable to Authenticate. {data}")
                await self.connection.close()
                self.connection = None
                self.is_authenticated = False
                return
        except Exception as e:
            print("Unable to Authenticate.")
            print(e)
            assert self.connection != None
            await self.connection.close()
            self.connection = None
            self.is_authenticated = False
            return

    async def __subscribe_alpaca_news(self):
        try:
            assert self.connection != None
            assert self.is_authenticated == True
            print("Subscribing to Alpaca News Client...")
            sub_msg = {"action": "subscribe", "news": ["*"]}
            await self.connection.send(json.dumps(sub_msg))
            data = await self.connection.recv()
            events = json.loads(data)
            if events[0].get("T") == "subscription":
                print(f"Succcessfully subscribed to the Alpaca News Stream.{data}")
                self.is_subscribed = True
                return
            else:
                print(f"Unable to subscribe to alpaca news. {data}")
                assert self.connection != None
                await self.connection.close()
                self.connection = None
                self.is_authenticated = False
                self.is_subscribed = False
        except Exception as e:
            print("Unable to subscribe to alpaca news.")
            print(e)
            assert self.connection != None
            await self.connection.close()
            self.connection = None
            self.is_authenticated = False
            self.is_subscribed = False
