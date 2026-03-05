from trello import TrelloClient

api="piemol"
secret="secret"

client = TrelloClient(
    api_key=api,
    api_secret=secret,
)

def main():
    boards = client.list_boards()
    print(boards[-1].name)
    print("Kill me right now")


if __name__ == "__main__":
    main()
