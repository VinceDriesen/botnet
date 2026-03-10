from email.utils import formatdate
from trello import Card, List as TrelloList
import platform
import socket
from src.utils import card_from_list
from src.command import TaskType

class StatusUpdater:
    def __init__(self, unique_id: str, status_list: TrelloList) -> None:
        self.unique_id = unique_id
        self.status_list = status_list
        self.card = card_from_list(self.status_list, self.unique_id)
    
    def update_or_announce(self) -> None:
        if self.card is None:
            self._announce()
        else:
            self._update_status(self.card)
            
    def runned_payload(self, additional_info: str) -> None:
        self.update_or_announce()
        description: str = self.card.description
        description = additional_info + "\n" + description
        self.card.set_description(description)
            
    def remove_status(self) -> None:
        self.card.delete()

    def _announce(self):
        print("Announce")
        system_info = self._system_info()

        self.status_list.add_card(
            name=system_info[0],
            desc=system_info[1],
        )


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
            f"Last Update:  {time_date}"
        ]

        system_desc = "\n".join([f"* {item}" for item in system_info_list])
        return (
            f"{self.unique_id}",
            system_desc,
        )


    def _update_status(self, card) -> None:
        print("Update status")
        card.set_description(self._system_info()[1])