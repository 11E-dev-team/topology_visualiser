from topology_visualizer.base_topology_visualizer import TopologyVisualizer


class IgraphTopologyVisualizer(TopologyVisualizer):
    def draw(self, filename: str) -> str:
        try:
            import matplotlib.pyplot as plt
        except ModuleNotFoundError:
            print("Установите модуль matplotlib:")
            print("1. pip install matplotlib")
            return None
        try:
            import igraph as ig
        except ModuleNotFoundError:
            print("Установите модуль igraph:")
            print("1. pip install igraph")
            return None

        n_vertices = len(self.topology)
        names = set()
        for (
            key,
            value,
        ) in self.topology.items():
            head, t = key
            tail, h = value

            names.add(head)
            names.add(tail)

        names = sorted(list(set(names)))
        edges = [
            (names.index(key[0]), names.index(value[0]))
            for key, value in self.topology.items()
        ]
        g = ig.Graph(n_vertices, edges)

        g["title"] = "Net"
        g.vs["name"] = names

        fig, ax = plt.subplots(figsize=(5, 5))

        ig.plot(
            g,
            target=ax,
            layout="circle",
            vertex_size=0.1,
            vertex_color="gray",
            vertex_frame_width=4.0,
            vertex_frame_color="white",
            vertex_label=g.vs["name"],
            vertex_label_size=10.0,
            edge_width=2,
            edge_color="black",
        )

        fig.savefig(filename)
        return filename
