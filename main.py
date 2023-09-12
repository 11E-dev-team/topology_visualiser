from topology_builder import build_topology
from topology_visualizer import visualize_topolgy

from topology_visualizer.igraph_topology_visualizer import IgraphTopologyVisualizer as default_visualizer
# from topology_visualizer.graphviz_topology_visualizer import GraphvizTopologyVisualizer as default_vizualizer

import dialog

import functions as fu
import operations as op

if __name__ == "__main__":
    while True:
        answer = input(dialog.main)
        match answer:
            case "1":
                print ("Инициализировать сеть")
                snapshot_name = fu.create_snapshot()
                main_pxp = op.start_ssh(input("ip: "), input("login: "), input("password: "))
                print ("Подключиться к первой машине")
                pxp = op.start_ssh(input("ip: "), input("login: "), input("password: "), main_pxp)
                print ("Поиск соседей")
                data = op.get_neig_data(pxp)
                fu.add_data_to_snapshot(snapshot_name, data)
            case "2":
                print ("Построить топологию сети")
                snapshot_name = fu.select_snapshot()
                # pxp = op.start_telnet(input("ip: "), input("port: "))
                # data = op.get_neig_data(pxp)
                # pr_data = op.match_neigbours(data)
                # graph = default_visualizer(connections)
                # build_topology()
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
