from trello import TrelloClient

api = "31ec916f741962caeb3b4d2ca1fd43b7"
secret = "adf924cd87998ca0832d5ad7adf015d7ac89765efd5c9390900f94faad14695b"

client = TrelloClient(
    api_key=api,
    api_secret=secret,
)


def main():
    boards = client.list_boards()
    print(boards[-1].name)


if __name__ == "__main__":
    main()
