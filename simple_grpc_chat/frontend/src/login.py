from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

from simple_grpc_chat.backend.src.client import ClientRunner
from simple_grpc_chat.frontend import FRONTEND_DIR
from simple_grpc_chat.frontend.src.client import ClientDialog

__all__ = ["LoginDialog"]


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(FRONTEND_DIR / "ui" / "login.ui"), self)

        self.setFixedSize(self.size())

        self.ClearButton.clicked.connect(self.clear_form)
        self.LoginButton.clicked.connect(self.login_user)

        self.client = None

    def clear_form(self):
        self.UsernameLineEdit.setText("")
        self.ServerIPLineEdit.setText("")
        self.ServerPORTLineEdit.setText("")

    def login_user(self):
        name = self.UsernameLineEdit.text()
        ip = self.ServerIPLineEdit.text()
        port = self.ServerPORTLineEdit.text()

        if name != "" and ip != "" and port != "":
            self.close()

            self.client = ClientDialog(
                ClientRunner(
                    name=name,
                    ip=ip,
                    port=port,
                )
            )
            self.client.show()
