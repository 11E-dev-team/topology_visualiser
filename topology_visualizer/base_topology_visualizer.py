import abc


class TopologyVisualizer(abc.ABC):
    topology: dict

    def __init__(self, topology: dict):
        self.topology = topology

    @abc.abstractmethod
    def draw(self, filename: str) -> str:
        pass
