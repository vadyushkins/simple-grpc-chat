import socket
from concurrent import futures
from random import randint

from grpc import server

from simple_grpc_chat.backend.protos.chat_pb2 import Empty
from simple_grpc_chat.backend.protos.chat_pb2_grpc import (
    ChatServicer as gRPCChatServicer,
    add_ChatServicer_to_server,
)

__all__ = ["ServerRunner"]


class ChatServicer(gRPCChatServicer):
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
        self.ip = socket.gethostbyname(socket.gethostname()) if ip is None else ip
        self.port = 50000 + randint(1, 1000) if port is None else port

        self.thread_pool = futures.ThreadPoolExecutor(max_workers=3)
        self.server = server(self.thread_pool)
        self.chat_servicer = ChatServicer()

    def start(self):
        add_ChatServicer_to_server(self.chat_servicer, self.server)
        self.server.add_insecure_port(f"{self.ip}:{self.port}")
        self.server.start()

    def stop(self):
        self.server.stop(grace=None)
        self.thread_pool.shutdown(wait=False)
