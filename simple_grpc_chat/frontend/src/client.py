"""Application client chat window."""
import threading

from PyQt5 import uic
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QDialog

from simple_grpc_chat.backend.src.client import ClientRunner
from simple_grpc_chat.frontend.config import FRONTEND_DIR

__all__ = ["ClientDialog"]


class ClientDialog(QDialog):
    """A class that represents the client chat window."""

    def __init__(self, client_runner: ClientRunner):
        """Initialize a client chat window instance."""
        super().__init__()

        # load user login window UI
        uic.loadUi(str(FRONTEND_DIR / "ui" / "chat.ui"), self)

        # fix window size
        self.setFixedSize(self.size())

        # connect client chat window to its backend
        self.client = client_runner

        # create cursor for chat messages
        self.cursor = QTextCursor(self.ChatTextEdit.document())
        self.cursor.setPosition(0)
        self.ChatTextEdit.setTextCursor(self.cursor)

        # connect MessageLineEdit field to its sending functionality
        self.MessageLineEdit.returnPressed.connect(self.send_message)

        # create thread for chat window
        self.client_chat_thread = threading.Thread(
            target=self.refresh_chat, daemon=True
        )

    def show(self):
        """Client chat window show action."""
        self.client_chat_thread.start()
        super(ClientDialog, self).show()

    def close(self):
        """Client chat window close action."""
        self.client_chat_thread.join()
        super(ClientDialog, self).close()

    def refresh_chat(self):
        """Update the client chat with messages received from the server."""
        for message in self.client.receive_messages():
            if not message.endswith("\n"):
                message += "\n"
            self.ChatTextEdit.insertPlainText(message)

    def send_message(self):
        """Send message to the server from MessageLineEdit field."""
        message = self.MessageLineEdit.text()

        if message != "":
            self.MessageLineEdit.setText("")
            self.client.send_message(message)
