import pygame
import time
from scene import Scene, Choice

GREY = (200,200,200)

class MenuChoice:
    def __init__(self, font, choice: Choice):
        self.font = font
        self.choice = choice
        self.rendered_choice = self.font.render(f"{choice.description}", True, GREY)
        self.width = 0
        self.position = (0,0)
        #self.rect = pygame.Rect(0, 0, self.width, self.height)

    def get_surface(self):
        pass



class Menu:
    """Menu"""
    def __init__(self, init_position, dimension):
        # dimension
        self.width,self.height = dimension
        # position
        self.left,self.top = init_position
        self.init_left,self.init_top = init_position
        # control
        self.visible = False
        self.animation_show = False
        self.animation_hide = False
        # choices
        self.menu_choices = []
        # Font initialisation
        t0 = time.time()
        self.font_size = 24
        self.font=pygame.font.SysFont(None, self.font_size)
        print('time needed for Font creation :', time.time()-t0)
        # surfaces
        self.surface = pygame.Surface(dimension, pygame.SRCALPHA)
        self.banner = pygame.Rect(0, 0, self.width, self.height)

    def toggle(self):
        if self.visible is True:
            self.hide()
        else:
            self.show()

    def update_menu_choices_from_scene(self, scene: Scene):
        top, left = 10, 20
        index = 0
        total = len(scene.choices)
        element_width = (self.width - (total*left)) / total
        self.menu_choices = []
        for choice in scene.choices:
            index = index + 1
            element = MenuChoice(self.font, choice)
            element.width = element.width
            element.position = (( index*left + (index-1)*element_width ), top)
            self.menu_choices.append(element)

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
        # Banner with rounded edge
        pygame.draw.rect(self.surface, pygame.Color(50,50,50), self.banner, 0, 10, 10, 10, 10)
        # CHoices rendering
        for choice in self.menu_choices:
            self.surface.blit(choice.rendered_choice, choice.position)
        return self.surface