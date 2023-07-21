class Square:
    ALFABETO = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5:'f', 6:'g', 7:'h'}

    def __init__(self, row, col, piece = None):
        self.row = row
        self.col = col
        self.piece = piece
        self.alfabeto = self.ALFABETO[col]

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col
    
    def has_piece(self):
        return self.piece != None #se tiver uma peça, retorna True, se não, retorna False
    
    def isempty(self):
        return not self.has_piece() #se não tiver uma peça, retorna True, se tiver, retorna False

    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color
    
    def has_enemy_piece(self, color):
        return self.has_piece() and self.piece.color != color #se tiver uma peça e a cor da peça for diferente da cor passada como parâmetro, retorna True, se não, retorna False

    def isempty_or_enemy(self, color):
        return self.isempty() or self.has_enemy_piece(color) #se não tiver uma peça ou se tiver uma peça e a cor da peça for diferente da cor passada como parâmetro, retorna True, se não, retorna False
    
    @staticmethod #metodo estatico, não precisa de uma instancia da classe para ser chamado
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True
    
    @staticmethod
    def get_alfabeto(col):
        ALFABETO = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5:'f', 6:'g', 7:'h'}
        return ALFABETO[col]



'''
s = Square() #criei uma instancia da classe Square
posso colocar -> s.has_piece()
um metodos estatico não precisa de uma instancia da classe para ser chamado, posso colocar -> Square.in_range()


'''
