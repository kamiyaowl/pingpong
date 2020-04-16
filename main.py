import socket
from rich.console import Console
from rich.table import Column, Table

console = Console()

targets = [
    {"host": "localhost", "port": 135, },
    {"host": "127.0.0.1", "port": 445, },
    {"host": "192.168.100.200", "port": 1111, },
    {"host": "192.168.1.1", "port": 22, },
]
timeout_sec = 1

def scan(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout_sec)
    ret = sock.connect_ex((host, port))
    sock.close()
    return ret == 0

def scan_all_and_print(targets):
    # header
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("host")
    table.add_column("port")
    table.add_column("alive")
    # body
    for t in targets:
        resp = scan(t["host"], t["port"])
        table.add_row(
            t["host"], str(t["port"]), ("[green]OK[/green]" if resp else "[red]NG[/red]")
        )
    console.print(table)

scan_all_and_print(targets)