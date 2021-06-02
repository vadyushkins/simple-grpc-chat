import client
import server


def main():
    # TODO: Integrate UI

    type = input("Server of Client? ")

    if type == "Server":
        print("Starting server...")
        server.run()
    elif type == "Client":
        print("Starting client...")
        client.run()


if __name__ == "__main__":
    main()
