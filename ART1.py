import random


def beautify_weight(weights: list[float]) -> str:
    result = "+----+\n|"
    for i in range(len(weights)):
        if i % 4 == 0 and i != 0:
            result += '|\n|'
        if weights[i] > 0:
            result += '∎'
        else:
            result += ' '
    result += "|\n+----+"
    return result


def linearize_matrix(matrix: list[list[int]]) -> list[int]:
    result = []
    for row in matrix:
        for element in row:
            result.append(element)
    return result


def rotate_matrix(arr: list[list[int]]) -> list[list[int]]:
    output = []
    for i in range(len(arr[0])):
        output.append([])
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            output[j].append(arr[i][j])
    return output


def generate_tetris() -> list[list[int]]:
    shapes = [
        [
            [1, 1, 1, 1]],
        [
            [1, 0, 0],
            [1, 1, 1]
        ],
        [
            [0, 1, 0],
            [1, 1, 1]
        ],
        [
            [1, 1],
            [1, 1]
        ],
        [
            [1, 1, 0],
            [0, 1, 1]
        ],
        [
            [0, 1, 1],
            [1, 1, 0]
        ]
    ]
    result = shapes[random.randint(0, len(shapes) - 1)]
    while len(result[0]) != 4:
        flag = random.randint(0, 1)
        for i in range(len(result)):
            if flag == 1:
                result[i].append(0)
            else:
                result[i] = [0] + result[i]
    while len(result) != 4:
        if random.randint(0, 1) == 1:
            result.append([0, 0, 0, 0])
        else:
            result = [[0, 0, 0, 0]] + result
    rotations = random.randint(0, 3)
    for i in range(rotations):
        result = rotate_matrix(result)
    return result


if __name__ == "__main__":
    # Константы
    R_CRIT = 0.5
    LAMBDA = 2
    V = 1
    V_DIF = 0.05
    EPOCH_COUNT = int(V / V_DIF)
    DB_SIZE = 10000

    # Инициализация
    db = []
    for i in range(DB_SIZE):
        db.append(linearize_matrix(generate_tetris()))
    w = [[(LAMBDA * db[0][i]) / (LAMBDA - 1 + sum(db[0])) for i in range(len(db[0]))]]
    t = [[db[0][i] for i in range(len(db[0]))]]

    for EPOCH in range(EPOCH_COUNT):
        random.shuffle(db)
        print("Эпоха %d" % (EPOCH + 1))
        # Распознавание образа
        for case in db[1:]:
            y_arr = [sum([neuron[i] * case[i] for i in range(len(case))]) for neuron in w]
            flag = sum(y_arr) != 0
            while flag:
                j = y_arr.index(max(y_arr))
                if y_arr[j] == 0:
                    break
                r = sum([case[i] * t[j][i] for i in range(len(case))]) / sum(case)
                if r > R_CRIT:
                    for i in range(len(w[j])):
                        w[j][i] = (1 - V) * w[j][i] + V * (LAMBDA * case[i]) / (LAMBDA - 1 + sum(db[0]))
                        t[j][i] = (1 - V) * t[j][i] + V * case[i]
                    flag = False
                else:
                    y_arr[j] = 0
            if max(y_arr) == 0:
                w.append([(LAMBDA * case[i]) / (LAMBDA - 1 + sum(case)) for i in range(len(case))])
                t.append([case[i] for i in range(len(case))])
        V -= V_DIF

    stats = [0 for i in w]
    for case in db:
        y_arr = [sum([neuron[i] * case[i] for i in range(len(case))]) for neuron in w]
        stats[y_arr.index(max(y_arr))] += 1
    for i in range(len(w)):
        print('=====Кластер %d=====' % (i + 1))
        print("Количество кейсов в кластере - %d" % stats[i])
        print(beautify_weight(w[i]))
        print('\n\n')

    while True:
        first_row = input("Введите фигуру или -1 чтобы выйти:\n")
        if first_row == "-1":
            break
        rows = [input() for i in range(3)]
        case = []
        for i in first_row:
            case.append(int(i))
        for i in range(3):
            for j in rows[i]:
                case.append(int(j))
        y_arr = [sum([neuron[i] * case[i] for i in range(len(case))]) for neuron in w]
        print("Пример отнесён к кластеру %d" % (1 + y_arr.index(max(y_arr))))
