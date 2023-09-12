from topology_visualizer.base_topology_visualizer import TopologyVisualizer

DEFAULT_GRAPH_STYLE = {
    "graph": {
        "label": "Network Map",
        "fontsize": "16",
        "fontcolor": "white",
        "bgcolor": "#3F3F3F",
        "rankdir": "BT",
    },
    "nodes": {
        "fontname": "Helvetica",
        "shape": "box",
        "fontcolor": "white",
        "color": "#006699",
        "style": "filled",
        "fillcolor": "#006699",
        "margin": "0.4",
    },
    "edges": {
        "style": "dashed",
        "color": "green",
        "arrowhead": "open",
        "fontname": "Courier",
        "fontsize": "14",
        "fontcolor": "white",
    },
}


class GraphvizTopologyVisualizer(TopologyVisualizer):
    def draw(self, filename: str, style=DEFAULT_GRAPH_STYLE) -> str:
        try:
            import graphviz as gv
        except ModuleNotFoundError:
            print("Установите модуль graphviz:")
            print("1. pip install graphviz")
            print("2. sudo apt install graphviz")
            return None

        def apply_styles(graph, styles):
            graph.graph_attr.update(
                ("graph" in styles and styles["graph"]) or {}
            )
            graph.node_attr.update(
                ("nodes" in styles and styles["nodes"]) or {}
            )
            graph.edge_attr.update(
                ("edges" in styles and styles["edges"]) or {}
            )
            return graph

        nodes = set(
            [
                item[0]
                for item in list(self.topology.keys())
                + list(self.topology.values())
            ]
        )
        graphs = gv.Graph(format="svg"), gv.Graph(format="png")

        for graph in graphs:
            for node in nodes:
                graph.node(node)

            for key, value in self.topology.items():
                head, t_label = key
                tail, h_label = value
                graph.edge(
                    head,
                    tail,
                    headlabel=h_label,
                    taillabel=t_label,
                    label=" " * 12,
                )

            graph = apply_styles(graph, style)
            filename = graph.render(filename=filename)
        return filename
