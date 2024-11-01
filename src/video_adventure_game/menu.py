import pygame
import time
from scene import Scene, Choice

BANNER_COLOR = (50,50,50)
UNFOCUS_ELEMENT_COLOR = (100,100,100)
FOCUS_ELEMENT_COLOR = (255,255,0)
SELECTED_ELEMENT_COLOR = (0,255,255)
TEXT_COLOR = (200,200,200)

class MenuChoice:
    def __init__(self, font, choice: Choice, position, dimension):
        """Create a menu choice element"""
        self.font = font
        self.choice = choice
        self.width, self.height = dimension
        self.position = position
        # pygame objects
        self.surface = pygame.Surface(dimension, pygame.SRCALPHA)
        self.rect = pygame.Rect((0,0), dimension)
        self.is_focus = False
        self.is_selected = False

    def reset(self):
        self.is_focus = False
        self.is_selected = False

    def color(self, vote_allowed):
        if self.is_selected is True:
            return SELECTED_ELEMENT_COLOR
        else:
            if self.is_focus is True and vote_allowed is True:
                return FOCUS_ELEMENT_COLOR
            else:
                return UNFOCUS_ELEMENT_COLOR

    def get_surface(self, vote_allowed):
        """Get surface of the MenuChoice object"""
        self.surface.fill(pygame.SRCALPHA)
        self.surface=self.surface.convert_alpha()
        # Render Rect
        pygame.draw.rect(self.surface, self.color(vote_allowed), self.rect, 2)
        # Render Text
        self.rendered_text = self.font.render(f"{self.choice.description}", True, TEXT_COLOR)
        self.surface.blit(self.rendered_text, (5,5))
        return self.surface


class Menu:
    """Menu"""
    def __init__(self, init_position, dimension):
        """Create the menu - should be created once"""
        # dimension
        self.width,self.height = dimension
        self.margin = 10
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
        # Current choice
        self.selected = None

    def toggle(self):
        if self.visible is True:
            self.hide()
        else:
            self.show()

    def update_menu_choices_from_scene(self, scene: Scene):
        # Init
        self.menu_choices = []
        self.selected = None

        index = 0
        element_width = (self.width - ((len(scene.choices)+1)*self.margin)) / len(scene.choices)
        element_heigth = (self.height - 2*self.margin)
        for choice in scene.choices:
            index = index + 1
            # Calculate position
            position = (index*self.margin + (index-1)*element_width, self.margin)
            # add choice
            menu_choice = MenuChoice(self.font, choice, position, (element_width, element_heigth))
            self.menu_choices.append(menu_choice)

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
        pygame.draw.rect(self.surface, BANNER_COLOR, self.banner, 0, 10, 10, 10, 10)
        # Choices rendering
        choice: Choice
        for choice in self.menu_choices:
            self.surface.blit(choice.get_surface(self.selected is None), choice.position)
        return self.surface