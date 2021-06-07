from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

from simple_grpc_chat.backend.src.client import ClientRunner
from simple_grpc_chat.frontend.src.client import ClientDialog
from simple_grpc_chat.frontend import FRONTEND_DIR

__all__ = ["LoginDialog"]


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(FRONTEND_DIR / "ui" / "login.ui"), self)

        self.setFixedSize(self.size())

        self.CancelButton.clicked.connect(self.clear_form)
        self.LoginButton.clicked.connect(self.login)

    def clear_form(self):
        self.UsernameLineEdit.setText("")
        self.ServerIPLineEdit.setText("")
        self.ServerPORTLineEdit.setText("")

    def login(self):
        name = self.UsernameLineEdit.text()
        ip = self.ServerIPLineEdit.text()
        port = self.ServerPORTLineEdit.text()

        if name != "" and ip != "" and port != "":
            self.hide()

            self.client_runner = ClientRunner(
                name=name,
                ip=ip,
                port=port,
            )
            self.client_dialog = ClientDialog(self.client_runner)
            self.client_dialog.show()
