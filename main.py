from trello import TrelloClient

api="piemol"
secret="secret"

client = TrelloClient(
    api_key=api,
    api_secret=secret,
    token='your-oauth-token-key',
    token_secret='your-oauth-token-secret'
)

def main():
    print("Kill me right now")


if __name__ == "__main__":
    main()
