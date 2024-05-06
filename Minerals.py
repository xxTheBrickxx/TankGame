import random
import math
import pygame
import helper as hlp

class Minerals:

    def __init__(self,
                  x,
                  y,
                  tanklist,
                  id,
                  statsdict
    ):
        self.x = x
        self.y = y
        self.img = pygame.image.load(statsdict["image"]).convert_alpha()
        self.image = pygame.transform.scale(self.img,(self.img.get_width() /2,self.img.get_height() /2))
        self.heath = statsdict["hp"]
        self.mask = pygame.mask.from_surface(self.image)
        self.id = id
        self.tanklist = tanklist
        
    def mineraldraw(self, win):
        win.blit(self.image, (self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)