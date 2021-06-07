import socket
from concurrent import futures
from random import randint

from grpc import server

from simple_grpc_chat.backend.protos.chat_pb2 import Empty
from simple_grpc_chat.backend.protos.chat_pb2_grpc import (
    ChatServicer,
    add_ChatServicer_to_server,
)

__all__ = ["ServerRunner"]


class ChatServicer(ChatServicer):
    def __init__(self):
        self.messages = []

    def receive_messages(self, request_iterator, context):
        lastindex = 0
        while True:
            while len(self.messages) > lastindex:
                new_message = self.messages[lastindex]
                lastindex += 1
                yield new_message

    def send_message(self, request, context):
        self.messages.append(request)
        return Empty()


class ServerRunner:
    def __init__(self, ip=None, port=None):
        if ip is None:
            self.ip = socket.gethostbyname(socket.gethostname())
        else:
            self.ip = ip

        if port is None:
            self.port = 50000 + randint(1, 1000)
        else:
            self.port = port

    def start(self):
        self.server = server(futures.ThreadPoolExecutor(max_workers=3))
        self.chat_servicer = ChatServicer()
        add_ChatServicer_to_server(self.chat_servicer, self.server)
        self.server.add_insecure_port(f"{self.ip}:{self.port}")
        self.server.start()

    def stop(self):
        self.server.stop()
