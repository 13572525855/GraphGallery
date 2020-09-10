import tensorflow as tf
import numpy as np
import networkx as nx
import scipy.sparse as sp
import graphgallery

from graphgallery.data import Planetoid
data = Planetoid('cora', root="~/GraphData/datasets/", verbose=False)
graph = data.graph
idx_train, idx_val, idx_test = data.split()

print(graph)

from graphgallery.nn.models import Deepwalk

model = Deepwalk(graph, seed=123)
model.build()
model.train(idx_train)
accuracy = model.test(idx_test)
print(f'Test accuracy {accuracy:.2%}')
