from topology_builder import build_topology
from topology_visualizer import visualize_topolgy

from topology_visualizer.igraph_topology_visualizer import IgraphTopologyVisualizer as default_visualizer
# from topology_visualizer.graphviz_topology_visualizer import GraphvizTopologyVisualizer as default_vizualizer

import operations as op

if __name__ == "__main__":
    while True:
        answer = input(
            """1 - Построение топологии
0 - Выход из программы\n"""
        )

        match answer:
            case "1":
                print("Построение топологии")
                pxp = op.start_telnet(input("ip: "), input("port: "))
                data = op.get_neig_data(pxp)
                pr_data = op.match_neigbours(data)
                graph = default_visualizer(connections)
                build_topology()
            case "0":
                print("Выход из программы")
            case _:
                print("Выберите цифру из списка")
