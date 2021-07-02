"""Backend for client functionality.
"""
import socket
from concurrent import futures
from typing import List, Iterator, Any

from grpc import server
from grpc._server import _Server

from simple_grpc_chat.backend.protos.chat_pb2 import Empty
from simple_grpc_chat.backend.protos.chat_pb2_grpc import (
    ChatServicer as gRPCChatServicer,
    add_ChatServicer_to_server,
)

__all__ = ["ServerRunner"]


class ChatServicer(gRPCChatServicer):
    """Class for running backend chat service functionality."""

    def __init__(self):
        """Initialize a chat service instance."""
        self.messages: List[str] = list()

    def receive_messages(
        self, request_iterator: Iterator, context: Any
    ) -> Iterator[str]:
        """Function for receiving messages from clients.

        Returns
        -------
        messages : Generator[str]
            Clients message flow.
        """
        lastindex = 0
        while True:
            while len(self.messages) > lastindex:
                new_message = self.messages[lastindex]
                lastindex += 1
                yield new_message

    def send_message(self, request: str, context: Any):
        """Function for receiving messages from the client.

        Parameters
        ----------
        request : str
            Message from client.

        context : Any
            Client message context.
        """
        self.messages.append(request)
        return Empty()


class ServerRunner:
    """Class for running server backend functionality."""

    def __init__(self, ip: str = "localhost"):
        """Initialize a server instance."""
        self.ip: str = socket.gethostbyname(socket.gethostname()) if ip is None else ip
        self.port: int = 50051

        self.thread_pool: futures.ThreadPoolExecutor = futures.ThreadPoolExecutor(
            max_workers=3
        )
        self.server: _Server = server(self.thread_pool)
        self.chat_servicer: ChatServicer = ChatServicer()

    def start(self):
        """Function for starting server."""
        add_ChatServicer_to_server(self.chat_servicer, self.server)
        self.server.add_insecure_port(f"{self.ip}:{self.port}")
        self.server.start()

    def stop(self):
        """Function for stopping server."""
        self.server.stop(grace=None)
        self.thread_pool.shutdown(wait=False)
