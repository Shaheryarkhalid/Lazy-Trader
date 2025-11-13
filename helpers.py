import sys
import re
from datetime import datetime
from colorama import Fore, init

init(autoreset=True)


def Singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


class Logger(object):

    def __init__(self, file_name) -> None:
        self.terminal = sys.stdout
        self.log = open(file_name, "a")
        self.log.write(
            "------------------------------------------------- New Instance -------------------------------------------------\n"
        )

    def __exit__(self):
        self.log.close()

    def __del__(self):
        self.log.close()

    def write(self, message):
        time_stamp = datetime.now()
        if message != "\n":
            message = f"{Fore.LIGHTWHITE_EX }{time_stamp}:  {message}"
        self.terminal.write(message)
        plain_message = re.sub(r"\x1B\[[0-?]*[ -/]*[@-~]", "", message)
        self.log.write(plain_message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()
