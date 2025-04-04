import socket

def get_free_port():
    s = socket.socket()
    s.bind(('', 0))  # Bind to a free port provided by the host
    addr, port = s.getsockname()
    s.close()
    return port