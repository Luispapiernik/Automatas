from os.path import exists
import pygame.locals as pl
import pygame as p


COLORS = {'WHITE': (255, 255, 255), 'BLACK': (0, 0, 0), 'CYAN': (0, 255, 255),
          'GREEN': (0, 255, 0), 'BLUE': (0, 0, 255), 'YELLOW': (255, 255, 0),
          'ORANGE': (255, 165, 0), 'MAGENTA': (255, 0, 255),
          'SILVER': (192, 192, 192), 'PURPLE': (128, 0, 128),
          'TEAL': (0, 128, 128), 'GRAY': (128, 128, 128), 'RED': (255, 0, 0),
          'BROWN': (165, 42, 42), 'GOLDEN': (255, 215, 0)}


class System(object):
    """docstring for System"""

    def __init__(self, matrix, name, colors):
        self.name = name
        self.width = len(matrix[0])
        self.height = len(matrix)
        self.colors = colors
        self.matrix = matrix

    def getColor(self, i, j):
        return self.colors[self.matrix[i][j]]

    def update(self):
        pass


class CellGraph(object):
    """Falta terminarlo"""

    def __init__(self, system, margin_width=0, margin_height=0,
                 background_color='BLACK', cellwidth=5, cellheight=5, fps=60,
                 separation_between_cells=1):
        self.separation_between_cells = separation_between_cells
        self.background_color = COLORS[background_color]
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

    def draw(self, screen):
        screen.fill(self.background_color)
        for i in range(self.system.height):
            for j in range(self.system.width):
                p.draw.rect(screen, COLORS[self.system.getColor(i, j)],
                            p.Rect(self.margin_width + j * self.cellwidth +
                                   (j * self.separation_between_cells),
                                   self.margin_height + i * self.cellheight +
                                   (i * self.separation_between_cells),
                                   self.cellwidth, self.cellheight))

    def getName(self):
        number = 0
        while True:
            name = self.system.name + str(number) + '.png'
            if not exists(name):
                return name
            number += 1

    def run(self, manual=False):
        p.display.init()

        screen = p.display.set_mode((self.width, self.height))

        clock = p.time.Clock()

        quit = False
        pause = False

        while not quit and not manual:
            clock.tick(self.fps)

            for event in p.event.get():
                if event.type == p.QUIT:
                    quit = True
                    break
                if event.type == p.KEYDOWN:
                    if event.key == pl.K_p or event.key == pl.K_SPACE:
                        pause = not pause
                    if event.key == pl.K_q:
                        quit = True
                    if event.key == pl.K_s:
                        p.image.save(screen, self.getName())
                        print('Saved image')

            if not pause and not quit:
                self.draw(screen)
                self.system.update()
                p.display.update()

        update = True

        while not quit and manual:
            # event = p.event.wait()
            clock.tick(20)

            for event in p.event.get():
                if event.type == p.QUIT:
                    quit = True

                if event.type == p.KEYDOWN:
                    if event.key == p.K_q:
                        quit = True
                    if event.key == pl.K_SPACE:
                        update = True
                    if event.key == pl.K_s:
                        p.image.save(screen, self.getName())
                        print('Saved image')

            if p.key.get_pressed()[pl.K_SPACE]:
                update = True

            if update and not quit:
                update = False
                self.draw(screen)
                self.system.update()
                p.display.update()

        p.quit()
