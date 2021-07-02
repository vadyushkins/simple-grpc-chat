"""Application user login window."""
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

from simple_grpc_chat.backend.src.client import ClientRunner
from simple_grpc_chat.frontend import FRONTEND_DIR
from simple_grpc_chat.frontend.src.client import ClientDialog

__all__ = ["LoginDialog"]


class LoginDialog(QDialog):
    """A class that represents the user login window."""

    def __init__(self):
        """Initialize a user login window instance."""
        super().__init__()

        # load user login window UI
        uic.loadUi(str(FRONTEND_DIR / "ui" / "login.ui"), self)

        # fix window size
        self.setFixedSize(self.size())

        # connect buttons to their functionality
        self.ClearButton.clicked.connect(self.clear_form)
        self.LoginButton.clicked.connect(self.login_user)

        # field for client chat window
        self.client = None

    def clear_form(self):
        """ClearButton click action."""
        self.UsernameLineEdit.setText("")
        self.ServerIPLineEdit.setText("")

    def login_user(self):
        """LoginButton click action."""
        name = self.UsernameLineEdit.text()
        ip = self.ServerIPLineEdit.text()

        if name != "" and ip != "":
            self.close()

            self.client = ClientDialog(
                ClientRunner(
                    name=name,
                    ip=ip,
                )
            )
            self.client.show()
