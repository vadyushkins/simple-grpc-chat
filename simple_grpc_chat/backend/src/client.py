"""Backend for client functionality.
"""
from time import strftime
from typing import Iterator

import grpc

import simple_grpc_chat.backend.protos.chat_pb2 as chat
import simple_grpc_chat.backend.protos.chat_pb2_grpc as rpc

__all__ = ["ClientRunner"]


class ClientRunner:
    """Class for running client backend functionality."""

    def __init__(self, name: str = "User", ip: str = "localhost"):
        """Initialize a client instance.

        Parameters
        ----------
        name : str
            Client name.

        ip : str
            Server address to which the client connects.
        """
        self.name: str = name
        self.ip: str = ip
        self.port: int = 50051
        self.connection: rpc.ChatStub = rpc.ChatStub(
            grpc.insecure_channel(f"{self.ip}:{self.port}")
        )

    def receive_messages(self) -> Iterator[str]:
        """Function for receiving messages from the server.

        Returns
        -------
        messages : Iterator[str]
            Server message flow.
        """
        for message in self.connection.receive_messages(chat.Empty()):
            yield f"[{message.time}, {message.name}] {message.message}"

    def send_message(self, message: str):
        """Function for sending a message to the server.

        Parameters
        ----------
        message : str
            Message to send.
        """
        new_message = chat.Message()
        new_message.name = self.name
        new_message.message = message
        new_message.time = strftime("%H:%M")

        self.connection.send_message(new_message)
