import socket
import select
from client_handler import ClientHandler


class Server:
    def __init__(self, host="127.0.0.1", port=65432):
        self.host = host
        self.port = port
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

    def run(self):
        print(f"Server listening on {self.host}:{self.port}")
        try:
            while True:
                read_sockets, _, _ = select.select(
                    [self.server_socket] + self.clients, [], []
                )
                for notified_socket in read_sockets:
                    if notified_socket == self.server_socket:
                        client_socket, client_address = self.server_socket.accept()
                        self.clients.append(client_socket)
                        print(
                            f"Accepted new connection from {client_address[0]}:{client_address[1]}"
                        )
                        ClientHandler(client_socket, self).start()
                    else:
                        pass  # ClientHandler will handle client messages
        finally:
            self.server_socket.close()


if __name__ == "__main__":
    server = Server()
    server.run()
