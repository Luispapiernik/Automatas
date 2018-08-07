### Modelo Biham Middleton Levine para trafico vehicular

El programa permite 2 modos de simulacion, el manual en el que se pasa al siguiente
frame de simulacion mediante la pulsacion de la tecla SPACE y otro en el que se
fija los frames por segundo, se puede pausar con la tecla p ademas se puede tomar
una captura de pantalla con la tecla s. En la simulacion se usan dos tipos de
carros, los del tipo 1 son los que solo se mueven en direccion vertical y los
de tipo 2 se mueven solo en direccion horizontal.

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
    - GOLDEN


usage:

    biham_milddleton_levine.py [-h] [-f NAME] [-w WIDTH] [--height HEIGHT]
                                  [-mw MARGIN_WIDTH] [-mh MARGIN_HEIGHT]
                                  [-cw CELL_WIDTH] [-ch CELL_HEIGHT]
                                  [-sbc SBC] [-n1 N1] [-n2 N2] [-bc COLOR]
                                  [-sc COLOR] [-c1 COLOR] [-c2 COLOR] [-m]
                                  [-fps FPS]

optional arguments:

      -h, --help            show this help message and exit

      -f NAME, --filename NAME

                            nombre con el que se guarda la captura de pantalla(si
                            se hace)

      -w WIDTH, --width WIDTH

                            ancho de la calle

      --height HEIGHT       largo de la calle

      -mw MARGIN_WIDTH, --margin-width MARGIN_WIDTH

                            largo de la margen horizontal

      -mh MARGIN_HEIGHT, --margin-height MARGIN_HEIGHT

                            largo de la margen vertical

      -cw CELL_WIDTH, --cell-width CELL_WIDTH

                            ancho horizontal de las celdas(carros)

      -ch CELL_HEIGHT, --cell-height CELL_HEIGHT

                            ancho vertical de las celdas(carros)

      -sbc SBC, --separation-between-cells SBC

                            separacion entre las celdas(carros)

      -n1 N1, --number-cars-type-one N1

                            numero de carros de tipo 1

      -n2 N2, --number-cars-type-two N2

                            numero de carros de tipo 2

      -bc COLOR, --background-color COLOR

                            color de fondo, es el mismo que el de la margen

      -sc COLOR, --street-color COLOR

                            color de fondo de la calle

      -c1 COLOR, --car-color-type-one COLOR

                            color del carro de tipo 1

      -c2 COLOR, --car-color-type-two COLOR

                            color del carro de tipo 2

      -m, --manual          si este argumento es pasado la simulaion se debe

                            actualizar manualment presionando la tecla SPACE

      -fps FPS, --frame-per-seconds FPS

                            frames por segundo la simulacion corre automaticamente
