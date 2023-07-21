class Move:
    def __init__(self, inicial, final):
        #inicial e final são squares
        self.inicial = inicial
        self.final = final

    
    def __str__(self):
        s = ''
        s += f'({self.initial.col}, {self.initial.row})'
        s += f' -> ({self.final.col}, {self.final.row})'
        return s
    


    def __eq__(self, other):
        return self.inicial == other.inicial and self.final == other.final