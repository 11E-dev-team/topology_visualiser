import dialog
import datetime
from pandas import *
import os
from typing import Iterable

def delete_snapshot(snapshot_id) -> str:
    if os.path.isfile(net_snapshot_path(snapshot_id)):
        os.remove(net_snapshot_path(snapshot_id))
    if os.path.isfile(connections_snapshot_path(snapshot_id)):
        os.remove(connections_snapshot_path(snapshot_id))

def most_recent_snapshot() -> str:
    with open('snapshots/most_recent') as m:
        mrs = m.read()
    return mrs

def select_snapshot() -> str:
    snapshots = os.listdir('snapshots')
    c = 1
    all_snapshots = [
        s[len("net_snapshot"):-len(".csv")]
        for s in snapshots
        if s.startswith('net_')
    ]
    for snapshot in reversed(all_snapshots):
        print (f"{c} - {snapshot[len('net_snapshot'):-len('.csv')]}")
        c += 1
    answer = int(input(("Выберите снапшот: ")))
    return snapshots[answer-1][len("net_snapshot"):-len(".csv")]

def create_snapshot() -> str:
    print ("Создание образа сети")
    if not os.path.isdir("snapshots"):
        os.mkdir("snapshots")
    snapshot_id = str(datetime.datetime.now()).replace(':', '-')
    with open(connections_snapshot_path(snapshot_id), "w") as f:
        f.write(dialog.connections_columns)
    with open(net_snapshot_path(snapshot_id), "w") as f:
        f.write(dialog.csv_columns)

    with open('snapshots/most_recent', "w") as f:
        f.write(snapshot_id)
    return snapshot_id

def connections_snapshot_path(snapshot_id: str):
    return f"snapshots/connections_snapshot{snapshot_id}.csv"

def net_snapshot_path(snapshot_id: str):
    return f"snapshots/net_snapshot{snapshot_id}.csv"

def add_connections_data_to_snapshot(snapshot_id: str, connections: Iterable[tuple]):
    print (f"Редактирование образа {snapshot_id}")
    to_write = ""
    print("Запись:\n", connections)
    for device_a, device_b in connections:
        to_write += ';'.join(
            (';'.join(device_a),
            ';'.join(device_b))
        ) + "\n"
    with open(connections_snapshot_path(snapshot_id), "a+") as f:
        f.write(to_write[:-1])

def add_data_to_snapshot(snapshot_id: str, devices: Iterable[dict]):
    print (f"Редактирование обараза {snapshot_id} (устройства)")
    with open(net_snapshot_path(snapshot_id), "a+") as f:
        text = f.read()
    to_write  = ""
    for device in devices:
        if device["device_id"] not in text:
            to_write += (device["device_id"]
                        + ";" + device["ip"]
                        + ";" + device["software"]
                        + ";" + device["version"]
                        + "\n"
            )
    with open(net_snapshot_path(snapshot_id), "a+") as f:
        f.write(to_write[:-1])

def select_device(snapshot_id: str) -> str:
    file = read_csv(net_snapshot_path(snapshot_id), sep=";")
    ids = file["Device ID"].tolist()
    c = 1
    for device in ids:
        print (f"{c} - {device}")
        c+=1
    answer = int(input("Выберите номер устройства: "))
    return ids[answer-1]
    
def select_params(snapshot_id: str) -> str:
    file = read_csv(net_snapshot_path(snapshot_id), sep=";", index_col=['Device ID'])
    columns = file.columns.tolist()
    c = 1
    for param in columns:
        print (f"{c} - {param}")
        c+=1
    answer = int(input("Выберите параметр: "))
    return columns[answer-1]

def get_data (snapshot_id, device_id, param) -> str:
    file = read_csv(net_snapshot_path(snapshot_id), sep=";", index_col=['Device ID'])
    print (f"{param}: \n {file[param][device_id]}")

def read_connections_snapshot(snapshot_id):
    with open(connections_snapshot_path(snapshot_id)) as f:
        for line in f.readlines()[1:]:
            args = line.strip(';')
            yield (tuple(args[:2]), tuple(args[2:]))