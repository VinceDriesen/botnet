from trello import List as TrelloList, Card
from .utils import card_from_list


class Runner:
    def execute_command(self, payload_id: str, payload_list: TrelloList):
        self._run_payload(payload_list, payload_id)

    def remove_client(self, unique_id: str):

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
