from random import uniform
from common import sigmoid, sigmoid_dif


class Neuron:
    def __init__(self, activation: callable, weight_amount: int):
        self.weight = [uniform(-1, 1) for i in range(weight_amount + 1)]
        self.activation = activation
        self.s = 0
        self.y = 0
        self.delta = 0

    def set_state(self, load: list) -> float:
        try:
            assert len(load) == len(self.weight)
        except AssertionError:
            raise ValueError("Neuron load size is not equal to weight size")
        self.s = sum([self.weight[i] * load[i] for i in range(len(load))])
        return self.s

    def apply_activation(self):
        self.y = self.activation(self.s)
        return self.y

    def train(self, margins: list) -> None:
        try:
            assert len(margins) == len(self.weight)
        except AssertionError:
            raise ValueError("Margins size is not equal to weight size")
        self.weight = [self.weight[i] + margins[i] for i in range(len(margins))]


class Layer:
    def __init__(self, size: int, activation: callable, prev_layer: "Layer" = None):
        self.neurons = []
        self.size = size
        for i in range(size):
            self.neurons.append(Neuron(activation, size + 1))
        self.prev_layer = prev_layer
        prev_layer.next_layer = self
        self.next_layer: "Layer" = None
        self.deltas = [0 for i in range(size)]

    def spread_error(self, out_deltas: list[float] = None):
        if out_deltas:
            self.deltas = [out_deltas[i] * sigmoid_dif(self.neurons[i].s) for i in range(self.size)]
        else:
            self.deltas = [sum([self.next_layer.neurons[j].weight[i] * self.next_layer.deltas[j] for j in
                                range(1, len(self.next_layer.neurons))]) * sigmoid_dif(self.neurons[i].s) for i in
                           range(self.size)]
        if self.prev_layer:
            pass
