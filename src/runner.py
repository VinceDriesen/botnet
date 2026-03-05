from trello import List as TrelloList, Card
from .utils import card_from_list


class Runner:
    def __init__(self, payload_id: str, payload_list: TrelloList):
        self.payload_id = payload_id
        self.payload_list = payload_list
        self.payload = ""
        self._find_payload()
        if len(self.payload) > 0:
            self._run()

    def _find_payload(self):
        card = card_from_list(self.payload_list, self.payload_id)
        if card is None:
            print("Geen valid payload")
        else:
            self.payload = card.desc
        print(card)

    def _run(self):
        veilige_payload = self.payload.replace('“', '"').replace(
            '”', '"').replace("‘", "'").replace("’", "'")

        exec(veilige_payload)
