import pygame
import time

class Menu:
    """Menu"""
    def __init__(self, init_position, dimension):
        # position, dimension
        self.width,self.height = dimension
        self.init_left,self.init_top = init_position
        self.left,self.top = init_position
        # surfaces
        self.surface = pygame.Surface(dimension, pygame.SRCALPHA)
        self.banner = pygame.Rect(0, 0, self.width, self.height)
        # control
        self.visible = False
        self.animation_show = False
        self.animation_hide = False
        # Font initialisation
        t0 = time.time()
        self.font=pygame.font.SysFont(None, 24)
        print('time needed for Font creation :', time.time()-t0)
    
    def toggle(self):
        if self.visible is True:
            self.hide()
        else:
            self.show()

    def create_from_scene(self, choices):
        pass

    def show(self):
        self.animation_hide=False
        self.animation_show=True

    def hide(self):
        self.animation_hide=True
        self.animation_show=False

    def update(self):
        limit_high = self.init_top-self.height-10
        limit_low = self.init_top
        if self.animation_show is True:
            if self.top-2 < limit_high:
                self.top = limit_high
                self.animation_show = False
                self.visible = True
            else:
                self.top -= 2
        
        if self.animation_hide is True:
            if self.top >= limit_low:
                self.top = limit_low
                self.animation_hide = False
                self.visible = False
            else:
                self.top += 2

    def get_surface(self):
        self.surface.fill(pygame.SRCALPHA)
        self.surface=self.surface.convert_alpha()
        pygame.draw.rect(self.surface, pygame.Color(50,50,50), self.banner, 0, 10, 10, 10, 10)
        #experiment text rendering
        img  =self.font.render("W -> Scene 1    X -> Scene 2    C -> Scene 3", True, (200,200,200))
        img2 =self.font.render("V -> Scene 1    B -> Scene 2    N -> Scene 3", True, (200,200,200))
        self.surface.blit(img, (20,10))
        self.surface.blit(img2, (20,35))
        #experiment text rendering
        return self.surface