from random import randint, random
from math import exp, sin, cos, sqrt
import matplotlib.pyplot as plt


def rand_double(min_inp, max_inp):
    return randint(min_inp, max_inp - 1) + random()


def sigmoid(s: float, alpha: float = 0.2) -> float:
    try:
        return 1 / (1 + exp(-alpha * s))
    except OverflowError:
        print(s)


def arr_shuffle(arr: list) -> list:
    returnable = []
    arr_local = arr.copy()
    cur_size = len(arr_local) - 1
    while cur_size >= 0:
        cur_item = arr_local[randint(0, cur_size)]
        returnable.append(cur_item)
        arr_local.remove(cur_item)
        cur_size -= 1
    return returnable


class TestCase:
    def __init__(self, inputs: list, output: float, group: int):
        self.inputs = inputs
        for i in range(len(self.inputs)):
            self.inputs[i] += 1
            self.inputs[i] /= 2
        self.output = (output + 1) / 2
        self.group = group


def normalize(inp_arr: list) -> list:
    out_arr = []
    min_val = inp_arr[0][1]
    max_val = inp_arr[0][1]
    for i in range(1, len(inp_arr)):
        if inp_arr[i][1] < min_val:
            min_val = inp_arr[i][1]
        if inp_arr[i][1] > max_val:
            max_val = inp_arr[i][1]
    for i in range(len(inp_arr)):
        out_arr.append((inp_arr[i][1] - min_val) / (max_val - min_val))
    return out_arr


def generate_test_set(size: int = 100) -> list[TestCase]:
    returnable = []
    for i in range(size):
        inputs = [rand_double(-1, 1) for i in range(3)]
        returnable.append(TestCase(inputs, sin(sum(inputs)), 0))
        returnable.append(TestCase(inputs, cos(sum(inputs)), 1))
    return returnable


class Neuron:
    def __init__(self, weight_amount: int):
        self.weight = [randint(-5, 5) for i in range(weight_amount + 1)]
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
            self.sets[case.group].append([1] + case.inputs)
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


if __name__ == "__main__":
    # Генерируем кейсы
    sets_size = 100
    generated_sets = generate_test_set(sets_size)
    # 80% кейсов берём на тренировку
    train_size = int(sets_size * 0.8)
    train_sets = generated_sets[:train_size]
    # 20% оставляем на тестирование
    test_sets = generated_sets[train_size:]

    # Создаём персептрон, загружаем тренировочные кейсы
    net = NeuralNet(3, 2, sigmoid, 0.2)

    # Запускаем необходимое количество эпох
    epoch_count = 1000
    error_arr = []
    # На каждой эпохе тасуем обучающие кейсы и обучаем нейронку на них
    for i in range(epoch_count):
        train_sets = arr_shuffle(train_sets)
        net.load_test_sets(train_sets)
        net.train()
        net.load_test_sets(test_sets)
        error_arr.append(net.test())
    # Загрузим тестовые кейсы и посмотрим на их ошибки
    net.load_test_sets(test_sets)
    net.process()
    print(net.calc_err())
    fig, [ax1, ax2] = plt.subplots(2, 1)
    err1 = [err[0] for err in error_arr]
    err2 = [err[1] for err in error_arr]
    ax1.plot([i for i in range(epoch_count)], err1)
    ax2.plot([i for i in range(epoch_count)], err2)
    plt.xscale(value="log")
    plt.show()
