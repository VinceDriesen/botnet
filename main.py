from datetime import datetime
from email.utils import formatdate
from trello import Card, TrelloClient, List as TrelloList
import platform
import uuid
import os
import socket
from typing import List
from enum import Enum
from src.command import Command
from src.runner import Runner
from src.utils import card_from_list
# Nieuwe token aanvragen: https://trello.com/1/authorize?expiration=1day&scope=read,write&response_type=token&key=31ec916f741962caeb3b4d2ca1fd43b7

api = "31ec916f741962caeb3b4d2ca1fd43b7"
token = "ATTA8be4e70421b8e94f58eb722edf7dcbc3f9502cec32383e4ba4599c12c617fbca5637B511"

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
    _update_or_announce(unique_id)
    commands = _fetch_command(unique_id=unique_id)


def _update_or_announce(unique_id) -> None:
    card = card_from_list(status_list, unique_id)
    if card is None:
        _announce(unique_id)
    else:
        _update_status(card, unique_id)


def _announce(unique_id: str):
    print("Announce")
    system_info = _system_info(unique_id)

    status_list.add_card(
        name=system_info[0],
        desc=system_info[1],
    )


def _system_info(unique_id: str) -> tuple[str, str]:
    time_date = formatdate(timeval=None, localtime=False, usegmt=True)

    system_info_list = [
        f"Hostname:     {socket.gethostname()}",
        f"OS Name:      {platform.system()}",
        f"OS Release:   {platform.release()}",
        f"OS Version:   {platform.version()}",
        f"Machine:      {platform.machine()}",
        f"Processor:    {platform.processor()}",
        f"Python:       {platform.python_version()}",
        f"Platform:     {platform.platform()}",
        f"Last Update:  {time_date}"
    ]

    system_desc = "\n".join([f"* {item}" for item in system_info_list])
    return (
        f"{unique_id}",
        system_desc,
    )


def _fetch_command(unique_id: str) -> Command:
    command = Command(command_list)
    return command


def _update_status(card: Card, unique_id: str) -> None:
    print("Update status")
    card.set_description(_system_info(unique_id)[1])


if __name__ == "__main__":
    main()
