from constant import *
from square import Square
from piece import *
from move import Move

class Board:
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0,] for col in range(COLS)] #para cada COLUNA nos vamos adicionar  uma lista de 8 zeros

        self._create() #cria o tabuleiro
        self._add_pieces('white') #adiciona as peças brancas
        self._add_pieces('black') #adiciona as peças pretas

    def _create(self):          # "_" significa que o método é privado
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col) #criamos um quadrado para cada posição do tabuleiro
    
    def calc_moves(self, piece, row, col):
        '''
            calcular todas as possiveis ou validos movimentos para uma peça especifica para uma posição especifica        
        '''

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
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color): #checando se a posição está vazia ou se tem uma peça rival(piece.doclor)
                        #criar squares do novo movimento
                        inicial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        #criar um novo movimento
                        move = Move(inicial, final)
                        piece.add_move(move) #adiciona o movimento na lista de movimentos da peça


        if piece.name == 'pawn':
            pass
        elif piece.name == 'knight':
            knight_moves()
        elif piece.name == 'bishop':
            pass
        elif piece.name == 'rook':
            pass
        elif piece.name == 'queen':
            pass
        elif piece.name == 'king':
            pass


        

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