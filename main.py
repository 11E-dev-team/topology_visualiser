from topology_visualizer.igraph_topology_visualizer import IgraphTopologyVisualizer as default_visualizer

import dialog
import os

import functions as fu
import operations as op
from getpass import getpass
import settings


def snapshot_dialog():
    snapshots = fu.get_snapshots()
    if not snapshots:
        return create_new_snapshot()
    while True:
        option = input(dialog.select_snapshot)
        match option:
            case "1":
                return create_new_snapshot()
            case "2":
                return fu.most_recent_snapshot()
            case "3":
                return fu.select_snapshot(snapshots)
            case _:
                return fu.most_recent_snapshot()
                

def create_new_snapshot():
    snapshot_id = fu.create_snapshot()

    try:
        userdata = dialog.net_access_user_data()
        outer_ip, outer_login, outer_password = userdata['outer']
        entry_ip, entry_login, entry_password = userdata['entry']
        
        main_pxp = op.start_ssh(outer_ip, outer_login, outer_password)

        connections_buffer = []
        data_iterator = op.roam_net(pxp=main_pxp, entry_ip=entry_ip, 
                                    username=entry_login, password=entry_password, 
                                    send_connections=False,
                                    connections_buffer=connections_buffer)

        fu.add_data_to_snapshot(snapshot_id, data_iterator)
        fu.add_connections_data_to_snapshot(snapshot_id, connections_buffer)
        print(f'Образ сети с {snapshot_id} сохранён')
        return snapshot_id
    except Exception as e:
        fu.delete_snapshot(snapshot_id)
        print('[!] Произошла ошибка при создании образа сети. Битые образы удалены')
        raise e


if __name__ == "__main__":
    while True:
        answer = input(dialog.main)
        match answer:
            case "1":
                create_new_snapshot()
            case "2":
                print ("Построить топологию сети")
                snapshot_id = snapshot_dialog()
                connections = {}
                for key, value in fu.read_connections_snapshot(snapshot_id):
                    connections[key] = value

                from topology_visualizer.graphviz_topology_visualizer import GraphvizTopologyVisualizer
                graphname = lambda ip, id, port: (f"{id} - {ip}", port)
                gtv = GraphvizTopologyVisualizer({
                    graphname(*key): graphname(*value) 
                    for key, value in connections.items()
                })
                gtv.draw(input('Имя файла изображения: '))
                print('Схема топологии сохранена')
            case "3":
                snapshot_id = snapshot_dialog()
                print ("Запрос параметров устройтсва")
                device_ip = fu.select_device(snapshot_id)
                param = fu.select_params(snapshot_id)
                print (fu.get_data(snapshot_id, device_ip, param))
            case "4":
                stgdict = settings.read_settings()
                keys = stgdict.keys()
                while True:
                    print('Выберите параметр: ')
                    for key in keys:
                        print(key, f"[{stgdict[key]}]")
                    opt = input()
                    if opt in keys:
                        break
                while True:
                    if opt == 'verbose':
                        print('Выберите значение:')
                        print('0 - только необходимый вывод в консоль')
                        print('1 - подробный вывод в консоль')
                        print('2 - очень подробный вывод в консоль')
                        val = input()
                        if val == '0' or val == '1' or val == '2':
                            break
                    else:
                        print('Впишите значение параметра:')
                        val = input()
                        if val.isdigit():
                            break
                settings.set_setting(key, val)
                print(f'Настройке {key} установлено значение {val}')


            case "0":
                print("Выход из программы")
                break
            case _:
                print("Выберите цифру из списка")
