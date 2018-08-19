# Game Of Life

Juego de la vida. El programa permite 2 modos de simulacion, el
manual en el que se pasa al siguiente frame de simulacion mediante la pulsacion
de la tecla SPACE y otro en el que se fija los frames por segundo, se puede
pausar con la tecla p ademas se puede tomar una captura de pantalla con la
tecla s, si se presiona la tecla c se limpia el tablero y si se presiona la
tecla e la configuracion del tablero se guarda en un archivo de texto. Se
permite tambien agregar celulas vivas presionando con el mouse a la celula. El
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
    - GOLDEN

usage:

    game_of_life.py [-h] [-f NAME] [-w WIDTH] [--height HEIGHT]
                       [-mw MARGIN_WIDTH] [-mh MARGIN_HEIGHT] [-cw CELL_WIDTH]
                       [-ch CELL_HEIGHT] [-sbc SBC] [-a ALIVES] [-bc COLOR]
                       [-c1 COLOR] [-c2 COLOR] [-m] [-fps FPS]


optional arguments:

    -h, --help            show this help message and exit
    -f NAME, --filename NAME
                        nombre con el que se guarda la captura de pantalla(si
                        se hace)
    -w WIDTH, --width WIDTH
                        numero de celdas horizontales
    --height HEIGHT       numero de celdas verticales
    -mw MARGIN_WIDTH, --margin-width MARGIN_WIDTH
                        largo de la margen horizontal
    -mh MARGIN_HEIGHT, --margin-height MARGIN_HEIGHT
                        largo de la margen vertical
    -cw CELL_WIDTH, --cell-width CELL_WIDTH
                        ancho horizontal de las celdas(celulas)
    -ch CELL_HEIGHT, --cell-height CELL_HEIGHT
                        ancho vertical de las celdas(celulas)
    -sbc SBC, --separation-between-cells SBC
                        separacion entre las celdas(celulas)
    -a ALIVES, --alives ALIVES
                        numero de celulas vivas
    -bc COLOR, --background-color COLOR
                        color de fondo, es el mismo que el de la margen y la
                        separacion entre celdas
    -c1 COLOR, --color-alive COLOR
                        color de celulas vivas
    -c2 COLOR, --color-death COLOR
                        color celulas muertas
    -m, --manual          si este argumento es pasado la simulaion se debe
                        actualizar manualmente presionando la tecla SPACE
    -fps FPS, --frame-per-seconds FPS
                        frames por segundo la simulacion corre automaticamente



## Pruebas

python game_of_life.py -w 50 --height 50 -a 500 -cw 10 -ch 10 -mw 30 -mh 30

![](https://github.com/Luispapiernik/Automatas/blob/master/GameOfLife/Images/gameoflife.png)
