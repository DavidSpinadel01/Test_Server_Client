import pytest
from unittest.mock import patch, MagicMock
from client import Client

# Test the Client's ability to send messages
def test_send_messages():
    with patch('builtins.input', return_value='hello'), \
         patch('client.socket.socket') as mock_socket:
        client = Client()
        client.socket.sendall = MagicMock()
        client.send_messages()
        client.socket.sendall.assert_called_with(b'hello\n')

# Test the Client's ability to receive messages
def test_receive_messages():
    with patch('client.socket.socket') as mock_socket, \
         patch('client.receive_message', return_value='hello from server'):
        client = Client()
        client.socket.recv = MagicMock(return_value=b'hello from server\n')
        client.receive_messages()
        mock_socket.recv.assert_called()
```

### Test for `server.py`
e will test the `Server` class, particularly focusing on the acceptance of new connections and the handling of incoming messages.
