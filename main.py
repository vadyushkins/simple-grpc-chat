import os

if not os.path.exists("chat_pb2.py") or not os.path.exists("chat_pb2_grpc.py"):
    os.system(
        (
            "python3 "
            "-m "
            "grpc_tools.protoc "
            "-I=. "
            "--python_out=. "
            "--grpc_python_out=. "
            "chat.proto "
        )
    )

from client import run as run_client
from server import run as run_server


def main():
    # TODO: Integrate UI

    type = input("Server of Client? ")

    if type == "Server":
        print("Starting server...")
        run_server()
    elif type == "Client":
        print("Starting client...")
        run_client()


if __name__ == "__main__":
    main()
