import pygame
import sys

from constant import *
from game import Game
from dragger import Dragger

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
        board = self.game.board
        dragger = self.game.dragger

        while True:
            game.show_bg(screen)
            game.show_pieces(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:    #click mouse
                    dragger.update_mouse(event.pos)                    #print(event.pos)                # vamos pegar essas possições e passar para o update_mouse

                    clicked_row = int(dragger.mouseY // SQSIZE) # clicked_row eh a linha que foi clicada, dragger.mouseY eh a posição do mouse em Y
                    clicked_col = int(dragger.mouseX // SQSIZE) #clicked_col eh a coluna que foi clicada, dragger.mouseX eh a posição do mouse em X

                    if board.squares[clicked_row][clicked_col].has_piece(): #se tiver uma peça na posição clicada
                        piece = board.squares[clicked_row][clicked_col].piece
                        dragger.save_initial(event.pos) #salva a posição inicial do mouse, precisamos disso pois se o usuario fizer um movimento invalido, a peça tem que voltar para a posição inicial
                        dragger.drag_piece(piece) #pega a peça que foi clicada e arrasta ela
                    
                elif event.type == pygame.MOUSEMOTION:      #mouse em movimento
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_bg(screen)
                        game.show_pieces(screen)
                        dragger.update_blit(screen)

                elif event.type == pygame.MOUSEBUTTONUP:    #mouse solto
                    dragger.undrag_piece()

                if event.type == pygame.QUIT:               #fechar janela
                    pygame.quit()
                    sys.exit()



            

            pygame.display.update()


main = Main()
main.mainLoop()