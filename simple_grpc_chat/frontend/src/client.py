import threading

from PyQt5 import uic
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QDialog

from simple_grpc_chat.backend.src.client import ClientRunner
from simple_grpc_chat.frontend.config import FRONTEND_DIR

__all__ = ["ClientDialog"]


class ClientDialog(QDialog):
    def __init__(self, client_runner: ClientRunner):
        super().__init__()
        uic.loadUi(str(FRONTEND_DIR / "ui" / "chat.ui"), self)

        self.setFixedSize(self.size())

        self.client = client_runner

        self.cursor = QTextCursor(self.ChatTextEdit.document())
        self.cursor.setPosition(0)
        self.ChatTextEdit.setTextCursor(self.cursor)

        self.MessageLineEdit.returnPressed.connect(self.send_message)

        self.client_chat_thread = threading.Thread(
            target=self.refresh_chat, daemon=True
        )

    def show(self):
        self.client_chat_thread.start()
        super(ClientDialog, self).show()

    def close(self):
        self.client_chat_thread.join()
        super(ClientDialog, self).close()

    def refresh_chat(self):
        for message in self.client.receive_messages():
            if not message.endswith("\n"):
                message += "\n"
            self.ChatTextEdit.insertPlainText(message)

    def send_message(self):
        message = self.MessageLineEdit.text()

        if message != "":
            self.MessageLineEdit.setText("")
            self.client.send_message(message)
