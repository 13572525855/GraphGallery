import tensorflow as tf
from tensorflow.keras import Model, Input
from tensorflow.keras.layers import Dropout, Softmax
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import regularizers

from graphgallery.nn.layers import GraphConvolution
from graphgallery.mapper import FullBatchNodeSequence
from .base import SupervisedModel


class GCN(SupervisedModel):
    
    def __init__(self, adj, features, labels, normalize_rate=-0.5, normalize_features=True, device='CPU:0', seed=None):
    
        super().__init__(adj, features, labels, device=device, seed=seed)
        
        if normalize_rate is not None:
            adj = self._normalize_adj(adj, normalize_rate)
            
        if normalize_features:
            features = self._normalize_features(features)
            
        self.features, self.adj = self._to_tensor([features, adj])
        
    def build(self, hidden_layers=[32], activations=['relu'], dropout=0.5, 
              learning_rate=0.01, l2_norm=5e-4, use_bias=False):
        
        with self.device:
            
            x = Input(batch_shape=[self.n_nodes, self.n_features], dtype=tf.float32, name='features')
            adj = Input(batch_shape=[self.n_nodes, self.n_nodes], dtype=tf.float32, sparse=True, name='adj_matrix')
            index = Input(batch_shape=[None],  dtype=tf.int32, name='index')

            h = x
            for hid, activation in zip(hidden_layers, activations):
                h = GraphConvolution(hid, use_bias=use_bias,
                                     activation=activation, 
                                     kernel_regularizer=regularizers.l2(l2_norm))([h, adj])
                
                h = Dropout(rate=dropout)(h)

            h = GraphConvolution(self.n_classes, use_bias=use_bias)([h, adj])
            h = tf.ensure_shape(h, [self.n_nodes, self.n_classes])
            h = tf.gather(h, index)
            output = Softmax()(h)

            model = Model(inputs=[x, adj, index], outputs=output)
            model.compile(loss='sparse_categorical_crossentropy', optimizer=Adam(lr=learning_rate), metrics=['accuracy'])

            self.model = model
            self.built = True
            
    def train_sequence(self, index):
        if self._is_iterable(index):
            return [self.train_sequence(idx) for idx in index]
        else:
            index = self._check_and_convert(index)
            labels = self.labels[index]
            with self.device:
                sequence = FullBatchNodeSequence([self.features, self.adj, index], labels)
            return sequence
        
        
    def predict(self, index):
        if not self.built:
            raise RuntimeError('You must compile your model before training/testing/predicting. Use `model.build()`.')

        if self.do_before_predict is not None:
            self.do_before_predict(idx, **kwargs)

        index = self._check_and_convert(index)

        with self.device:
            index = self._to_tensor(index)
            logit = self.model.predict_on_batch([self.features, self.adj, index])

        return logit.numpy()