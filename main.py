from one_layer_perceptron import NeuralNet
from TestCase import TestCase

from random import shuffle, uniform
from math import exp, sin, cos
import matplotlib.pyplot as plt


def sigmoid(s: float, alpha: float = 0.2) -> float:
    return 1 / (1 + exp(-alpha * s))


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
        inputs = [uniform(-1, 1) for i in range(3)]
        returnable.append(TestCase(inputs, sin(sum(inputs)), 0))
        returnable.append(TestCase(inputs, cos(sum(inputs)), 1))
    return returnable


if __name__ == "__main__":
    # Генерируем кейсы
    sets_size = 100
    generated_sets = generate_test_set(sets_size)
    # 80% кейсов берём на тренировку
    train_size = int(sets_size * 0.8)
    train_sets = generated_sets[:train_size]
    # 20% оставляем на тестирование
    test_sets = generated_sets[train_size:]
    # Выведем обучающие кейсы
    '''print("x1\t\tx2\t\tx3\t\ty\t\tgroup (0 = sin(sum(x)), 1 = cos(sum(x))")
    for case in train_sets:
        print(case)'''

    # Создаём персептрон, загружаем тренировочные кейсы
    net = NeuralNet(3, 2, sigmoid, 0.2)

    # Запускаем необходимое количество эпох
    epoch_count = 1000
    error_arr = []
    # На каждой эпохе тасуем обучающие кейсы и обучаем нейронку на них
    for i in range(epoch_count):
        shuffle(train_sets)
        net.load_test_sets(train_sets)
        net.train()
        net.load_test_sets(test_sets)
        error_arr.append(net.test())
    # Загрузим тестовые кейсы и посмотрим на их ошибки
    net.load_test_sets(test_sets)
    net.process()
    errors = net.calc_err()
    print("Средняя ошибка по тестам на первом выходе (синус суммы) = %.3f" % errors[0])
    print("Средняя ошибка по тестам на втором выходе (косинус суммы) = %.3f" % errors[1])
    fig, [ax1, ax2] = plt.subplots(2, 1)
    err1 = [err[0] for err in error_arr]
    err2 = [err[1] for err in error_arr]
    ax1.plot([i for i in range(epoch_count)], err1)
    ax2.plot([i for i in range(epoch_count)], err2)
    plt.xscale(value="log")
    plt.show()
