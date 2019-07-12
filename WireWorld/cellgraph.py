import pygame.locals as pl
from os.path import exists
import pygame as p


_events = None

COLORS = {'WHITE': (255, 255, 255), 'BLACK': (0, 0, 0), 'CYAN': (0, 255, 255),
          'GREEN': (0, 255, 0), 'BLUE': (0, 0, 255), 'YELLOW': (255, 255, 0),
          'ORANGE': (255, 165, 0), 'MAGENTA': (255, 0, 255),
          'SILVER': (192, 192, 192), 'PURPLE': (128, 0, 128),
          'TEAL': (0, 128, 128), 'GRAY': (128, 128, 128), 'RED': (255, 0, 0),
          'BROWN': (165, 42, 42), 'GOLDEN': (255, 215, 0)}


def setEvents():
    global _events

    _events = p.event.get()

    return _events


class System(object):
    def __init__(self, matrix, colors, possibleValues=[], name='system',
                 nullCell=0, clear=True, export=True, add=True, width=0,
                 height=0):
        """matrix representa el sistema cada numero en la matrix representa un
           color. Colors es un diccionario con numeros como claves y tuplas en
           formato (R, G, B) como valor, possibleValues son los posibles
           valores que hay en la matrix. name es el nombre del sistema.
           nullCell es un entero que representa a una celda en la que no hay
           nada. clear, export, add se usa para activar dichas funciones"""
        self.width = width or len(matrix[0])
        self.height = height or len(matrix)
        self.nullCell = nullCell
        self.colors = colors
        self.matrix = matrix
        self.possibleValues = possibleValues
        self.lenValues = len(self.possibleValues)
        self.name = name
        self.events = {'keydown': [], 'keyup': [], 'mousebuttondown': [],
                       'mousebuttonup': [], 'mousemotion': []}
        if clear:
            self.events['keydown'].append(self.clear)
        if export:
            self.events['keydown'].append(self.export)
        if add:
            self.events['mousebuttondown'].append(self.add)

    def getMatrixFromFile(self, filename):
        matrix = []

        with open(filename, 'r') as fichero:
            for line in fichero:
                matrix.append(list(map(int, line.replace('\n', ''))))

        return matrix

    def getColor(self, i, j):
        return self.colors.get(self.matrix[i][j], 'BLACK')

    def getCaption(self):
        return self.name

    def getName(self, extention='png'):
        number = 0
        while True:
            name = self.name + str(number) + '.' + extention
            if not exists(name):
                return name
            number += 1

    def clear(self, key):
        """limpia el tablero"""
        if key == 'c':
            self.matrix = [[self.nullCell] *
                           self.width for i in range(self.height)]

    def export(self, key):
        """exporta el tablero a un archivo txt"""
        if key == 'e':
            with open(self.getName('txt'), 'w') as fichero:
                for line in self.matrix:
                    fichero.write(''.join(list(map(str, line))) + '\n')
            print('Text saved')

    def add(self, pos, _, added=None):
        """agrega celulas al tablero y retorna el valor agregado en caso de no
           pasar una valor a ser agregado"""
        x, y = pos
        if 0 <= x < self.width and 0 <= y < self.height:
            # added in self.possibleValues
            if isinstance(added, int):
                value = self.matrix[y][x]
                self.matrix[y][x] = added
                return value

            ind = self.possibleValues.index(self.matrix[y][x])
            self.matrix[y][x] = self.possibleValues[(ind + 1) % self.lenValues]
            return self.matrix[y][x]

    def keyDown(self, key):
        for function in self.events['keydown']:
            function(key)

    def keyUp(self, key):
        for function in self.events['keyup']:
            function(key)

    def mouseButtonDown(self, pos, event):
        for function in self.events['mousebuttondown']:
            function(pos, event)

    def mouseButtonUp(self, pos, event):
        for function in self.events['mousebuttonup']:
            function(pos, event)

    def mouseMotion(self, pos, event):
        for function in self.events['mousemotion']:
            function(pos, event)

    def update(self):
        """Se debe implementar en las clases que heredan"""
        pass


class CellGraph(object):
    """docstring for CellGraph"""

    def __init__(self, system, margin_width=0, margin_height=0,
                 background_color=(0, 0, 0), cellwidth=5, cellheight=5, fps=60,
                 separation_between_cells=1):
        self.separation_between_cells = separation_between_cells
        self.background_color = background_color
        self.margin_height = margin_height
        self.margin_width = margin_width
        self.cellheight = cellheight
        self.cellwidth = cellwidth
        self.system = system
        self.fps = fps

        self.width = 2 * margin_width + cellwidth * system.width + \
            separation_between_cells * (system.width - 1)
        self.height = 2 * margin_height + cellheight * system.height + \
            separation_between_cells * (system.height - 1)

    def getPositionInMatrix(self, pos):
        """dada la posicion de la pantalla retorna la posicion en la matrix"""
        posx = pos[0] - self.margin_height
        posy = pos[1] - self.margin_width
        posx = posx / (self.cellwidth + self.separation_between_cells)
        posy = posy / (self.cellheight + self.separation_between_cells)
        return int(posx), int(posy)

    def draw(self, screen):
        """dibuja el sistema en pantalla"""
        screen.fill(self.background_color)
        for i in range(self.system.height):
            for j in range(self.system.width):
                p.draw.rect(screen, self.system.getColor(i, j),
                            p.Rect(self.margin_width + j * self.cellwidth +
                                   (j * self.separation_between_cells),
                                   self.margin_height + i * self.cellheight +
                                   (i * self.separation_between_cells),
                                   self.cellwidth, self.cellheight))

    def reload(self, screen):
        self.draw(screen)
        if self.pause:
            p.display.set_caption(self.system.getCaption() + ' Pause')
        else:
            p.display.set_caption(self.system.getCaption())
        p.display.update()

    def eventManager(self, screen):
        quit = False
        pause = False

        for event in setEvents():
            if event.type == p.QUIT:
                quit = True
                break
            if event.type == p.KEYDOWN:
                if event.key == pl.K_p or event.key == pl.K_SPACE:
                    pause = True
                if event.key == pl.K_q:
                    quit = True
                if event.key == pl.K_s:
                    p.image.save(screen, self.system.getName())
                    print('Saved image')
                self.system.keyDown(p.key.name(event.key))
            if event.type == p.MOUSEBUTTONDOWN:
                self.system.mouseButtonDown(
                    self.getPositionInMatrix(event.pos), event)
            if event.type == p.KEYUP:
                self.system.keyUp(event)
            if event.type == p.MOUSEBUTTONUP:
                self.system.mouseButtonUp(
                    self.getPositionInMatrix(event.pos), event)
            if event.type == p.MOUSEMOTION:
                self.system.mouseMotion(
                    self.getPositionInMatrix(event.pos), event)

        return quit, pause

    def run(self, manual=False):
        p.display.init()

        screen = p.display.set_mode((self.width, self.height))
        p.display.set_caption(self.system.getCaption())

        clock = p.time.Clock()

        quit = False
        self.pause = True

        self.reload(screen)

        while not quit and not manual:
            clock.tick(self.fps)

            quit, temp = self.eventManager(screen)

            if temp:
                self.pause = not self.pause

            if not self.pause and not quit:
                self.system.update()

            self.reload(screen)

        while not quit and manual:
            pause = False
            while not pause and not quit:
                clock.tick(10)
                quit, pause = self.eventManager(screen)
                self.reload(screen)

                if p.key.get_pressed()[pl.K_SPACE]:
                    pause = True

            if pause and not quit:
                self.pause = True
                self.system.update()

            self.reload(screen)


def test():
    pass


if __name__ == '__main__':
    test()
