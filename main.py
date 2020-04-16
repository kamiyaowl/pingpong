import socket

targets = [
    {"host": "localhost", "port": 135, },
    {"host": "127.0.0.1", "port": 445, },
    {"host": "192.168.100.200", "port": 1111, },
    {"host": "192.168.1.1", "port": 22, },
]

def scan(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ret = sock.connect_ex((host, port))
    sock.close()
    return ret == 0

results = map(lambda t: scan(t["host"], t["port"]), targets)
for r in results:
    print(r)