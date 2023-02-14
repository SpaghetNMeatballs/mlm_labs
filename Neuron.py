from random import uniform


class Neuron:
    def __init__(self, weight_amount: int):
        self.weight = [uniform(-1, 1) for i in range(weight_amount + 1)]
        self.s = 0

    def set_state(self, load: list) -> float:
        try:
            assert len(load) == len(self.weight)
        except AssertionError:
            raise ValueError("Neuron load size is not equal to weight size")
        self.s = sum([self.weight[i] * load[i] for i in range(len(load))])
        return self.s

    def apply_activation(self, activation):
        return activation(self.s)

    def train(self, margins: list) -> None:
        try:
            assert len(margins) == len(self.weight)
        except AssertionError:
            raise ValueError("Margins size is not equal to weight size")
        self.weight = [self.weight[i] + margins[i] for i in range(len(margins))]
