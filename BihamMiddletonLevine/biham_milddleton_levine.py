from argparse import ArgumentParser, RawDescriptionHelpFormatter
from CellGraph import CellGraph, System, COLORS
from random import randint


class BihamLevine(System):
    """modelo de trafico vehicular en el que se tiene una cuadricula llena de
       carros, cada carro tiene una direccion unica(horizontal o vertical).
       Se representa internamente por una matrix llena de numeros, el cero
       indica que no hay carro en la cuadricula, el 1 indica que hay un carro
       que solo se mueve en direccion vertical y el 2 indica que hay un carro
       que solo se mueve en direccion horizontal"""

    def __init__(self, name, width, height, colors):
        matrix = [[0] * width for i in range(height)]
        super(BihamLevine, self).__init__(matrix, name, colors)
        self.width = width
        self.height = height
        self.turn = 0

    def putVerticalCar(self, number):
        ready = number
        while ready != 0:
            i = randint(0, self.height - 1)
            j = randint(0, self.width - 1)

            if not self.matrix[i][j]:
                self.matrix[i][j] = 1
                ready -= 1

    def putHorizontalCar(self, number):
        ready = number
        while ready != 0:
            i = randint(0, self.height - 1)
            j = randint(0, self.width - 1)

            if not self.matrix[i][j]:
                self.matrix[i][j] = 2
                ready -= 1

    def putCars(self, vertical=0, horizontal=0):
        if vertical + horizontal <= self.width * self.height:
            self.putVerticalCar(vertical)
            self.putHorizontalCar(horizontal)

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
                    if (self.matrix[row][column] == 1 and
                            self.matrix[(row + 1) % self.height][column] == 0):
                        self.matrix[(row + 1) % self.height][column] = 1
                        self.matrix[row][column] = 0

    def updateHorizontal(self):
        for row in range(self.height):
            zero = self.findCeroFromRow(row)
            if isinstance(zero, int):
                for j in range(self.width):
                    column = (zero - j) % self.width
                    if (self.matrix[row][column] == 2 and
                            self.matrix[row][(column + 1) % self.width] == 0):
                        self.matrix[row][(column + 1) % self.width] = 2
                        self.matrix[row][column] = 0

    def update(self):
        self.turn = (self.turn + 1) % 2
        if self.turn:
            self.updateVertical()
        else:
            self.updateHorizontal()


def main():
    epilog = '''Modelo Biham Middleton Levine para trafico vehicular. El
programa permite 2 modos de simulacion, el manual en el que se pasa al
siguiente frame de simulacion mediante la pulsacion de la tecla SPACE y otro en
el que se fija los frames por segundo, se puede pausar con la tecla p ademas se
puede tomar una captura de pantalla con la tecla s. EN la simulacionLos se usan
dos tipos de carros, los del tipo 1 son los que solo se mueven en direccion
vertical y los de tipo 2 se mueven solo en direccion horizontal.

Los colores disponibles son:
    - WHITE
    - BLACK
    - CYAN
    - GREEN
    - BLUE
    - YELLOW
    - ORANGE
    - MAGENTA
    - SILVER
    - PURPLE
    - TEAL
    - GRAY
    - RED
    - BROWN
    - GOLDEN'''

    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                            epilog=epilog)

    parser.add_argument('-f', '--filename', default='bihamlevine',
                        dest='name', help='''nombre con el que se guarda la
                        captura de pantalla(si se hace)''')
    parser.add_argument('-w', '--width', type=int, default=10,
                        help='ancho de la calle')
    parser.add_argument('--height', type=int, default=10,
                        help='largo de la calle')
    parser.add_argument('-mw', '--margin-width', type=int, default=0,
                        help='largo de la margen horizontal')
    parser.add_argument('-mh', '--margin-height', type=int, default=0,
                        help='largo de la margen vertical')
    parser.add_argument('-cw', '--cell-width', type=int, default=5,
                        help='ancho horizontal de las celdas(carros)')
    parser.add_argument('-ch', '--cell-height', type=int, default=5,
                        help='ancho vertical de las celdas(carros)')
    parser.add_argument('-sbc', '--separation-between-cells', type=int,
                        default=1, dest='sbc',
                        help='separacion entre las celdas(carros)')
    parser.add_argument('-n1', '--number-cars-type-one', type=int, default=10,
                        help='numero de carros de tipo 1',
                        dest='n1')
    parser.add_argument('-n2', '--number-cars-type-two', type=int, default=10,
                        help='numero de carros de tipo 2',
                        dest='n2')
    parser.add_argument('-bc', '--background-color', type=lambda x: x.upper(),
                        metavar='COLOR', default='BLACK',
                        choices=COLORS.keys(),
                        help='color de fondo, es el mismo que el de la margen')
    parser.add_argument('-sc', '--street-color', type=str,
                        metavar='COLOR', default='WHITE',
                        choices=COLORS.keys(),
                        help='color de fondo de la calle')
    parser.add_argument('-c1', '--car-color-type-one', type=str,
                        metavar='COLOR', default='RED', choices=COLORS.keys(),
                        help='color del carro de tipo 1', dest='color1')
    parser.add_argument('-c2', '--car-color-type-two', type=str,
                        metavar='COLOR', default='GREEN',
                        choices=COLORS.keys(), dest='color2',
                        help='color del carro de tipo 2')
    parser.add_argument('-m', '--manual', action='store_true',
                        help='''si este argumento es pasado la simulaion se
                        debe actualizar manualment presionando la tecla
                        SPACE''')
    parser.add_argument('-fps', '--frame-per-seconds', type=int, dest='fps',
                        default=30, help='''frames por segundo la simulacion
                        corre automaticamente''')

    args = parser.parse_args()

    colors = {1: args.color1, 2: args.color2, 0: args.street_color}

    bihamlevine = BihamLevine(args.name, args.width, args.height, colors)
    bihamlevine.putVerticalCar(args.n1)
    bihamlevine.putHorizontalCar(args.n2)

    graph = CellGraph(bihamlevine, cellwidth=args.cell_width, fps=args.fps,
                      cellheight=args.cell_height,
                      background_color=args.background_color,
                      margin_width=args.margin_width,
                      margin_height=args.margin_height,
                      separation_between_cells=args.sbc)

    graph.run(args.manual)


if __name__ == '__main__':
    main()
