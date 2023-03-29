import copy
from random import randint
import array
from os import listdir, mkdir
from PIL import Image


class Generator:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def generate_image(self) -> list[int]:
        result = []
        for i in range(self.height):
            for j in range(self.width):
                result.append(randint(0, 1) * 2 - 1)
        return result

    def generate_initial_bank(self, dirpath: str, bank_size: int) -> None:
        mkdir(dirpath)
        header = f'P6 {self.width} {self.height} 255\n'
        for case_number in range(bank_size):
            temp = self.generate_image()
            image = []
            for i in temp:
                if i == 1:
                    image += [0, 0, 0]
                    continue
                image += [255, 255, 255]
            image = array.array('B', image)
            with open(f'{dirpath}/{case_number + 1}.ppm', 'wb') as f:
                f.write(bytearray(header, 'ascii'))
                image.tofile(f)

    def read_from_files(self, dirname: str) -> list[list[int]]:
        result = []
        for filename in listdir(dirname):
            filepath = dirname + '/' + filename
            im = Image.open(filepath)
            px = im.load()
            result.append([])
            for x in range(im.width):
                for y in range(im.height):
                    if px[x, y] == (0, 0, 0):
                        result[-1].append(-1)
                        continue
                    else:
                        result[-1].append(1)
        return result

    def apply_noise(self, case_dir: str) -> None:
        


if __name__ == "__main__":
    gen = Generator(64, 64)
    gen.generate_initial_bank('amogus', 5)
    print(gen.read_from_files('amogus')[0])
