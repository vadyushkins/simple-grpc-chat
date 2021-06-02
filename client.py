import threading

import grpc

import chat_pb2 as chat
import chat_pb2_grpc as rpc


class Client:
    def __init__(self, name, address="localhost", port=50051):
        self.name = name
        self.conn = rpc.ChatStub(grpc.insecure_channel(f"{address}:{port}"))
        threading.Thread(target=self.listen_for_messages, daemon=True).start()
        self.setup_ui()

    def listen_for_messages(self):
        # TODO: Integrate UI
        for message in self.conn.receive_messages(chat.Empty()):
            print(message)

    def send_message(self):
        # TODO: Integrate UI
        message = input(f"{self.name} message: ")

        new_message = chat.Message()
        new_message.name = self.name
        new_message.message = message
        new_message.time = "TIME"

        self.conn.send_message(new_message)

    def setup_ui(self):
        # TODO: Setup UI
        pass


def run():
    username = input("Username: ")
    client = Client(username)
    while True:
        client.send_message()


if __name__ == "__main__":
    run()
