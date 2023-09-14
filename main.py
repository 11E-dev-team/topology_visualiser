from topology_visualizer.igraph_topology_visualizer import IgraphTopologyVisualizer as default_visualizer
# from topology_visualizer.graphviz_topology_visualizer import GraphvizTopologyVisualizer as default_vizualizer

import dialog
import os

import functions as fu
import operations as op
from getpass import getpass

if __name__ == "__main__":
    while True:
        answer = input(dialog.main)
        match answer:
            case "1":
                print ("Инициализировать сеть")
                snapshot_name = fu.create_snapshot()

                userdata = dialog.net_access_user_data()
                outer_ip, outer_login, outer_password = userdata['outer']
                entry_ip, entry_login, entry_password = userdata['entry']
                
                main_pxp = op.start_ssh(outer_ip, outer_login, outer_password)
                fu.add_data_to_snapshot(snapshot_name, 
                                        op.roam_net(pxp=main_pxp, entry_ip=entry_ip, 
                                                    username=entry_login, password=entry_password, 
                                                    send_connections=False))
            case "2":
                print ("Построить топологию сети")
                userdata = dialog.net_access_user_data()
                outer_ip, outer_login, outer_password = userdata['outer']
                entry_ip, entry_login, entry_password = userdata['entry']

                main_pxp = op.start_ssh(outer_ip, outer_login, outer_password)
                print('Подключение к первой машине в сети')
                connections = {key: value for key, value in op.roam_net(
                    pxp=main_pxp, entry_ip=entry_ip, username=entry_login, 
                    password=entry_password, send_connections=True
                )}
                print(connections)
                for key, value in list(connections.items()):
                    if value in connections:
                        del connections[key]
                print(connections)
                from topology_visualizer.graphviz_topology_visualizer import GraphvizTopologyVisualizer
                gtv = GraphvizTopologyVisualizer(connections)
                gtv.draw(input('Имя файла изображения: '))
                print('Схема топологии сохранена')
            case "3":
                snapshot_name = fu.select_snapshot()
                print ("Запрос параметров устройтсва")
                device_id = fu.select_device(snapshot_name)
                params = fu.select_params(snapshot_name)
            case "4":
                snapshot_name = fu.select_snapshot()
                print ("Выполнить команды в конфигурационном режиме")
            case "5":
                snapshot_name = fu.select_snapshot()
                print ("Выполнить команды и записать их вывод")
            case "0":
                print("Выход из программы")
                break
            case _:
                print("Выберите цифру из списка")
