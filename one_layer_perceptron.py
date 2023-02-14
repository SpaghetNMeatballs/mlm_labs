from Neuron import Neuron
from TestCase import TestCase
from math import sqrt


class NeuralNet:
    def __init__(self, inp_amount: int, out_amount: int, activation, v: float = 0.5):
        self.neurons = []
        self.sets = []
        self.response = []
        self.goal_response = []
        self.deltas = []
        self.margins = []
        self.neuron_amount = out_amount
        self.activation = activation
        self.v = v
        for i in range(self.neuron_amount):
            self.neurons.append(Neuron(inp_amount))
        self.flush_all()

    # Функция для сброса кейсов
    def flush_sets(self) -> None:
        self.sets = []
        self.response = []
        self.goal_response = []
        for i in range(self.neuron_amount):
            self.sets.append([])
            self.goal_response.append([])
            self.response.append([])

    # Функция для сброса дельт и шагов
    def flush_deltas(self) -> None:
        self.deltas = []
        self.margins = []
        for i in range(self.neuron_amount):
            self.deltas.append([])
            self.margins.append([])

    def flush_all(self) -> None:
        self.flush_sets()
        self.flush_deltas()

    # Загружает лист тестовых кейсов
    def load_test_sets(self, cases: list[TestCase]) -> None:
        self.flush_sets()
        for case in cases:
            self.sets[case.group].append([1.] + case.inputs)
            self.goal_response[case.group].append(case.output)

    # Прогоняет все сеты из self.sets и получает Yj для каждого нейрона
    def process(self) -> None:
        for i in range(self.neuron_amount):
            for j in range(len(self.sets[i])):
                train_set = self.sets[i][j]
                self.response[i].append(self.activation(self.neurons[i].set_state(train_set)))
                self.deltas[i].append(self.goal_response[i][j] - self.response[i][-1])

    # Получаем шаги изменения весов
    def get_margins(self) -> None:
        for i in range(self.neuron_amount):
            for j in range(len(self.deltas[i])):
                cur_margins = [self.v * self.deltas[i][j] * self.sets[i][j][k] for k in range(len(self.sets[i][j]))]
                self.margins[i].append(cur_margins)

    # Применяем шаги к весам в нейронах
    def apply_margins(self):
        for i in range(self.neuron_amount):
            for j in range(len(self.margins[i])):
                self.neurons[i].train(self.margins[i][j])

    # Функция, по порядку вызывающая получение Yj, расчёт шага и его применение
    def train(self):
        self.process()
        self.get_margins()
        self.apply_margins()
        self.flush_all()

    def test(self) -> list[float]:
        self.process()
        returnable = self.calc_err()
        self.flush_all()
        return returnable

    def calc_err(self) -> list[float]:
        errors = [0 for i in range(self.neuron_amount)]
        for i in range(self.neuron_amount):
            n = len(self.response)
            for j in range(n):
                errors[i] += (self.response[i][j] - self.goal_response[i][j]) ** 2
            errors[i] /= n
            errors[i] = sqrt(errors[i])
        return errors
