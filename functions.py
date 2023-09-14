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


def get_snapshots() -> str:
    snapshots = os.listdir('snapshots')
    c = 1
    all_snapshots = [
        s[len("net_snapshot"):-len(".csv")]
        for s in snapshots
        if s.startswith('net_')
    ]
    return all_snapshots


def select_snapshot(snapshots=None) -> str:
    if snapshots == None:
        snapshots = os.listdir('snapshots')
        all_snapshots = [
            s[len("net_snapshot"):-len(".csv")]
            for s in snapshots
            if s.startswith('net_')
        ]
    else:
        all_snapshots = snapshots
    c = 1
    for snapshot in reversed(all_snapshots):
        print (f"{c} - {snapshot[len('net_snapshot')-1:-len('.csv')]}")
        c += 1
    answer = int(input(("Выберите снапшот: ")))
    return snapshots[answer-1][len("net_snapshot")-1:-len(".csv")]


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
    ips = file["IP address"].tolist()
    c = 1
    for i in range(len(ids)):
        print (f"{c} - {ids[i]} : {ips[i]}")
        c+=1
    answer = int(input("Выберите номер устройства: "))
    return ips[answer-1]


def select_params(snapshot_id: str) -> str:
    file = read_csv(net_snapshot_path(snapshot_id), sep=";", index_col=['IP address'])
    columns = file.columns.tolist()
    columns.remove("Device ID")
    c = 1
    for param in columns:
        print (f"{c} - {param}")
        c+=1
    answer = int(input("Выберите параметр: "))
    return columns[answer-1]


def get_data (snapshot_id, device_ip, param) -> str:
    file = read_csv(net_snapshot_path(snapshot_id), sep=";", index_col=['IP address'])
    print (f"{param}: \n {file[param][device_ip]}")

def read_connections_snapshot(snapshot_id):
    with open(connections_snapshot_path(snapshot_id)) as f:
        res = []
        for line in f.readlines()[1:]:
            args = line.split(';')
            res.append((tuple(args[:3]), tuple(args[3:])))
        return res
