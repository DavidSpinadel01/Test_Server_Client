import socket
import threading
from message_protocol import send_message, receive_message


class Client:
    def __init__(self, host="127.0.0.1", port=65432):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def send_messages(self):
        while True:
            message = input("You: ")
            send_message(self.socket, message)

    def receive_messages(self):
        while True:
            message = receive_message(self.socket)
            if message:
                print(f"Server: {message}")
            else:
                print("Connection closed by the server")
                break

    def run(self):
        threading.Thread(target=self.receive_messages).start()
        self.send_messages()


if __name__ == "__main__":
    client = Client()
    client.run()
