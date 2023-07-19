import os

class Piece:
    def __init__(self, name, color, value, texture = None, texture_rect = None):
        self.name = name   # nome da peça
        self.color = color  # cor da peça

        #valor = 1 if color == 'white' else -1  =>  mesmo codigo de baixo
        if color == 'white':
            value_signal = 1
        else:
            value_signal = -1

        self.value = value * value_signal # valor da peça, se for branca, o valor é positivo, se for preta, o valor é negativo
        self.moves = [] # lista de movimentos possiveis da peça
        self.moved = False # se a peça já se moveu ou não
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect
    
    def set_texture(self, size=80): #a textura vai ser o caminho onde nos vamos encontrar a imagem da peça  texture == imagem_url
        self.texture = os.path.join(
            f'assets/images/imgs-{size}px/{self.color}_{self.name}.png' #vamos passar o caminho para encontrar uma imagem especifica
        )
    
    def add_moves(self, move):
        self.moves.append(move) #adiciona o movimento na lista de movimentos da peça



class Pawn(Piece):  # em python para falar que uma classe herda de outra, basta colocar o nome da classe pai entre parenteses

    def __init__(self, color): #com a cor do peão, podemos definir a seu movimento
        # self.dir = -1 if color == 'white else 1  =>  mesmo codigo de baixo

        if color == 'white':
            self.direction = -1 # se for branco, ele vai andar para cima, ou seja, a linha vai diminuir      cordenadas funcionam de um jeito diferente pois a linha do x aumento para a direita e a linha do y aumenta para baixo
        else:
            self.direction = 1
        
        super().__init__('pawn', color, 1.0) #super() é usado para chamar o construtor da classe pai, no caso Piece, e passar os parametros que ele precisa

class Knight(Piece): # so nao vai ter a direção, pois o cavalo pode andar para qualquer lado
    def __init__(self, color):
        super().__init__('knight', color, 3.0)

class Bishop(Piece):
    def __init__(self, color):
        super().__init__('bishop', color, 3.001) # vou "falar" para IA que o bispo é um pouco melhor que o cavalo

class Rook(Piece):
    def __init__(self, color):
        super().__init__('rook', color, 5.0)

class Queen(Piece):
    def __init__(self, color):
        super().__init__('queen', color, 9.0)

class King(Piece): #most important piece
    def __init__(self, color):
        super().__init__('king', color, 10000.0)
