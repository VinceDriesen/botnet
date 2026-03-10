from trello import TrelloClient
import platform
import uuid
import os
from src.command import Command
from src.schedular import Schedular
from src.status_updater import StatusUpdater
# Nieuwe token aanvragen: https://trello.com/1/authorize?expiration=1day&scope=read,write&response_type=token&key=31ec916f741962caeb3b4d2ca1fd43b7

api = "31ec916f741962caeb3b4d2ca1fd43b7"
token = "ATTAecf5ece5c6ab2fa61dbe09bf6e78c1761b5b6096bb45e104163e3b540a9d91e6E8A7D5FF"

board_id = "8Gjc8fX8"
status_list_id = "69a946c9af7564bacbed187d"
command_list_id = "69a946cd58f076e0489335cb"
payload_list_id = "69a957e9099ba7c6167a878a"

client = TrelloClient(
    api_key=api,
    api_secret=token,
)

board = client.get_board(board_id=board_id)
status_list = board.get_list(status_list_id)
command_list = board.get_list(command_list_id)
payload_list = board.get_list(payload_list_id)


def _get_unique_id() -> str:
    if platform.system() == "Linux":
        if os.path.exists("/etc/machine-id"):
            with open("/etc/machine-id", "r") as f:
                return f.read().strip()
    return hex(uuid.getnode())


def main():
    unique_id = _get_unique_id()
    status_updater = StatusUpdater(unique_id, status_list)
    status_updater.update_or_announce()
    commands = Command(command_list)
    schedular = Schedular(unique_id, commands.get_commands(), payload_list, status_updater)
    
if __name__ == "__main__":
    main()
