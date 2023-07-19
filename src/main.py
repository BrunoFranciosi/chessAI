import pygame
import sys

from constant import *
from game import Game

class Main:
    def __init__(self):
        pygame.init()                                               # é feita a inicialização do pygame
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )    # criação da tela do jogo com as dimensões definidas em WIDTH e HEIGHT
        pygame.display.set_caption('Chess')                         # definido o título da janela do jogo como "Chess"
        self.game = Game()


    def mainLoop(self):                                             # executar o loop principal do jogo

        #usar game e screen ao inves de se referir toda vez a self.game e self.screen
        screen = self.screen
        game = self.game

        while True:
            game.show_bg(screen)
            game.show_pieces(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()



            

            pygame.display.update()


main = Main()
main.mainLoop()