# responsável por todos os métodos de renderização

import pygame

from constant import *

class Game:
    def __init__(self):
        pass

    # Show Methods

    def show_bg(self, surface):                     # recebe como parâmetro uma superfície onde será exibido o jogo (nesse caso, a tela do pygame).
        for lin in range(ROWS):                     # percorridas todas as linhas e colunas do tabuleiro, definidas em ROWS e COLS
            for col in range(COLS):
                if (lin + col) % 2 == 0:
                    color = (234, 235, 200) # light green
                else:
                    color = (119, 154, 88) # dark green
                
                rectangle = (col * SQSIZE, lin * SQSIZE, SQSIZE, SQSIZE)

                pygame.draw.rect(surface, color, rectangle)