class TestCase:
    def __init__(self, ref: list[int], answer: list[int]):
        self.ref = ref
        self.answer = answer


def str_to_process(inp: str) -> list[int]:
    return [1 if i == '1' else -1 for i in inp]


def str_to_case(inp: str) -> TestCase:
    inner_inp = inp.split('=')
    return TestCase(str_to_process(inner_inp[0]), str_to_process(inner_inp[1]))


class Kosko:
    def __init__(self, cases: list[TestCase], t_ref: list[int] = None, t_answer: list[int] = None):
        self.refs = [i.ref for i in cases]
        self.answers = [i.answer for i in cases]
        self.K = len(self.answers[0])
        self.M = len(self.refs[0])
        self.N = len(self.refs)
        self.w = [[0 for _ in range(self.K)] for _ in range(self.M)]
        self.T_ref = t_ref if t_ref else [0 for _ in range(self.M)]
        self.T_answer = t_answer if t_answer else [0 for _ in range(self.K)]
        for i in range(self.M):
            for j in range(self.K):
                self.w[i][j] = sum([self.refs[k][i] * self.answers[k][j] for k in range(self.N)])

    @staticmethod
    def _activate(s: list[int], t: list[int]) -> list[int]:
        assert (len(s) == len(t))
        result = []
        for i in range(len(s)):
            if s[i] <= t[i]:
                result.append(-1)
                continue
            result.append(1)
        return result

    @staticmethod
    def _calc_diff(q: list[int], q1: list[int]) -> int:
        return sum([q[i] - q1[i] for i in range(len(q))])

    def process(self, x0: list[int]):
        s1 = []
        s2 = []
        x = [x0]
        y = []
        exit_flag = True
        while exit_flag:
            # 14.2
            s1.append([sum([self.w[i][j] * x[-1][i] for i in range(self.M)]) for j in range(self.K)])
            y.append(self._activate(s1[-1], self.T_answer))
            s2.append([sum([self.w[i][j] * y[-1][j] for j in range(self.K)]) for i in range(self.M)])
            x.append(self._activate(s2[-1], self.T_ref))
            if len(x) <= 2:
                continue
            if self._calc_diff(x[-1], x[-2]) == 0:
                exit_flag = False
        return y[-1]


def main():
    case1 = '1001010000101001=111101101'
    case2 = '1111100110011111=101110101'
    cases = [str_to_case(case1), str_to_case(case2)]
    net = Kosko(cases)
    print(net.process(str_to_process('1101010010110001')))


if __name__ == "__main__":
    main()
