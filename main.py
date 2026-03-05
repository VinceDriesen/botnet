from trello import TrelloClient

api = "31ec916f741962caeb3b4d2ca1fd43b7"
token = "ATTA499aed423e1f8c8d9e6b7342e9fdc93a88053e51526037e58616fb50867236033EB1F029"

client = TrelloClient(
    api_key=api,
    api_secret=token,
)


def main():
    boards = client.list_boards()
    print(boards[-1].name)


if __name__ == "__main__":
    main()
