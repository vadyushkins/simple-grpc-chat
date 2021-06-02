from concurrent import futures

import grpc

import chat_pb2 as chat
import chat_pb2_grpc as rpc


class ChatServicer(rpc.ChatServicer):
    def __init__(self):
        self.messages = []

    def receive_messages(self, request_iterator, context):
        lastindex = 0
        while True:
            while len(self.messages) > lastindex:
                new_message = self.messages[lastindex]
                lastindex += 1
                yield new_message

    def send_message(self, request, context):
        self.messages.append(request)
        return chat.Empty()


def run():
    port = 50051
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    rpc.add_ChatServicer_to_server(ChatServicer(), server)
    server.add_insecure_port("[::]:" + str(port))
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    run()
