"""
net utils
"""

import socket
from _socket import SocketType


def get_local_ip() -> str:
    """
    get local network ip
    :return: local network ip
    """
    s: SocketType = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip: str = s.getsockname()[0]
    s.close()
    return ip
