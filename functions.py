import dialog
import datetime
from pandas import *
import os
from typing import Iterable

def select_snapshot():
    snapshots = os.listdir('snapshots')
    snapshots.remove('most_recent')

def create_connections_snapshot() -> str:
    print ("Создание снапшота связей")
    if not os.path.isdir("snapshots"):
        os.mkdir("snapshots")
    filename = f"snapshots/connections_snapshot{str(datetime.datetime.now()).replace(':', '-')}.csv"
    with open(filename, "w") as f:
        f.write(dialog.connections_columns)

    with open('snapshots/most_recent_connections', "w") as f:
        f.write(filename)

    return filename


def create_snapshot() -> str:
    print ("Создание снапшота")
    if not os.path.isdir("snapshots"):
        os.mkdir("snapshots")
    filename = f"snapshots/net_snapshot{str(datetime.datetime.now()).replace(':', '-')}.csv"
    with open(filename, "w") as f:
        f.write(dialog.csv_columns)

    with open('snapshots/most_recent', "w") as f:
        f.write(filename)

    return filename

def add_connections_data_to_snapshot(snapshot_name: str, connections: Iterable[tuple]):
    print (f"Редактирование {snapshot_name}")
    with open(snapshot_name, "a+") as f:
        text = f.read()
    for device_a, device_b in connections:
        to_write = ';'.join(
            (';'.join(device_a),
            ';'.join(device_b))
        )
        with open(snapshot_name, "a+") as f:
            f.write(to_write)

def add_data_to_snapshot(snapshot_name: str, devices: Iterable[dict]):
    print (f"Редактирование {snapshot_name}")
    with open(snapshot_name, "a+") as f:
        text = f.read()
    for device in devices:
        if device["device_id"] not in text:
            to_write = (device["device_id"]
                        + "," + device["ip"]
                        + "," + device["software"]
                        + "," + device["version"]
            )
            with open(snapshot_name, "a+") as f:
                f.write(to_write)

def select_device(snapshot_name: str) -> str:
    with open(snapshot_name, "r") as f:
        ids = f['device_id'].tolist()
        c = 1
        for device in ids:
            print (f"{c} - {device}")
            c+=1
    answer = input("Выберите номер устройства")
    return answer
    
def select_params(snapshot_name: str) -> str:
    with open(snapshot_name, "r") as f:
        c = 1
        params = []
        for param in params:
            print (f"{c} - {param}")
    answer = input("Выберите параметры")
    return answer

