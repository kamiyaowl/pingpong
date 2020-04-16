import socket
import schedule
import time
import datetime
from rich.console import Console
from rich.table   import Column, Table

console = Console()

# Config
targets = [
    {"host": "localhost", "port": 135, "remark": "test", },
    {"host": "127.0.0.1", "port": 445, "remark": "", },
    {"host": "192.168.100.200", "port": 1111, },
    {"host": "192.168.1.1", "port": 22, },
]
timeout_sec = 1
duration_sec = 1
datetime_format = "Update At: %Y/%m/%d %H:%M:%S"

# 指定したhost,portと接続できればTrueを返します
def scan(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout_sec)
    ret = sock.connect_ex((host, port))
    sock.close()
    return ret == 0

# 指定されたhost,portのリストのdead or aliveを表敬式で表示します
def scan_all_and_print(targets):
    # header
    table = Table(show_header=True, header_style="bold magenta", title=datetime.datetime.now().strftime(datetime_format))
    table.add_column("host", style="dim")
    table.add_column("port", justify="right")
    table.add_column("alive")
    table.add_column("remark")
    # body
    for t in targets:
        resp = scan(t["host"], t["port"])
        table.add_row(
            t["host"], 
            str(t["port"]),
            ("[green]OK[/green]" if resp else "[red]NG[/red]"),
            (t["remark"] if ("remark" in t) > 0 else "")
        )
    console.print(table)

# Run
schedule.every(duration_sec).seconds.do(lambda: scan_all_and_print(targets))
while True:
    schedule.run_pending()
    time.sleep(1)