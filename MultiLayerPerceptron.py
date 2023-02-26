from Neuron import MultilayerNeuron
from TestCase import TestCase


class MultiLayerPerceptron:
    def __int__(self, inp_amount: int, out_amount: int, layer_amount: int, activation: callable, v: float = 0.5):
        layers = []
        for i in range(layer_amount):
            layers.append([])
            for j in range(inp_amount):
                prev_neurons = None
                if i > 0:
                    prev_neurons = layers[i - 1]
                layers[i].append(MultilayerNeuron(inp_amount + 1, activation, prev_neurons))
