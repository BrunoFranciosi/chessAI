from constant import *
from square import Square
from piece import *
from move import Move
import copy
from sound import Sound
import os

class Board:
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0,] for col in range(COLS)] #para cada COLUNA nos vamos adicionar  uma lista de 8 zeros
        self.last_move = None #ultimo movimento feito
        self._create() #cria o tabuleiro
        self._add_pieces('white') #adiciona as peças brancas
        self._add_pieces('black') #adiciona as peças pretas

    def move(self, piece, move, testing=False):
        inicial = move.inicial
        final = move.final

        en_passant_empty = self.squares[final.row][final.col].isempty()

        # atualiza o tabuleiro do console
        self.squares[inicial.row][inicial.col].piece = None
        self.squares[final.row][final.col].piece = piece
       

        # promoção do peão e en passant
        if isinstance(piece, Pawn):
            diff = final.col - inicial.col
            if diff != 0 and en_passant_empty:
                self.squares[inicial.row][inicial.col + diff].piece = None
                self.squares[final.row][final.col].piece = piece
                if not testing:
                    sound = Sound(os.path.join('assets/sounds', 'capture.wav'))
                    sound.play()
                           
            else:
                # pawn promotion
                self.pawn_promotion(piece, final)
            
        # roque
        if isinstance(piece, King):
            if self.roque(inicial, final) and not testing:
                diff = final.col - inicial.col
                if (diff < 0):
                    rook = piece.left_rook
                else:
                    rook = piece.right_rook
                self.move(rook, rook.moves[-1])


        #move
        piece.moved = True

        #clear valide moves
        piece.clear_moves()

        # set last move
        self.last_move = move


    def valid_move(self, piece, move):
        return move in piece.moves

    def pawn_promotion(self, piece, final):
        if final.row == 0 or final.row == 7: #nao preciso checar a cor, pois o peão só pode chegar na ultima linha do tabuleiro
            self.squares[final.row][final.col].piece = Queen(piece.color) #se o peão chegar na ultima linha, ele vai virar uma rainha


    def roque(self, inicial, final):
        return abs(inicial.col - final.col) == 2 #se a diferença entre a coluna inicial e a final for igual a 2, o roque é valido


    
    def set_true_en_passant(self, piece):
        if not isinstance(piece, Pawn):
            return

        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_passant = False
        
        piece.en_passant = True
        

    def check(self, piece, move):
        temp_piece = copy.deepcopy(piece) #cria uma copia da peça
        temp_board = copy.deepcopy(self) #cria uma copia do tabuleiro
        temp_board.move(temp_piece, move, testing=True) #move a peça na copia do tabuleiro

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool = False) #calcula os movimentos possiveis para a peça
                    for m in p.moves: #loopando cada movimento possivel da peça
                        if isinstance(m.final.piece, King): #se o movimento final da peça for um rei
                            return True #retorna True, pois o rei está em cheque
        
        return False





    def _create(self):          # "_" significa que o método é privado
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col) #criamos um quadrado para cada posição do tabuleiro
    
    def calc_moves(self, piece, row, col, bool=True):
        '''
            calcular todas as possiveis ou validos movimentos para uma peça especifica para uma posição especifica        
        '''
        def pawn_moves():
            if piece.moved:
                steps = 1 #se o peão já tiver se movido, ele só pode andar uma casa
            else:
                steps = 2 #se o peão ainda não tiver se movido, ele pode andar duas casas

            # movimento na vertical
            start = row + piece.direction #exemplo: se o peão for branco, ele vai andar para cima, então o start vai ser a linha atual - 1
            end = row + (piece.direction * (1 + steps)) #exemplo: se o peão for branco, ele vai andar para cima, então o end vai ser a linha atual - 3(Execlusivo entao -2)
            for possible_move_row in range(start, end, piece.direction):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        #criar squares do novo movimento
                        inicial = Square(row, col)
                        final = Square(possible_move_row, col)
                        #criar um novo movimento
                        move = Move(inicial, final)

                        # check potential check
                        if bool:
                            if not self.check(piece, move):
                                #adicionar o movimento na lista de movimentos da peça
                                piece.add_move(move)
                        else:
                            piece.add_move(move)                        
                    # bloqueado
                    else:
                        break
                # fora do tabuleiro
                else:
                    break

            # movimento na diagonal
            possible_move_row = row + piece.direction
            possible_move_cols = [col - 1, col + 1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        #criar squares do novo movimento
                        inicial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        #criar um novo movimento
                        move = Move(inicial, final)

                        # check potential check
                        if bool:
                            if not self.check(piece, move):
                                #adicionar o movimento na lista de movimentos da peça
                                piece.add_move(move)
                        else:
                            piece.add_move(move)  
            
            # en passant movimento
            if piece.color == "white":
                r = 3
                final_row = 2
            else:
                r = 4
                final_row = 5
            #left en passant
            if Square.in_range(col-1) and row == r:
                if self.squares[row][col-1].has_enemy_piece(piece.color):
                    p = self.squares[row][col-1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            #criar squares do novo movimento
                            inicial = Square(row, col)
                            final = Square(final_row, col-1, p)
                            #criar um novo movimento
                            move = Move(inicial, final)

                            # check potential check
                            if bool:
                                if not self.check(piece, move):
                                    #adicionar o movimento na lista de movimentos da peça
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
            
            #right en passant
            if Square.in_range(col+1) and row == r:
                if self.squares[row][col+1].has_enemy_piece(piece.color):
                    p = self.squares[row][col+1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            #criar squares do novo movimento
                            inicial = Square(row, col)
                            final = Square(final_row, col+1, p)
                            #criar um novo movimento
                            move = Move(inicial, final)

                            # check potential check
                            if bool:
                                if not self.check(piece, move):
                                    #adicionar o movimento na lista de movimentos da peça
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)


        def knight_moves():
            # 8 possiveis movimentos caso o cavalo esteja no centro do tabuleiro
            possible_moves = [
                (row - 2, col + 1),
                (row - 1, col + 2),
                (row + 1, col + 2),
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row + 1, col - 2),
                (row - 1, col - 2),
                (row - 2, col - 1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color): #checando se a posição está vazia ou se tem uma peça rival(piece.doclor)
                        #criar squares do novo movimento
                        inicial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        #criar um novo movimento
                        move = Move(inicial, final)
                        
                        # check potential check
                        if bool:
                            if not self.check(piece, move):
                                #adicionar o movimento na lista de movimentos da peça
                                piece.add_move(move)
                            else:
                                break
                        else:
                            piece.add_move(move)  

        def straightline_moves(incrs): #incrs = increments: "como" voce vai mover em linha reta
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                # enquanto a posição estiver dentro do tabuleiro e estiver vazia ou tiver uma peça rival, o loop vai continuar
                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        # criar squares do possivel novo movimento
                        inicial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # criar um possivel novo movimento
                        move = Move(inicial, final)
                        
                        #empty = continua o loop
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            # check potential check
                            if bool:
                                if not self.check(piece, move):
                                    #adicionar o movimento na lista de movimentos da peça
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)  

                        # has enemy piece = add move + break
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            # check potential check
                            if bool:
                                if not self.check(piece, move):
                                    #adicionar o movimento na lista de movimentos da peça
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)  
                            break

                        # has team piece = break
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                    # fora do tabuleiro
                    else:
                        break

                    # incrementando incrs
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            adjacent_squares = [
                (row - 1, col + 0), # cima
                (row -1, col + 1), # diagonal superior direita
                (row + 0, col + 1), # direita
                (row + 1, col + 1), # diagonal inferior direita
                (row + 1, col + 0), # baixo
                (row + 1, col - 1), # diagonal inferior esquerda
                (row + 0, col - 1), # esquerda
                (row - 1, col - 1), # diagonal superior esquerda
            ]

            for possible_move in adjacent_squares:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        #criar squares do novo movimento
                        inicial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        #criar um novo movimento
                        move = Move(inicial, final)
                        # check potential check
                        if bool:
                            if not self.check(piece, move):
                                #adicionar o movimento na lista de movimentos da peça
                                piece.add_move(move)
                            else:
                                break
                        else:
                            piece.add_move(move)  

        # movimento do roque
        if not piece.moved:
            # roque grande
            left_rook = self.squares[row][0].piece
            if isinstance(left_rook, Rook):
                if not left_rook.moved:
                    for c in range(1, 4):
                        if self.squares[row][c].has_piece(): # roque nao eh possivel, só pode ser feito se não tiver nenhuma peça entre o rei e a torre
                            break

                        if c == 3:
                            # add left rook to king
                            piece.left_rook = left_rook

                            # rook move
                            inicial = Square(row, 0)
                            final = Square(row, 3)
                            moveR = Move(inicial, final)
                            

                            # king move
                            inicial = Square(row, col)
                            final = Square(row, 2)
                            moveK = Move(inicial, final)
                            

                            # check potential check
                            if bool:
                                if not self.check(piece, moveK) and not self.check(left_rook, moveR):
                                    #append new move to rook
                                    left_rook.add_move(moveR)
                                    #append new move to king
                                    piece.add_move(moveK)
                            else:
                                #append new move to rook
                                left_rook.add_move(moveR)
                                #append new move to king
                                piece.add_move(moveK)  

            # roque pequeno
            right_rook = self.squares[row][7].piece
            if isinstance(right_rook, Rook):
                if not right_rook.moved:
                    for c in range(5, 7):
                        if self.squares[row][c].has_piece(): # roque nao eh possivel, só pode ser feito se não tiver nenhuma peça entre o rei e a torre
                            break

                        if c == 6:
                            # add right rook to king
                            piece.right_rook = right_rook

                            # rook move
                            inicial = Square(row, 7)
                            final = Square(row, 5)
                            moveR = Move(inicial, final)
                            

                            # king move
                            inicial = Square(row, col)
                            final = Square(row, 6)
                            moveK = Move(inicial, final)
                            
                            # check potential check
                            if bool:
                                if not self.check(piece, moveK) and not self.check(right_rook, moveR):
                                    #append new move to rook
                                    right_rook.add_move(moveR)
                                    #append new move to king
                                    piece.add_move(moveK)
                            else:
                                #append new move to rook
                                right_rook.add_move(moveR)
                                #append new move to king
                                piece.add_move(moveK) 
        
        
        if piece.name == 'pawn':
            pawn_moves()
        elif piece.name == 'knight':
            knight_moves()
        elif piece.name == 'bishop':
            straightline_moves([
                (-1, 1), # diagonal superior esquerda
                (-1, -1), # diagonal superior direita
                (1, 1), # diagonal inferior esquerda
                (1, -1), # diagonal inferior direita
            ])
        elif piece.name == 'rook':
            straightline_moves([
                (-1, 0), # cima
                (1, 0), # baixo
                (0, 1), # direita
                (0, -1), # esquerda
            ])
        elif piece.name == 'queen':
            straightline_moves([
                (-1, 1), # diagonal superior esquerda
                (-1, -1), # diagonal superior direita
                (1, 1), # diagonal inferior esquerda
                (1, -1), # diagonal inferior direita
                (-1, 0), # cima
                (1, 0), # baixo
                (0, 1), # direita
                (0, -1), # esquerda
            ])
        elif piece.name == 'king':
            king_moves()
        

    def _add_pieces(self, color): # em cima já fizemos os "squares" que não pussuem peças, agora vamos adicionar as peças em cada quadrado
        # row_pawn = 1 if color == 'white' else 6  =>  mesmo codigo de baixo

        if color == 'white':
            row_pawn, row_other = (6, 7) #row_pawn = 6 e row_other = 7, quando as cores forem brancas, as peças vão ficar na linha 6 e 7
        else:
            row_pawn, row_other = (1, 0) #row_pawn = 1 e row_other = 0, quando as cores forem pretas, as peças vão ficar na linha 1 e 0

        # peões
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color)) #adiciona o peão na linha 6 ou 1, dependendo da cor, e na coluna que estivermos
        
        # cavalo
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bispo
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))        

        # torre
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # rainha
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # rei
        self.squares[row_other][4] = Square(row_other, 4, King(color))


# b = Board()
# b._create()