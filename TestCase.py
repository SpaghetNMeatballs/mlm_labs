class TestCase:
    def __init__(self, inputs: list[float], output: float, group: int):
        self.inputs = inputs
        for i in range(len(self.inputs)):
            self.inputs[i] += 1
            self.inputs[i] /= 2
        self.output = (output + 1) / 2
        self.group = group

    def __str__(self):
        returnable = ""
        for inp in self.inputs:
            returnable += "%.4f\t" % inp
        returnable += "%.4f\t" % self.output
        returnable += "%d" % self.group
        return returnable
