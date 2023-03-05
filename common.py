from math import exp, sqrt


def sigmoid(s: float, alpha: float = 0.2) -> float:
    return 1 / (1 + exp(-alpha * s))


def sigmoid_dif(s: float, alpha: float = 0.2) -> float:
    return alpha * sigmoid(s, alpha) * (1 - sigmoid(s, alpha))


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


def normalize_keys(keys: list, minmaxes: list) -> list:
    out_arr = []
    for i in range(len(keys)):
        out_arr.append((keys[i] - minmaxes[i][0]) / (minmaxes[i][1] - minmaxes[i][0]))
    return out_arr


def denormalize_values(values: list, minmaxes: list) -> list:
    out_arr = []
    for i in range(len(values)):
        out_arr.append(values[i] * (minmaxes[i][1] - minmaxes[i][0]) + minmaxes[i][0])
    return out_arr


def euclidian(keys, weights):
    try:
        assert len(keys) == len(weights)
    except AssertionError:
        raise Exception("Keys length and weights length does not match")
    return sqrt(sum([(keys[i] - weights[i]) ** 2 for i in range(len(keys))]))
