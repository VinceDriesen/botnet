from trello import Card, List as TrelloList


def card_from_list(lijstje: TrelloList, unique_id: str) -> Card | None:
    cards = lijstje.list_cards(card_filter="open")
    for card in cards:
        if card.name == unique_id:
            return card

    return None
