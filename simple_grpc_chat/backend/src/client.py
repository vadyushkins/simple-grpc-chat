from time import strftime

import grpc

import simple_grpc_chat.backend.protos.chat_pb2 as chat
import simple_grpc_chat.backend.protos.chat_pb2_grpc as rpc

__all__ = ["ClientRunner"]


class ClientRunner:
    def __init__(self, name="User", ip="localhost"):
        self.name = name
        self.ip = ip
        self.port = 50051
        self.connection = rpc.ChatStub(grpc.insecure_channel(f"{self.ip}:{self.port}"))

    def receive_messages(self):
        for message in self.connection.receive_messages(chat.Empty()):
            yield f"[{message.time}, {message.name}] {message.message}"

    def send_message(self, message):
        new_message = chat.Message()
        new_message.name = self.name
        new_message.message = message
        new_message.time = strftime("%H:%M")

        self.connection.send_message(new_message)
