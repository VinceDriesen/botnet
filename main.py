from trello import TrelloClient
import platform
import uuid
import os
import socket

# Nieuwe token aanvragen: https://trello.com/1/authorize?expiration=1day&scope=read,write&response_type=token&key=31ec916f741962caeb3b4d2ca1fd43b7

api = "31ec916f741962caeb3b4d2ca1fd43b7"
token = "ATTA8be4e70421b8e94f58eb722edf7dcbc3f9502cec32383e4ba4599c12c617fbca5637B511"

board_id = "8Gjc8fX8"
status_list_id = "69a946c9af7564bacbed187d"
command_list_id = "69a946cd58f076e0489335cb"

client = TrelloClient(
    api_key=api,
    api_secret=token,
)

board = client.get_board(board_id=board_id)
status_list = board.get_list(status_list_id)
command_list = board.get_list(command_list_id)


def _get_unique_id():
    if platform.system() == "Linux":
        if os.path.exists("/etc/machine-id"):
            with open("/etc/machine-id", "r") as f:
                return f.read().strip()
    return hex(uuid.getnode())


def main():
    _announce()


def _announce():
    system_info_list = [
        f"Unique ID:    {_get_unique_id()}",
        f"Hostname:     {socket.gethostname()}",
        f"OS Name:      {platform.system()}",
        f"OS Release:   {platform.release()}",
        f"OS Version:   {platform.version()}",
        f"Machine:      {platform.machine()}",
        f"Processor:    {platform.processor()}",
        f"Python:       {platform.python_version()}",
        f"Platform:     {platform.platform()}"
    ]
    system_desc = "\n".join([f"* {item}" for item in system_info_list[1:]])
    status_list.add_card(
        name=system_info_list[0],
        desc=system_desc,


    )


def _update_status():
    pass


if __name__ == "__main__":
    main()
