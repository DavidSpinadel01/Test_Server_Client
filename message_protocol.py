
HEADER_LENGTH = 10

def send_message(socket, message):
    message = message.encode('utf-8')
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
    socket.send(message_header + message)

def receive_message(socket):
    try:
        message_header = socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        message_length = int(message_header.strip())
        return socket.recv(message_length).decode('utf-8')
    except:
        return False