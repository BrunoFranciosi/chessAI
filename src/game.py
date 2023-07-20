# responsável por todos os métodos de renderização

import pygame

from constant import *
from board import Board
from dragger import Dragger

class Game:
    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()

    # Show Methods

    def show_bg(self, surface):                     # recebe como parâmetro uma superfície onde será exibido o jogo (nesse caso, a tela do pygame).
        for row in range(ROWS):                     # percorridas todas as linhas e colunas do tabuleiro, definidas em ROWS e COLS
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = (234, 235, 200) # light green
                else:
                    color = (119, 154, 88) # dark green
                
                rectangle = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)

                pygame.draw.rect(surface, color, rectangle)
    
    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # checar se tem uma peça na posição especifica
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece # pega a peça que está na posição especifica


                    # todas as peças exceto a que eu estou arrastando
                    if piece is not self.dragger.piece:
                        piece.set_texture(size = 80)
                        img = pygame.image.load(piece.texture) # carrega a imagem da peça
                        img_center = (col * SQSIZE + SQSIZE//2, row * SQSIZE + SQSIZE//2) # define o centro da imagem
                        piece.texture_rect = img.get_rect(center = img_center) # define o centro da imagem
                        surface.blit(img, piece.texture_rect) # desenha a imagem na tela


    def show_moves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece # pega a peça que está sendo arrastada que queremos mostrar os movimentos

            #loop todos os movimentos validos
            for move in piece.moves:
                #colorir o quadrado do movimento
                if (move.final.row + move.final.col) % 2 == 0:
                    color = '#C86464'
                else:
                    color = '#C84646'
                
                rectangle = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)

                pygame.draw.rect(surface, color, rectangle)