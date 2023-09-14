import dialog
import datetime
from pandas import *
import os
from typing import Iterable

def select_snapshot() -> str:
    snapshots = os.listdir('snapshots')
    snapshots.remove('most_recent')
    c = 1
    for snapshot in snapshots:
        print (f"{c} - {snapshot}")
        c += 1
    answer = int(input(("Выберите снапшот: ")))
    return snapshots[answer-1]

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
    file = read_csv(f"snapshots/{snapshot_name}", sep=";")
    ids = file["Device ID"].tolist()
    c = 1
    for device in ids:
        print (f"{c} - {device}")
        c+=1
    answer = int(input("Выберите номер устройства: "))
    return ids[answer-1]
    
def select_params(snapshot_name: str) -> str:
    file = read_csv(f"snapshots/{snapshot_name}", sep=";", index_col=['Device ID'])
    columns = file.columns.tolist()
    c = 1
    for param in columns:
        print (f"{c} - {param}")
        c+=1
    answer = int(input("Выберите параметр: "))
    return columns[answer-1]

def get_data (snapshot_name, device_id, param) -> str:
    file = read_csv(f"snapshots/{snapshot_name}", sep=";", index_col=['Device ID'])
    print (file[param][device_id])
