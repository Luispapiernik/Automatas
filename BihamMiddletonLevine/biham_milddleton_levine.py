from argparse import ArgumentParser, RawDescriptionHelpFormatter
from cellgraph import CellGraph, System, COLORS
from random import randint


class BihamLevine(System):
    """modelo de trafico vehicular en el que se tiene una cuadricula llena de
       carros, cada carro tiene una direccion unica(horizontal o vertical).
       Se representa internamente por una matrix llena de numeros, el cero
       indica que no hay carro en la cuadricula, el 1 indica que hay un carro
       que solo se mueve en direccion vertical y el 2 indica que hay un carro
       que solo se mueve en direccion horizontal"""

    def __init__(self, name, width, height, colors, filename=None):
        if filename:
            matrix = self.getMatrixFromFile(filename)
        else:
            matrix = [[0] * width for i in range(height)]

        super(BihamLevine, self).__init__(matrix, colors, name=name,
                                          possibleValues=[0, 1, 2])

        self.turn = 0

    def __putCars(self, number, tp):
        """tipo 1 para vertical, tipo 2 para horizontal"""
        ready = number
        while ready != 0:
            i = randint(0, self.height - 1)
            j = randint(0, self.width - 1)

            if not self.matrix[i][j]:
                self.matrix[i][j] = tp
                ready -= 1

    def putCars(self, vertical=0, horizontal=0):
        if vertical + horizontal <= self.width * self.height:
            self.__putCars(vertical, 1)
            self.__putCars(horizontal, 2)

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


def validateColor(color):
    if len(color) == 3:
        return all(map(lambda x: isinstance(x, int) and 0 <= x <= 255, color))
    return False


def parseColor(string):
    if string.isalpha():
        return COLORS.get(string.upper(), (0, 0, 0))

    color = [filter(lambda x: x.isdigit(), num) for num in string.split()]
    color = tuple(map(int, color))
    if validateColor(color):
        return color

    return (0, 0, 0)


def main():
    epilog = '''Modelo Biham Middleton Levine para trafico vehicular. El
programa permite 2 modos de simulacion, el manual en el que se pasa al
siguiente frame de simulacion mediante la pulsacion de la tecla SPACE y otro en
el que se fija los frames por segundo, se puede pausar con la tecla p ademas se
puede tomar una captura de pantalla con la tecla s, si se presiona la tecla c
se limpia el tablero y si se presiona la tecla e la configuracion del tablero
se guarda en un archivo de texto. En la simulacion se usan dos tipos de
carros, los del tipo 1 son los que solo se mueven en direccion vertical y los
de tipo 2 se mueven solo en direccion horizontal. Se permite tambien agregar
vehiculos presionando con el mouse la posicion a la que se desea agregar. El
programa tambien permite cargar configuraciones para el tablero desde un
archivo de texto.

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

    parser.add_argument('-f', '--filename', default=None,
                        help='''Archivo con la configuracion
                        inicial del tablero''')
    parser.add_argument('-o', '--output', default='bihamlevine',
                        dest='name', help='''nombre con el que se guarda la
                        captura de pantalla(si se hace)''')
    parser.add_argument('-w', '--width', type=int, default=10,
                        help='ancho de la calle')
    parser.add_argument('-ht', '--height', type=int, default=10,
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
    parser.add_argument('-bc', '--background-color', type=parseColor,
                        metavar='{COLOR, "R G B"}', default='BLACK',
                        help='color de fondo, es el mismo que el de la margen')
    parser.add_argument('-sc', '--street-color', type=parseColor,
                        metavar='{COLOR, "R G B"}', default='WHITE',
                        help='color de fondo de la calle')
    parser.add_argument('-c1', '--car-color-type-one', type=parseColor,
                        metavar='{COLOR, "R G B"}', default='RED',
                        dest='color1', help='color del carro de tipo 1')
    parser.add_argument('-c2', '--car-color-type-two', type=parseColor,
                        metavar='{COLOR, "R G B"}', default='GREEN',
                        dest='color2', help='color del carro de tipo 2')
    parser.add_argument('-m', '--manual', action='store_true',
                        help='''si este argumento es pasado la simulaion se
                        debe actualizar manualment presionando la tecla
                        SPACE''')
    parser.add_argument('-fps', '--frame-per-seconds', type=int, dest='fps',
                        default=30, help='''frames por segundo la simulacion
                        corre automaticamente''')

    args = parser.parse_args()

    colors = {1: args.color1, 2: args.color2, 0: args.street_color}

    bihamlevine = BihamLevine(args.name, args.width, args.height, colors,
                              filename=args.filename)
    bihamlevine.putCars(vertical=args.n1)
    bihamlevine.putCars(horizontal=args.n2)

    graph = CellGraph(bihamlevine, cellwidth=args.cell_width, fps=args.fps,
                      cellheight=args.cell_height,
                      background_color=args.background_color,
                      margin_width=args.margin_width,
                      margin_height=args.margin_height,
                      separation_between_cells=args.sbc)

    graph.run(args.manual)


if __name__ == '__main__':
    main()
