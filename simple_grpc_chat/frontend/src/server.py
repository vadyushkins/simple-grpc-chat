"""Application server window."""
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

from simple_grpc_chat.backend.src.server import ServerRunner
from simple_grpc_chat.frontend import FRONTEND_DIR

__all__ = ["ServerDialog"]


class ServerDialog(QDialog):
    """A class that represents the server window."""

    def __init__(self, server_runner: ServerRunner):
        """Initialize a server window instance."""
        super().__init__()

        # load user login window UI
        uic.loadUi(str(FRONTEND_DIR / "ui" / "server.ui"), self)

        # fix window size
        self.setFixedSize(self.size())

        # connect server window to its backend
        self.server = server_runner

        # set server IP
        self.IPLabel.setText(f"IP = {self.server.ip}")

    def show(self):
        """Server window show action."""
        self.server.start()
        super(ServerDialog, self).show()

    def close(self):
        """Server window close action."""
        self.server.stop()
        super(ServerDialog, self).close()
