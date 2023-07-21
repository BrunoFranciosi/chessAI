import pygame
from constant import *

class Dragger:
    def __init__(self):
        self.piece = None   #peça que está sendo arrastada
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0

    def update_blit(self, surface): # quero que a peça seja desenhada um pouco maior que o normal
        self.piece.set_texture(size = 128) #texture
        texture = self.piece.texture
        img = pygame.image.load(texture) # carrega a imagem da peça
        img_center = (self.mouseX, self.mouseY)
        self.piece.texture_rect = img.get_rect(center = img_center)
        surface.blit(img, self.piece.texture_rect) # desenha a imagem na tela

    

    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos #(xcor, ycor)

    def save_initial(self, pos):
        self.initial_row = int(pos[1] // SQSIZE)
        self.initial_col = int(pos[0] // SQSIZE)
    
    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.piece = None
        self.dragging = False