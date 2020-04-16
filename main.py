import os
import sys
import time
import json
import socket
import schedule
import datetime
import argparse
from rich.console import Console
from rich.table import Column, Table

# 指定したhost,portと接続できればTrueを返します
def scan(host, port, timeout_sec):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout_sec)
    ret = sock.connect_ex((host, port))
    sock.close()
    return ret == 0

# 指定されたhost,portのリストのdead or aliveを表敬式で表示します
def scan_all_and_print(config):
    # header
    table = Table(show_header=True, header_style="bold magenta",
                  title=datetime.datetime.now().strftime(config["datetime_format"]))
    table.add_column("host", style="dim")
    table.add_column("port", justify="right")
    table.add_column("alive")
    table.add_column("remark")
    # body
    for t in config["targets"]:
        resp = scan(t["host"], t["port"], config["timeout_sec"])
        table.add_row(
            t["host"],
            str(t["port"]),
            ("[green]OK[/green]" if resp else "[red]NG[/red]"),
            (t["remark"] if ("remark" in t) > 0 else "")
        )
    os.system("cls")
    console = Console()
    console.print(table)

if __name__ == '__main__':
    # Parse Arguments
    parser = argparse.ArgumentParser(description='simple alive checker.')
    parser.add_argument("-c", "--config", default="config.json", help="path to config.json")
    parser.add_argument("-o", "--once", action="store_true", help="scan once")
    args = parser.parse_args()
    # Read and Prepare Config
    f = open(args.config, "r")
    config = json.load(f)

    def job():
        scan_all_and_print(config)

    # Run Once
    job()
    if (args.once):
        sys.exit(0)

    # Run contusions scan
    schedule.every(config["duration_sec"]).seconds.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
