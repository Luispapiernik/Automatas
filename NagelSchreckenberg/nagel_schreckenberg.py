from __future__ import division

from cellgraph import CellGraph, System, COLORS
from random import randint, random


class NagelSchreckenberg(System):
    """1: (1, 0), 2: (0, 1), 3: (-1, 0), 4: (0, -1) directions,
       un carro sera representado por una lista (velocidad, direccion)"""

    def __init__(self, name, colors, width=0, height=0, filename=None, vmax=5,
                 breakProbability=0.5, turnProbability=0.5):
        if filename:
            matrix, width, height = self.getMatrixFromFile(filename)
        else:
            matrix = [[[0, 0]] * width for i in range(height)]

        super(NagelSchreckenberg, self).__init__(matrix, colors, width=width,
                                                 height=height)

        self.turnProbability = turnProbability
        self.breakProbability = breakProbability
        self.vmax = vmax

    def getMatrixFromFile(self, filename):
        """en el se especifica la velocidad del carro y al lado su direccion"""

        matrix = super(NagelSchreckenberg, self).getMatrixFromFile(filename)

        width = len(matrix[0])
        height = len(matrix)

        output = [[0] * (width // 2) for i in range(height)]

        for i in range(height):
            for j in range(0, width, 2):
                output[i][j // 2] = matrix[i][j:j + 2]

        return output, width // 2, height

    def getColor(self, i, j):
        return self.colors.get(self.matrix[i][j][0], 'BLACK')

    def putVerticalCar(self, number):
        ready = number
        while ready != 0:
            i = randint(0, self.height - 1)
            j = randint(0, self.width - 1)

            if self.matrix[i][j] == [-1, -1]:
                self.matrix[i][j] = [randint(0, self.vmax), 4]
                ready -= 1

    def putHorizontalCar(self, number):
        ready = number
        while ready != 0:
            i = randint(0, self.height - 1)
            j = randint(0, self.width - 1)

            if self.matrix[i][j] == [-1, -1]:
                self.matrix[i][j] = [randint(0, self.vmax), 1]
                ready -= 1

    def putCars(self, vertical=0, horizontal=0):
        if vertical + horizontal <= self.width * self.height:
            self.putVerticalCar(vertical)
            self.putHorizontalCar(horizontal)

    def findPredecessorDistant(self, i, j):
        distant = 0

        if self.matrix[i][j][1] == 1:
            while distant <= self.width:
                if self.matrix[i][(j + distant) % self.width]:
                    break
                distant += 1
        else:
            while distant <= self.height:
                if self.matrix[(i + distant) % self.height][j]:
                    break
                distant += 1

        return distant

    def breakForInteraction(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.matrix[i][j][0] != -1:
                    distant = self.findPredecessorDistant(i, j)
                    self.matrix[i][j][0] = min(distant, self.matrix[i][j][0])

    def breakProbability(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.breakProbability > random():
                    self.matrix[i][j][0] = min(self.matrix[i][j][0] - 1, 0)

    def updateVelocity(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.matrix[i][i][0] != -1:
                    self.matrix[i][j][0] = min(self.vmax, self.matrix[i][j][0] + 1)

    def findCeroFromColumn(self, column):
        for i in range(self.height):
            if self.matrix[i][column] == 0:
                return i

    def findCeroFromRow(self, row):
        for j in range(self.width):
            if self.matrix[row][j] == 0:
                return j

    def updateVertical(self):
        for column in range(self.width):
            zero = self.findCeroFromColumn(column)
            if isinstance(zero, int):
                for i in range(self.height):
                    row = (zero - i) % self.height
                    # distant self.matrix[row][column][0]
                    if (self.matrix[row][column] != -1 and self.matrix[(row + self.matrix[row][column][0]) % self.height][column] == -1 and self.matrix[i][j][1] == 1):
                        self.matrix[(row + self.matrix[row][column][0]) % self.height][column] = 1
                        self.matrix[row][column] = [-1, -1]

    def updateHorizontal(self):
        for row in range(self.height):
            zero = self.findCeroFromRow(row)
            if isinstance(zero, int):
                for j in range(self.width):
                    column = (zero - j) % self.width
                    # distant self.matrix[row][column][0]
                    if (self.matrix[row][column] != -1 and self.matrix[row][(column + self.matrix[row][column][0]) % self.width] == -1 and self.matrix[i][j][1] == 4):
                        self.matrix[row][(column + self.matrix[row][column][0]) % self.width] = 2
                        self.matrix[row][column] = [-1, -1]

    def update(self):
        self.updateVelocity()
        self.updateVertical()
        self.updateHorizontal()


def main():
    colors = {0: 'BLACK', 1: 'RED', 2: 'BLUE', 3: 'YELLOW', 4: 'ORANGE',
              -1: 'WHITE'}

    nagel = NagelSchreckenberg('nagel', colors, filename='prueba.txt', vmax=4)

    print(nagel.matrix)

    # nagel.putCars(20, 20)

    # graph = CellGraph(nagel, fps=20)

    # graph.run(True)


if __name__ == '__main__':
    main()
