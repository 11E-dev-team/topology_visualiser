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
                if os.path.isfile("login_data.txt"):
                    use_saved_login_data = input("Использовать сохрененные данные для входа в сеть? [Д/н]: ")
                    if not use_saved_login_data or use_saved_login_data.find("н") != -1:
                        with open("login_data.txt") as f:
                            login_data = f.readlines()[:3]
                    else:
                        login_data = [input("ip: "), input("login: "), getpass("password: ")]
                else:
                    login_data = [input("ip: "), input("login: "), getpass("password: ")]
                main_pxp = op.start_ssh(login_data[0], login_data[1], login_data[2])
                print('Подключение к первой машине в сети')
                if os.path.isfile("login_data1.txt"):
                    use_saved_login_data = input("Использовать сохрененные данные для входа в сеть? [Д/н]: ")
                    if not use_saved_login_data or use_saved_login_data.find("н") != -1:
                        with open("login_data1.txt") as f:
                            login_data = f.readlines()[:3]
                    else:
                        login_data = [input("ip: "), input("login: "), getpass("password: ")]
                else:
                    login_data = [input("ip: "), input("login: "), getpass("password: ")]
                for device in op.roam_net(pxp=main_pxp, entry_ip=input("ip: "), 
                                          username=input('login: '), password=getpass('password: '), 
                                          send_connections=False):
                    fu.add_data_to_snapshot(snapshot_name, op.parse_neighbors(device))
            case "2":
                print ("Построить топологию сети")
                main_pxp = op.start_ssh(input("ip: "), input("login: "), getpass("password: "))
                print('Подключение к первой машине в сети')
                connections = {key: value for key, value in op.roam_net(
                    pxp=main_pxp, entry_ip=input("ip: "), username=input('login: '), 
                    password=getpass('password: '), send_connections=True
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
            case _:
                print("Выберите цифру из списка")
