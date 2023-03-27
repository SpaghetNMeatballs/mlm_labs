from PIL import Image
from numpy import array


def inp_to_case(inp: str) -> list[int]:
    result = []
    for i in inp:
        if i == '1':
            result.append(1)
            continue
        result.append(-1)
    return result


class Hopfield:
    def __init__(self, refs: list[list[int]], t: int = 0):
        self.T = t
        self.refs = refs
        self.M = len(refs[0])
        self.N = len(refs)
        self.w = [[0 for j in range(len(refs[0]))] for i in range(len(refs[0]))]
        for i in range(self.M):
            for j in range(self.M):
                if i == j:
                    continue
                self.w[i][j] = sum([self.refs[k][i] * self.refs[k][j] for k in range(self.N)])

    def _activate(self, s: list[int]) -> list[int]:
        result = []
        for element in s:
            if element <= self.T:
                result.append(-1)
                continue
            result.append(1)
        return result

    def _calc_diff(self, q: list[int], q1: list[int]) -> int:
        return sum([q[i] - q1[i] for i in range(len(q))])

    def _find_ref(self, inp: list[int]) -> int:
        for i in range(len(self.refs)):
            ref = self.refs[i]
            if sum([abs(ref[j] - inp[j]) for j in range(len(inp))]) == 0:
                return i
        return -1

    def process(self, inp: list[int]):
        y = [inp.copy()]
        while True:
            s = [sum([self.w[i][j] * y[-1][j] for j in range(self.M)]) for i in range(self.M)]
            y.append(self._activate(s))
            if self._calc_diff(y[-1], y[-2]) == 0:
                break
            if len(y) > 4 and self._calc_diff(y[-1], y[-3]) == 0 and self._calc_diff(y[-2], y[-4]) == 0:
                break
        result = self._find_ref(y[-1])
        if result == -1:
            print("No reference for this input")
            return
        print("Reference identified: ref %d" % (result + 1))


def main():
    refs = [[1, 1, 1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1],
            [1, 1, 1, 1, -1, 1, 1, -1, -1, 1, 1, -1, 1, 1, 1, 1]]
    net = Hopfield(refs)
    net.process(inp_to_case('1111000000001011'))


if __name__ == "__main__":
    main()
