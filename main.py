from trello import TrelloClient

api = "31ec916f741962caeb3b4d2ca1fd43b7"
token = "ATTA499aed423e1f8c8d9e6b7342e9fdc93a88053e51526037e58616fb50867236033EB1F029"
board_id = "8Gjc8fX8"
status_list_id = "69a946c9af7564bacbed187d"
command_list_id = "69a946cd58f076e0489335cb"

client = TrelloClient(
    api_key=api,
    api_secret=token,
)


def main():
    board = client.get_board(board_id=board_id)
    print(board.get_list(status_list_id))


if __name__ == "__main__":
    main()
