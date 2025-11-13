from colorama import Fore, init
import websockets
import json

from helpers import Singleton
from internals.Config import Config

init(autoreset=True)


@Singleton
class NewsClient:
    def __init__(self) -> None:
        try:
            self.config = Config()
            self.connection = None
            self.is_authenticated = False
            self.is_subscribed = False
            self.config.validate_config()
        except Exception as e:
            print(Fore.RED + f"{e}")

    async def run(self):
        try:
            await self.__connect_alpaca()
            await self.__authenticate_alpaca()
            await self.__subscribe_alpaca_news()
            self.__validate_instance()
        except Exception as e:
            print(Fore.RED + f"{e}")
            exit(1)

    async def __exit__(self):
        await self.close()

    async def close(self):
        try:
            if self.connection:
                if hasattr(self.connection, "close"):
                    print(Fore.LIGHTWHITE_EX + "⏳ Closing Alpaca News Stream...")
                    await self.connection.close()
                    if self.connection.close_code:
                        print(Fore.GREEN + "🟢 Alpaca News Stream Closed Successfully.")
        except Exception as e:
            print(Fore.RED + f"🔴 {e}")

    def __validate_instance(self):
        assert self.connection is not None
        assert self.is_authenticated is not False
        assert self.is_subscribed is not False

    async def __connect_alpaca(self):
        try:
            print(Fore.LIGHTWHITE_EX + "⏳ Connecting to Alpaca News Stream...")
            assert self.config.Alpaca_Stream_Url is not None
            alpaca_connection = await websockets.connect(self.config.Alpaca_Stream_Url)
            data = await alpaca_connection.recv()
            events = json.loads(data)
            if events[0].get("T") == "success":
                print(Fore.GREEN + f"🟢 Connection Succcessfull. {data}")
                self.connection = alpaca_connection
                return
            else:
                self.connection = None
                print(
                    Fore.RED + "🔴 Error: Unable to connect to alpaca news stream url."
                )
                print(data)
                return

        except Exception as e:
            self.connection = None
            print(Fore.RED + "🔴 Error: Unable to connect to alpaca news stream url.")
            print(Fore.RED + str(e))
            return

    async def __authenticate_alpaca(self):
        try:
            assert self.connection is not None
            print(Fore.LIGHTWHITE_EX + "⏳ Authenticating Alpaca News Client...")
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
                print(Fore.GREEN + f"🟢 Authentication Successfull.{data}")
                self.is_authenticated = True
                return
            else:
                print(Fore.RED + f"🔴 Unable to Authenticate. {data}")
                await self.connection.close()
                self.connection = None
                self.is_authenticated = False
                return
        except Exception as e:
            print(Fore.RED + "🔴 Unable to Authenticate.")
            print(Fore.RED + str(e))
            assert self.connection is not None
            await self.connection.close()
            self.connection = None
            self.is_authenticated = False
            return

    async def __subscribe_alpaca_news(self):
        try:
            assert self.connection is not None
            assert self.is_authenticated is True
            print(Fore.LIGHTWHITE_EX + "⏳ Subscribing to Alpaca News Client...")
            sub_msg = {"action": "subscribe", "news": ["*"]}
            await self.connection.send(json.dumps(sub_msg))
            data = await self.connection.recv()
            events = json.loads(data)
            if events[0].get("T") == "subscription":
                print(
                    Fore.GREEN
                    + f"🟢 Succcessfully subscribed to the Alpaca News Stream.{data}"
                )
                self.is_subscribed = True
                return
            else:
                print(Fore.RED + f"🔴 Unable to subscribe to alpaca news. {data}")
                assert self.connection is not None
                await self.connection.close()
                self.connection = None
                self.is_authenticated = False
                self.is_subscribed = False
        except Exception as e:
            print(Fore.RED + "🔴 Unable to subscribe to alpaca news.")
            print(Fore.RED + str(e))
            assert self.connection is not None
            await self.connection.close()
            self.connection = None
            self.is_authenticated = False
            self.is_subscribed = False
