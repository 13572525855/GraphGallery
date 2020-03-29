import numpy as np
import tensorflow as tf
from tensorflow.keras import Model, Input
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import regularizers

from graphgallery.nn.layers import GraphConvolution
from graphgallery.mapper import FullBatchNodeSequence
from .base import SupervisedModel


class GCN_MIX(SupervisedModel):
    
    def __init__(self, adj, features, labels, normalize_rate=-0.5, normalize_features=True, device='CPU:0', seed=None):
    
        super().__init__(adj, features, labels, device=device, seed=seed)
        
        self.normalize_rate = normalize_rate
        self.normalize_features = normalize_features            
        self.preprocess(adj, features)
        
    def preprocess(self, adj, features):
        
        if self.normalize_rate is not None:
            adj = self._normalize_adj(adj, self.normalize_rate)        
            
        if self.normalize_features:
            features = self._normalize_features(features)
            
        features = adj @ features
        
        with self.device:
            self.features, self.adj = self._to_tensor(features), adj
        
    def build(self, hidden_layers=[32], activations=['relu'], dropout=0.5, 
              learning_rate=0.01, l2_norm=5e-4, use_bias=False):
        
        with self.device:
            
            x = Input(batch_shape=[self.n_nodes, self.n_features], dtype=tf.float32, name='features')
            adj = Input(batch_shape=[None, self.n_nodes], dtype=tf.float32, sparse=True, name='adj_matrix')

            h = x
            for hid, activation in zip(hidden_layers, activations):
                h = Dense(hid, use_bias=use_bias, activation=activation, kernel_regularizer=regularizers.l2(l2_norm))(h)
                h = Dropout(rate=dropout)(h)

            output = GraphConvolution(self.n_classes, activation='softmax')([h, adj])

            model = Model(inputs=[x, adj], outputs=output)
            model.compile(loss='sparse_categorical_crossentropy', optimizer=Adam(lr=learning_rate), metrics=['accuracy'])

            self.model = model
            self.built = True
            

    def train_sequence(self, index):
        index = self._check_and_convert(index)
        labels = self.labels[index]
        adj = self.adj[index]
        with self.device:
            sequence = FullBatchNodeSequence([self.features, adj], labels)
        return sequence
        
        
    def predict(self, index):
        super().predict(index)
        index = self._check_and_convert(index)
        
        with self.device:
            adj = self._to_tensor(self.adj[index])
            logit = self.model.predict_on_batch([self.features, adj])
        return logit.numpy()