import numpy as np

from ..transforms import BaseTransform
from ..get_transform import Transform
from graphgallery.data.preprocess import largest_connected_components
__all__ = ['Standardize']


@Transform.register()
class Standardize(BaseTransform):
    def __init__(self):
        super().__init__()

    def __call__(self, graph):
        # TODO: multiple graph
        assert not graph.multiple
        graph = graph.to_unweighted().to_undirected().eliminate_selfloops()
        graph = largest_connected_components(graph)
        return graph
