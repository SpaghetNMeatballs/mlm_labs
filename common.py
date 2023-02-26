from math import exp


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
