import pytest
import struct
from unittest.mock import MagicMock, patch
from message_protocol import send_message, receive_message, HEADER_LENGTH

# Mock socket object
@pytest.fixture
def mock_socket():
    return MagicMock()

def test_send_message(mock_socket):
    message = "Hello, world!"
    send_message(mock_socket, message)

    # Check if socket.send was called with the correct message header and message
    expected_message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
    expected_message = message.encode('utf-8')
    mock_socket.send.assert_called_once_with(expected_message_header + expected_message)

def test_receive_message(mock_socket):
    message = "Hello, world!"
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
    mock_socket.recv.side_effect = [message_header, message.encode('utf-8')]

    received_message = receive_message(mock_socket)

    # Check if the correct message was received
    assert received_message == message

def test_receive_message_empty(mock_socket):
    # Simulate an empty message header, indicating the connection is closed
    mock_socket.recv.return_value = b''

    received_message = receive_message(mock_socket)

    # Check if the function returns False when an empty message header is received
    assert received_message is False

def test_receive_message_exception(mock_socket):
    # Simulate an exception while receiving a message
    mock_socket.recv.side_effect = Exception()

    received_message = receive_message(mock_socket)

    # Check if the function returns False when an exception occurs
    assert received_message is False
