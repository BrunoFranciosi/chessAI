import pygame
import sys

from constant import *
from game import Game
from dragger import Dragger
from square import Square
from move import Move

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
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            #click mouse
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)                    #print(event.pos)                # vamos pegar essas possições e passar para o update_mouse

                    clicked_row = int(dragger.mouseY // SQSIZE) # clicked_row eh a linha que foi clicada, dragger.mouseY eh a posição do mouse em Y
                    clicked_col = int(dragger.mouseX // SQSIZE) #clicked_col eh a coluna que foi clicada, dragger.mouseX eh a posição do mouse em X

                    if board.squares[clicked_row][clicked_col].has_piece(): #se tiver uma peça na posição clicada
                        piece = board.squares[clicked_row][clicked_col].piece
                        #valid piece (color)
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col) #calcula os movimentos validos para a peça clicada
                            dragger.save_initial(event.pos) #salva a posição inicial do mouse, precisamos disso pois se o usuario fizer um movimento invalido, a peça tem que voltar para a posição inicial
                            dragger.drag_piece(piece) #pega a peça que foi clicada e arrasta ela

                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                    
                #mouse em movimento
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        #show methods
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        dragger.update_blit(screen)

                #mouse solto
                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        #pegar a linha e coluna que o mouse foi solto
                        released_row = int(dragger.mouseY // SQSIZE)
                        released_col = int(dragger.mouseX // SQSIZE)

                        #criar possivel movimento
                        inicial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(inicial, final)

                        #verificar se o movimento é valido
                        if board.valid_move(dragger.piece, move):
                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece, move)
                            game.sound_effect(captured)
                            #show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)

                            #next turn
                            game.next_turn()




                    dragger.undrag_piece()

                #tecla pressionada
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        game.change_theme()

                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger
                        


                #fechar janela
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()



            

            pygame.display.update()


main = Main()
main.mainLoop()