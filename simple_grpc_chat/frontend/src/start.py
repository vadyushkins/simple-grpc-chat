"""Application launch window."""
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

from simple_grpc_chat.backend.src.server import ServerRunner
from simple_grpc_chat.frontend.config import FRONTEND_DIR
from simple_grpc_chat.frontend.src.login import LoginDialog
from simple_grpc_chat.frontend.src.server import ServerDialog

__all__ = ["StartDialog"]


class StartDialog(QDialog):
    """A class that represents the application launch window."""

    def __init__(self):
        """Initialize a application launch window instance."""
        super().__init__()

        # load start window UI
        uic.loadUi(str(FRONTEND_DIR / "ui" / "start.ui"), self)

        # fix window size
        self.setFixedSize(self.size())

        # connect buttons to their functionality
        self.ClientButton.clicked.connect(self.run_client)
        self.ServerButton.clicked.connect(self.run_server)

        # create child windows
        self.login_dialog = LoginDialog()
        self.server_dialog = ServerDialog(ServerRunner())

    def run_client(self):
        """ClientButton click action."""
        self.hide()
        self.login_dialog.show()

    def run_server(self):
        """ServerButton click action."""
        self.hide()
        self.server_dialog.show()

    def close(self):
        """Start windown close action."""
        super(StartDialog, self).close()
        self.login_dialog.close()
        self.server_dialog.close()
