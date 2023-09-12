import dialog
import time
from pandas import *

def select_snapshot():
    answer = input (dialog.init)
    match answer:
        case "1":
            print ("Инициализировать сеть")
        case "2":
            print ("Использовать последний снапшот")
        case "3":
            print ("Выбрать снапшот")
    return snap

def create_snapshot():
    print ("Создание снапшота")
    filename = f"snapshots/net_snapshot{time}.csv"
    with open(filename, "w") as f:
        f.write(dialog.csv_columns)

    return filename

def add_data_to_snapshot(snapshot_name, data):
    print (f"Редактирование {snapshot_name}")
    with open(snapshot_name, "w") as f:
        f.write()

def select_device(snapshot_name):
    with open(snapshot_name, "r") as f:
        ids = f['device_id'].tolist()
        c = 1
        for device in ids:
            print (f"{c} - {device}")
            c+=1
    answer = input("Выберите номер устройства")
    return answer
    
def select_params(snapshot_name):
    with open(snapshot_name, "r") as f:
        c = 1
        params = #list of params
        for param in params:
            print (f"{c} - {param}")
    answer = input("Выберите параметры")
    return answer