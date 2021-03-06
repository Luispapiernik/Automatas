from argparse import ArgumentParser, RawDescriptionHelpFormatter
from cellgraph import System, CellGraph, COLORS
from random import randint


class GameOfLife(System):
    """docstring for GameOfLife"""

    def __init__(self, name, width, height, colors, filename=None):
        if filename:
            matrix = self.getMatrixFromFile(filename)
        else:
            matrix = [[0] * width for i in range(height)]

        super(GameOfLife, self).__init__(matrix, colors, name=name, add=False,
                                         possibleValues=[0, 1])

        self.events['mousebuttondown'].append(self.__mouseButtonDown)
        self.events['mousemotion'].append(self.__mouseMotion)
        self.alives = 0

    def __mouseButtonDown(self, pos, _):
        value = super(GameOfLife, self).add(pos, _)

        if value:
            self.alives += 1
        else:
            self.alives -= 1

    def __mouseMotion(self, pos, event):
        if event.buttons[0]:
            value = super(GameOfLife, self).add(pos, event, 1)
            self.alives += int(not value)
        if event.buttons[2]:
            value = super(GameOfLife, self).add(pos, event, 0)
            self.alives -= value

    def getCaption(self):
        return 'Alives: %s' % self.alives

    def putCellsAlives(self, alives):
        ready = alives
        self.alives = alives
        while ready != 0:
            i = randint(0, self.height - 1)
            j = randint(0, self.width - 1)

            if not self.matrix[i][j]:
                self.matrix[i][j] = 1
                ready -= 1

    def countAliveNeighbor(self, i, j):
        alives = 0

        if self.matrix[(i - 1) % self.height][(j - 1) % self.width]:
            alives += 1
        if self.matrix[(i - 1) % self.height][j]:
            alives += 1
        if self.matrix[(i - 1) % self.height][(j + 1) % self.width]:
            alives += 1
        if self.matrix[i][(j - 1) % self.width]:
            alives += 1
        if self.matrix[i][(j + 1) % self.width]:
            alives += 1
        if self.matrix[(i + 1) % self.height][(j - 1) % self.width]:
            alives += 1
        if self.matrix[(i + 1) % self.height][j]:
            alives += 1
        if self.matrix[(i + 1) % self.height][(j + 1) % self.width]:
            alives += 1

        return alives

    def update(self):
        copy = [[0] * self.width for i in range(self.height)]
        self.alives = 0

        for i in range(self.height):
            for j in range(self.width):
                alives = self.countAliveNeighbor(i, j)

                if self.matrix[i][j] and (alives == 3 or alives == 2):
                    copy[i][j] = 1
                    self.alives += 1
                if not self.matrix[i][j] and alives == 3:
                    copy[i][j] = 1
                    self.alives += 1

        self.matrix = copy


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
    epilog = '''Juego de la vida. El programa permite 2 modos de simulacion, el
manual en el que se pasa al siguiente frame de simulacion mediante la pulsacion
de la tecla SPACE y otro en el que se fija los frames por segundo, se puede
pausar con la tecla p ademas se puede tomar una captura de pantalla con la
tecla s, si se presiona la tecla c se limpia el tablero y si se presiona la
tecla e la configuracion del tablero se guarda en un archivo de texto. Se
permite tambien agregar o quitar celulas presionando con el click derecho o
izquierdo respectivamente con el mouse en la celda. El programa tambien permite
cargar configuraciones para el tablero desde un archivo de texto.


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
    parser.add_argument('-o', '--output', default='gameoflife',
                        dest='name', help='''nombre con el que se guarda la
                        captura de pantalla(si se hace)''')
    parser.add_argument('-w', '--width', type=int, default=10,
                        help='numero de celdas horizontales')
    parser.add_argument('-ht', '--height', type=int, default=10,
                        help='numero de celdas verticales')
    parser.add_argument('-mw', '--margin-width', type=int, default=0,
                        help='largo de la margen horizontal')
    parser.add_argument('-mh', '--margin-height', type=int, default=0,
                        help='largo de la margen vertical')
    parser.add_argument('-cw', '--cell-width', type=int, default=5,
                        help='ancho horizontal de las celdas(celulas)')
    parser.add_argument('-ch', '--cell-height', type=int, default=5,
                        help='ancho vertical de las celdas(celulas)')
    parser.add_argument('-sbc', '--separation-between-cells', type=int,
                        default=1, dest='sbc',
                        help='separacion entre las celdas(celulas)')
    parser.add_argument('-a', '--alives', type=int, default=0,
                        help='numero de celulas vivas')
    parser.add_argument('-bc', '--background-color', type=parseColor,
                        metavar='{COLOR, "R G B"}', default='BLACK',
                        help='''color de fondo, es el mismo que el de la
                        margen y la separacion entre celdas''')
    parser.add_argument('-ca', '--color-alive', type=parseColor,
                        metavar='{COLOR, "R G B"}', default='BLACK',
                        help='color de celulas vivas')
    parser.add_argument('-cd', '--color-death', type=parseColor,
                        metavar='{COLOR, "R G B"}', default='WHITE',
                        help='color celulas muertas')
    parser.add_argument('-m', '--manual', action='store_true',
                        help='''si este argumento es pasado la simulacion se
                        debe actualizar manualmente presionando la tecla
                        SPACE''')
    parser.add_argument('-fps', '--frame-per-seconds', type=int, dest='fps',
                        default=30, help='''frames por segundo la simulacion
                        corre automaticamente''')

    args = parser.parse_args()

    colors = {1: args.color_alive, 0: args.color_death}

    gameoflife = GameOfLife(args.name, args.width, args.height, colors,
                            filename=args.filename)
    if not args.filename:
        gameoflife.putCellsAlives(args.alives)

    graph = CellGraph(gameoflife, cellwidth=args.cell_width, fps=args.fps,
                      cellheight=args.cell_height,
                      background_color=args.background_color,
                      margin_width=args.margin_width,
                      margin_height=args.margin_height,
                      separation_between_cells=args.sbc)

    graph.run(args.manual)


if __name__ == '__main__':
    main()
