from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

from simple_grpc_chat.backend.src.server import ServerRunner
from simple_grpc_chat.frontend import FRONTEND_DIR

__all__ = ["ServerDialog"]


class ServerDialog(QDialog):
    def __init__(self, server_runner: ServerRunner):
        super().__init__()
        uic.loadUi(str(FRONTEND_DIR / "ui" / "server.ui"), self)

        self.setFixedSize(self.size())

        self.server = server_runner

        self.IPLabel.setText(f"IP = {self.server.ip}")
        self.PORTLabel.setText(f"PORT = {self.server.port}")

    def show(self):
        self.server.start()
        super(ServerDialog, self).show()

    def close(self):
        self.server.stop()
        super(ServerDialog, self).close()
