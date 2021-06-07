import sys

from PyQt5.QtWidgets import QApplication

from simple_grpc_chat import StartDialog


def main():
    app = QApplication([])

    start = StartDialog()
    start.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
