# responsável por todos os métodos de renderização

import pygame

from constant import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square

class Game:
    def __init__(self):
        self.next_player = "white"
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()

    # Show Methods

    def show_bg(self, surface):                     # recebe como parâmetro uma superfície onde será exibido o jogo (nesse caso, a tela do pygame).
        theme = self.config.theme             # pega o tema do jogo
        
        for row in range(ROWS):                     # percorridas todas as linhas e colunas do tabuleiro, definidas em ROWS e COLS
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = theme.bg.light
                else:
                    color = theme.bg.dark
                
                rectangle = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)

                pygame.draw.rect(surface, color, rectangle)

                # row coordinates
                if col == 0:
                    if row % 2 == 0:
                        color = theme.bg.dark
                    else:
                        color = theme.bg.light
                    #label
                    lbl = self.config.font.render(str(ROWS - row), 1, color)
                    lbl_pos = (5, 5 + row * SQSIZE)
                    #blit
                    surface.blit(lbl, lbl_pos)

                # col coordinates
                if row == 7:
                    if (row + col) % 2 == 0:
                        color = theme.bg.dark
                    else:
                        color = theme.bg.light
                    #label
                    lbl = self.config.font.render(Square.get_alfabeto(col), 1, color)
                    lbl_pos = (col * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    #blit
                    surface.blit(lbl, lbl_pos)
    
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
        theme = self.config.theme

        if self.dragger.dragging:
            piece = self.dragger.piece # pega a peça que está sendo arrastada que queremos mostrar os movimentos

            #loop todos os movimentos validos
            for move in piece.moves:
                #colorir o quadrado do movimento
                if (move.final.row + move.final.col) % 2 == 0:
                    color = theme.moves.light
                else:
                    color = theme.moves.dark
                
                rectangle = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)

                pygame.draw.rect(surface, color, rectangle)

    
    def show_last_move(self, surface):
        theme = self.config.theme

        if self.board.last_move:
            inicial = self.board.last_move.inicial
            final = self.board.last_move.final

            for pos in [inicial, final]:
                if (pos.row + pos.col) % 2 == 0:
                    color = theme.trace.light
                else:
                    color = theme.trace.dark

                rectangle = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)

                pygame.draw.rect(surface, color, rectangle)

    
    #other methods

    def next_turn(self):
        if self.next_player == "white":
            self.next_player = "black"
        else:
            self.next_player = "white"
    
    def change_theme(self):
        self.config.change_theme()

    def sound_effect(self, captured = False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()
    
    def reset(self):
        self.__init__()