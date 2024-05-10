import socket
import threading
from message_protocol import receive_message, send_message


class ClientHandler(threading.Thread):
    def __init__(self, client_socket, server):
        super().__init__()
        self.client_socket = client_socket
        self.server = server

    def run(self):
        while True:
            try:
                message = receive_message(self.client_socket)
                if message:
                    print(f"Received message: {message}")
                    self.broadcast_message(message)
                else:
                    self.disconnect()
                    break
            except Exception as e:
                print(f"Error: {e}")
                self.disconnect()
                break

    def broadcast_message(self, message):
        for client in self.server.clients:
            if client != self.client_socket:
                send_message(client, message)

    def disconnect(self):
        print(f"Closed connection from {self.client_socket.getpeername()}")
        self.server.clients.remove(self.client_socket)
        self.client_socket.close()
