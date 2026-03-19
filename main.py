import atexit

from trello import TrelloClient, List as TrelloList
from src.utils import get_unique_id
from src.command import Command
from src.schedular import Schedular
from src.status_updater import StatusUpdater
import time
# Nieuwe token aanvragen: https://trello.com/1/authorize?expiration=1day&scope=read,write&response_type=token&key=31ec916f741962caeb3b4d2ca1fd43b7

api = "31ec916f741962caeb3b4d2ca1fd43b7"
token = "ATTAbbb0df7680738b87679dcc32e18c97ca877040bd54da2db90c89433cd37c73a3B1F31D43"

board_id = "8Gjc8fX8"
status_list_id = "69a946c9af7564bacbed187d"
command_list_id = "69a946cd58f076e0489335cb"
payload_list_id = "69a957e9099ba7c6167a878a"

client = TrelloClient(
    api_key=api,
    api_secret=token,
)

board = client.get_board(board_id=board_id)
status_list: TrelloList = board.get_list(status_list_id)
command_list: TrelloList = board.get_list(command_list_id)
payload_list: TrelloList = board.get_list(payload_list_id)


def main():
    unique_id = get_unique_id()
    status_updater = StatusUpdater(unique_id, status_list)

    atexit.register(status_updater.remove_status)

    try:
        while True:
            time.sleep(1)
            status_updater.update_or_announce()
            commands = Command(command_list)
            schedular = Schedular(
                unique_id, commands.get_commands(), payload_list, status_updater
            )
    finally:
        status_updater.remove_status()
        

if __name__ == "__main__":
    main()
