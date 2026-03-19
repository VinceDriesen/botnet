from email.utils import formatdate
from trello import List as TrelloList, Card
import platform
import socket
from src.utils import card_from_list


class StatusUpdater:
    def __init__(self, unique_id: str, status_list: TrelloList) -> None:
        self.unique_id = unique_id
        self.status_list = status_list

    def update_or_announce(self) -> None:
        card = self._get_card()
        if card is None:
            self._announce()
        else:
            self._update_status(card)

    def remove_status(self) -> None:
        card = self._get_card()
        card.delete()

    def _announce(self):
        system_info = self._system_info()

        self.status_list.add_card(
            name=system_info[0],
            desc=system_info[1],
        )

    def _get_card(self) -> Card:
        return card_from_list(self.status_list, self.unique_id)

    def _system_info(self) -> tuple[str, str]:
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
            f"Last Update:  {time_date}",
        ]

        system_desc = "\n".join([f"* {item}" for item in system_info_list])
        return (
            f"{self.unique_id}",
            system_desc,
        )

    def _update_status(self, card) -> None:
        card.set_description(self._system_info()[1])
