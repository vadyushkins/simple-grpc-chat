import sys

from PyQt5.QtWidgets import QApplication

from simple_grpc_chat import StartDialog


def main():
    app = QApplication([])

    start = StartDialog()
    start.show()

    app.exec_()

    start.close()

    sys.exit(0)


if __name__ == "__main__":
    main()
