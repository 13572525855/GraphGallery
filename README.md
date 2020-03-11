# GraphGallery

TensorFlow 2 implementation of state-of-the-arts deep learning graph models.

# Requirements

+ Python 3.7

+ Tensorflow 2.1

+ Scipy

+ Sklearn

+ Networkx

+ Numpy

+ Numba

# Usage

## Inputs

+ adj: scipy.sparse_matrix, shape [N, N], adjacency matrix.
+ features: np.ndarray shape [N, F], feature matrix.
+ labels: np.ndarray shape [N, ], labels of all nodes.
+ idx_train, idx_val, idx_test: np.ndarray, the indices of training, validation and test nodes.

You can specified training details by call `model.build(args)`.

## GCN

```python
from graphgallery.nn.models import GCN
model = GCN(adj, features, labels, device='CPU:0', seed=123)
train_data = model.train_sequence(idx_train)
val_data, test_data = model.test_sequence((idx_val, idx_test))
model.build()
his = model.train(train_data, val_data, verbose=10, epochs=100)
loss, accuracy = model.test(test_data)
model.close
print(f'Test loss {loss:.5}, Test accuracy {accuracy:.2%}')
```



## DenceGCN

```python
from graphgallery.nn.models import DenseGCN
model = DenseGCN(adj, features, labels, device='CPU:0', seed=123)
train_data = model.train_sequence(idx_train)
val_data, test_data = model.test_sequence((idx_val, idx_test))
model.build()
his = model.train(train_data, val_data, verbose=10, epochs=100)
loss, accuracy = model.test(test_data)
model.close
print(f'Test loss {loss:.5}, Test accuracy {accuracy:.2%}')
```



## ChebyGCN

```python
from graphgallery.nn.models import ChebyGCN
model = ChebyGCN(adj, features, labels, order=2, device='CPU:0', seed=123)
train_data = model.train_sequence(idx_train)
val_data, test_data = model.test_sequence((idx_val, idx_test))
model.build()
his = model.train(train_data, val_data, verbose=10, epochs=100)
loss, accuracy = model.test(test_data)
model.close
print(f'Test loss {loss:.5}, Test accuracy {accuracy:.2%}')
```

## FastGCN

```python
from graphgallery.nn.models import FastGCN
model = FastGCN(adj, features, labels, device='CPU:0', seed=123)
train_data = model.train_sequence(idx_train)
val_data, test_data = model.test_sequence((idx_val, idx_test))
model.build()
his = model.train(train_data, val_data, verbose=10, epochs=100)
loss, accuracy = model.test(test_data)
model.close
print(f'Test loss {loss:.5}, Test accuracy {accuracy:.2%}')
```

## GraphSAGE

```python
from graphgallery.nn.models import GraphSAGE
model = GraphSAGE(adj, features, labels, n_samples=[10, 5], device='CPU:0', seed=123)
train_data = model.train_sequence(idx_train)
val_data, test_data = model.test_sequence((idx_val, idx_test))
model.build()
his = model.train(train_data, val_data, verbose=10, epochs=100)
loss, accuracy = model.test(test_data)
model.close
print(f'Test loss {loss:.5}, Test accuracy {accuracy:.2%}')
```

## RobustGCN

```python
from graphgallery.nn.models import RobustGCN
model = RobustGCN(adj, features, labels, device='CPU:0', seed=123)
train_data = model.train_sequence(idx_train)
val_data, test_data = model.test_sequence((idx_val, idx_test))
model.build()
his = model.train(train_data, val_data, verbose=10, epochs=100)
loss, accuracy = model.test(test_data)
model.close
print(f'Test loss {loss:.5}, Test accuracy {accuracy:.2%}')
```

## SGC

```python
from graphgallery.nn.models import SGC
model = SGC(adj, features, labels, device='CPU:0', seed=123)
train_data = model.train_sequence(idx_train)
val_data, test_data = model.test_sequence((idx_val, idx_test))
model.build()
his = model.train(train_data, val_data, verbose=10, epochs=100)
loss, accuracy = model.test(test_data)
model.close
print(f'Test loss {loss:.5}, Test accuracy {accuracy:.2%}')
```

## GWNN

```python
from graphgallery.nn.models import GWNN
model = GWNN(adj, features, labels, device='CPU:0', seed=123)
train_data = model.train_sequence(idx_train)
val_data, test_data = model.test_sequence((idx_val, idx_test))
model.build()
his = model.train(train_data, val_data, verbose=10, epochs=100)
loss, accuracy = model.test(test_data)
model.close
print(f'Test loss {loss:.5}, Test accuracy {accuracy:.2%}')
```

## GAT

```python
from graphgallery.nn.models import GAT
model = GAT(adj, features, labels, device='CPU:0', seed=123)
train_data = model.train_sequence(idx_train)
val_data, test_data = model.test_sequence((idx_val, idx_test))
model.build()
his = model.train(train_data, val_data, verbose=10, epochs=100)
loss, accuracy = model.test(test_data)
model.close
print(f'Test loss {loss:.5}, Test accuracy {accuracy:.2%}')
```

## ClusterGCN

```python
from graphgallery.nn.models import ClusterGCN
model = ClusterGCN(Data.adj, Data.features, data.labels, n_cluster=10, device='CPU:0', seed=123)
train_data = model.train_sequence(data.idx_train)
val_data, test_data = model.test_sequence((data.idx_val, data.idx_test))
model.build()
his = model.train(train_data, val_data, verbose=10, epochs=50)
loss, accuracy = model.test(test_data)
model.close
print(f'Test loss {loss:.5}, Test accuracy {accuracy:.2%}')
```

## Deepwalk

```python
from graphgallery.nn.models import Deepwalk
model = Deepwalk(adj, features, labels)
model.build()
model.train(idx_train)
accuracy = model.test(idx_test)
print(f'Test accuracy {accuracy:.2%}')
```

## Node2vec

```python
from graphgallery.nn.models import Node2vec
model = Node2vec(adj, features, labels)
model.build()
model.train(idx_train)
accuracy = model.test(idx_test)
print(f'Test accuracy {accuracy:.2%}')
```

