from tensorflow.keras import Model

from config import Config

from tensorflow.keras.layers import (ZeroPadding2D,
                                     Conv2D,Activation,
                                     Flatten,
                                     BatchNormalization,
                                     Reshape,
                                     Input,
                                     Softmax,
                                     Dense,
                                     Add)

from keras import regularizers

from tensorflow.keras.optimizers import Adadelta
from tensorflow.keras.losses import categorical_crossentropy, mean_squared_error


# VERSION 1 OF THE MODEL
class NNet():
    
    def __init__(self, height, width):
        self.row = height 
        self.column = width 
        
        # Regularization term
        self.reg = 1e-4
        
        self.pi = None
        self.v = None
    
        states = Input(shape=(self.row, self.column, 2))
        print('Initializing model:')
        
        conv = self.conv_block(states)
        print('conv:', conv.shape)
        
        res = self.res_block(conv, Config.res_blocks)
        print('res', res.shape)
        
        self.pi = self.policy_head(res)
        print('pi', self.pi.shape)
        
        self.v = self.value_head(res)
        print('v', self.v.shape)
        
        self.model = Model(inputs = states, outputs = [self.pi, self.v])
        
        self.model.compile(
            optimizer = Adadelta(),
            loss = [categorical_crossentropy, mean_squared_error],
            loss_weights = [0.5, 0.5],
            metrics=["accuracy"])
        
        
    def conv_block(self, input_layer):
        # Convolutional Block
        layer = ZeroPadding2D((2, 2))(input_layer)
        layer = Conv2D(256, (3, 3), padding = "valid", kernel_regularizer = regularizers.l2(self.reg))(layer)
        layer = Activation("relu")(layer)
        layer = Conv2D(256, (3, 3), padding = "valid", kernel_regularizer = regularizers.l2(self.reg))(layer)
        layer = BatchNormalization()(layer)
        layer = Activation("relu")(layer)

        return layer

    def res_block(self, input_layer, res_n):
        
        # Residual Block
        for i in range(res_n):
            
            layer = ZeroPadding2D((2, 2))(input_layer)
            layer = Conv2D(256, (3, 3), padding = "valid", kernel_regularizer = regularizers.l2(self.reg))(layer)
            layer = Activation("relu")(layer)
            layer = Conv2D(256, (3, 3), padding = "valid", kernel_regularizer = regularizers.l2(self.reg))(layer)
            layer = BatchNormalization()(layer)
            layer = Add()([layer, input_layer])
            resnet_out = Activation("relu")(layer)
            input_layer = resnet_out
            
        return resnet_out
    
    def policy_head(self, input_layer):
        
        phead = input_layer
        #phead = Conv2D(7, (6, 1), padding = "valid", kernel_regularizer = keras.regularizers.l2(self.reg))(phead)
        #phead = Activation("relu")(phead)
        phead = Conv2D(2, (1, 1), padding = "valid", kernel_regularizer = regularizers.l2(self.reg))(phead)
        phead = BatchNormalization()(phead)
        phead = Activation("relu")(phead)
        phead = Flatten()(phead)
        phead = Dense(7)(phead)
        p = Softmax(name = "policy_head")(phead)
        
        return p
    
    def value_head(self, input_layer):
        
        vhead = Conv2D(1, (1, 1), kernel_regularizer = regularizers.l2(self.reg))(input_layer)
        vhead = BatchNormalization()(vhead)
        vhead = Activation("relu")(vhead)
        vhead = Flatten()(vhead)
        vhead = Dense(256)(vhead)
        vhead = Activation("relu")(vhead)
        vhead = Dense(1)(vhead)
        v = Activation("tanh", name = "vh")(vhead)
        
        return v
    
            
    