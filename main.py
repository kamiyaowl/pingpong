import os
import socket
import schedule
import time
import datetime
import json
from rich.console import Console
from rich.table import Column, Table

console = Console()

# Config
f = open("config.json", "r")
config = json.load(f)

# port scan時のtimeout
timeout_sec = config["timeout_sec"]
# scanする周期
duration_sec = config["duration_sec"]
# 表のタイトルに表示する時刻文字列
datetime_format = config["datetime_format"]
# Scan対象のリスト
targets = config["targets"]


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
    table = Table(show_header=True, header_style="bold magenta",
                  title=datetime.datetime.now().strftime(datetime_format))
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
    os.system("cls")
    console.print(table)

def job():
    scan_all_and_print(targets)    

# Run

job() # 初回は一回出しておく
schedule.every(duration_sec).seconds.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
