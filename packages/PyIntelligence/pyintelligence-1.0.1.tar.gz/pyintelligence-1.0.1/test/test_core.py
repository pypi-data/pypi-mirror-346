import numpy as np
import pyml as ml

X = np.array([[0,0], [0,1], [1,0], [1,1]])
Y = np.array([[0], [1], [1], [0]])

model = ml.feedforward(input_size=2)
model.add_layer(nn.dense(2, activation=ml.tanh))
model.add_layer(nn.dense(1, activation=ml.sigmoid))
model.build()
model.train(X, Y, loss=ml.binary_crossentropy, epochs=600, optimizer=ml.adam, plot=True)
model.evaluate(X, Y)
model.summary()
