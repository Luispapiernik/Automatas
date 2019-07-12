from argparse import ArgumentParser, RawDescriptionHelpFormatter
from cellgraph import CellGraph, System, COLORS
from copy import deepcopy


class WireWorld(System):
    """0 no hay nada, 1 es el elemento conductor, 2 es el electron tail, el
       3 es el electron head"""

    def __init__(self, colors, width=None, height=None, filename=None):
        if filename:
            matrix = self.getMatrixFromFile(filename)
        else:
            matrix = [[0] * width for i in range(height)]

        super(WireWorld, self).__init__(matrix, colors, name='Wire World',
                                        possibleValues=[0, 1, 2, 3])

        self.events['mousemotion'].append(self.__mouseMotion)
        self.events['keydown'].append(self.__keydown)

        self.delete = 1

    def __mouseMotion(self, pos, event):
        if event.buttons[0]:
            super(WireWorld, self).add(pos, event, self.delete)

    def __keydown(self, key):
        if key == 'd':
            print('delete mode')
            self.delete = 0
        if key == 'a':
            print('add mode')
            self.delete = 1

    def aliveNeighbors(self, i, j):
        alive = 0

        for r in range(-int(0 < i), int(i < self.height - 1) + 1):
            for c in range(-int(0 < j), int(j < self.width - 1) + 1):
                if (r != 0 or c != 0) and self.matrix[i + r][j + c] == 3:
                    alive += 1

        return alive

    def update(self):
        copy = deepcopy(self.matrix)

        for i in range(self.height):
            for j in range(self.width):
                if self.matrix[i][j] == 3:
                    copy[i][j] = 2
                if self.matrix[i][j] == 2:
                    copy[i][j] = 1
                if self.matrix[i][j] == 1:
                    alive = self.aliveNeighbors(i, j)
                    if alive == 2 or alive == 1:
                        copy[i][j] = 3

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
    epilog = '''El programa permite 2 modos de simulacion, el
manual en el que se pasa al siguiente frame de simulacion mediante la pulsacion
de la tecla SPACE y otro en el que se fija los frames por segundo, se puede
pausar con la tecla p ademas se puede tomar una captura de pantalla con la
tecla s, si se presiona la tecla c se limpia el tablero y si se presiona la
tecla e la configuracion del tablero se guarda en un archivo de texto. Se
permite tambien agregar o quitar elementos presionando con el click derecho o
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
    parser.add_argument('-bc', '--background-color', type=parseColor,
                        metavar='{COLOR, "R G B"}', default='BLACK',
                        help='''color de fondo, es el mismo que el de la
                        margen y la separacion entre celdas''')
    parser.add_argument('-ce', '--color-empty', type=parseColor,
                        metavar='{COLOR, "R G B"}', default='BLACK',
                        help='color de celula vacia')
    parser.add_argument('-cc', '--color-conductor', type=parseColor,
                        metavar='{COLOR, "R G B"}', default='YELLOW',
                        help='color celula conductora')
    parser.add_argument('-ct', '--color-tail', type=parseColor,
                        metavar='{COLOR, "R G B"}', default='RED',
                        help='color de electron cola')
    parser.add_argument('-cH', '--color-head', type=parseColor,
                        metavar='{COLOR, "R G B"}', default='BLUE',
                        help='color celula electron cabeza')
    parser.add_argument('-m', '--manual', action='store_true',
                        help='''si este argumento es pasado la simulacion se
                        debe actualizar manualmente presionando la tecla
                        SPACE''')
    parser.add_argument('-fps', '--frame-per-seconds', type=int, dest='fps',
                        default=30, help='''frames por segundo la simulacion
                        corre automaticamente''')

    args = parser.parse_args()

    colors = {0: args.color_empty, 1: args.color_conductor,
              2: args.color_tail, 3: args.color_head}

    gameoflife = WireWorld(colors, args.width, args.height,
                           filename=args.filename)

    graph = CellGraph(gameoflife, cellwidth=args.cell_width, fps=args.fps,
                      cellheight=args.cell_height,
                      background_color=args.background_color,
                      margin_width=args.margin_width,
                      margin_height=args.margin_height,
                      separation_between_cells=args.sbc)

    graph.run(args.manual)


if __name__ == '__main__':
    main()
