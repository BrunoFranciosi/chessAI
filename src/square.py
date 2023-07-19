class Square:
    def __init__(self, row, col, piece = None):
        self.row = row
        self.col = col
        self.piece = piece
    
    def has_piece(self):
        return self.piece != None #se tiver uma peça, retorna True, se não, retorna False