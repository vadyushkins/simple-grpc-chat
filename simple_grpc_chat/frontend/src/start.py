from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

from simple_grpc_chat.backend.src.server import ServerRunner
from simple_grpc_chat.frontend.config import FRONTEND_DIR
from simple_grpc_chat.frontend.src.login import LoginDialog
from simple_grpc_chat.frontend.src.server import ServerDialog

__all__ = ["StartDialog"]


class StartDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(FRONTEND_DIR / "ui" / "start.ui"), self)

        self.setFixedSize(self.size())

        self.ClientButton.clicked.connect(self.run_client)
        self.ServerButton.clicked.connect(self.run_server)

        self.login_dialog = LoginDialog()
        self.server_dialog = ServerDialog(ServerRunner())

    def run_client(self):
        self.hide()
        self.login_dialog.show()

    def run_server(self):
        self.hide()
        self.server_dialog.show()

    def close(self):
        super(StartDialog, self).close()
        self.login_dialog.close()
        self.server_dialog.close()
