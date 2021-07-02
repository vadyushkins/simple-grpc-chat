"""Application launch point."""
import sys

from PyQt5.QtWidgets import QApplication

from simple_grpc_chat import StartDialog


def main():
    """Launch application."""
    # create application
    app = QApplication([])

    # show launch application window
    start = StartDialog()
    start.show()

    # execute application
    app.exec_()

    # close launch application window
    start.close()

    sys.exit(0)


if __name__ == "__main__":
    main()
