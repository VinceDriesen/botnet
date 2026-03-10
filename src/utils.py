import os
import platform
import uuid

from trello import Card, List as TrelloList


def card_from_list(lijstje: TrelloList, unique_id: str) -> Card | None:
    cards = lijstje.list_cards(card_filter="open")
    for card in cards:
        if card.name == unique_id:
            return card

    return None


def get_unique_id() -> str:
    if platform.system() == "Linux":
        if os.path.exists("/etc/machine-id"):
            with open("/etc/machine-id", "r") as f:
                return f.read().strip()
    return hex(uuid.getnode())
