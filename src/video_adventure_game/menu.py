import pygame
import time
from scene import Scene, Choice

BANNER_COLOR = (0,0,0)

UNFOCUS_BOX_COLOR = (0,0,0)
FOCUS_BOX_COLOR = (255,255,0)
SELECTED_BOX_COLOR = (0,255,255)

UNFOCUS_TEXT_COLOR = (150,150,150)
FOCUS_TEXT_COLOR = (200,200,0)
SELECTED_TEXT_COLOR = (255,255,255)

class MenuChoice:
    """Define a menu choice element"""
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

    def color_box(self, vote_allowed):
        if self.is_selected is True:
            return SELECTED_BOX_COLOR
        else:
            if self.is_focus is True and vote_allowed is True:
                return FOCUS_BOX_COLOR
            else:
                return UNFOCUS_BOX_COLOR
            
    def color_text(self, vote_allowed):
        if self.is_selected is True:
            return SELECTED_TEXT_COLOR
        else:
            if self.is_focus is True and vote_allowed is True:
                return FOCUS_TEXT_COLOR
            else:
                return UNFOCUS_TEXT_COLOR

    def get_surface(self, vote_allowed):
        """Get surface of the MenuChoice object"""
        self.surface.fill(pygame.SRCALPHA)
        self.surface=self.surface.convert_alpha()
        # Render Rect
        pygame.draw.rect(self.surface, self.color_box(vote_allowed), self.rect, 2, 10,10,10,10)
        # Render Text
        self.rendered_text = self.font.render(f"{self.choice.description}", True, self.color_text(vote_allowed))
        text_rec = self.rendered_text.get_rect(center=(self.surface.get_width()/2, self.surface.get_height()/2))
        self.surface.blit(self.rendered_text, text_rec)
        return self.surface


class Menu:
    """Menu"""
    def __init__(self, screen_size):
        """Create the menu 
            - should be created once
        """
        # dimension
        h = screen_size[1] / 10
        self.animation_increment = h / 25
        dimension=(screen_size[0]-100,h)
        init_position=((screen_size[0]-dimension[0])/2, screen_size[1])
        self.width,self.height = dimension
        self.margin = 10
        self.font_size = round(h/2)
        self.font=pygame.font.SysFont(None, self.font_size)
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
        print('time needed for Font creation :', time.time()-t0)
        # surfaces
        self.surface = pygame.Surface(dimension, pygame.SRCALPHA)
        self.banner = pygame.Rect(0, 0, self.width, self.height)
        self.progress_bar_color = (255, 255, 255)
        self.progress_bar_rect = pygame.Rect(0,0,0,4)

    def update_menu_choices_from_scene(self, scene: Scene, history):
        # Init
        self.menu_choices = []
        filtered_scene_choices = [choice for choice in scene.choices if eval(choice.condition) is True]
        index = 0
        element_width = (self.width - ((len(filtered_scene_choices)+1)*self.margin)) / len(filtered_scene_choices)
        element_heigth = (self.height - 2*self.margin)
        for choice in filtered_scene_choices:
            index = index + 1
            # Calculate position
            position = (index*self.margin + (index-1)*element_width, self.margin)
            # add choice
            menu_choice = MenuChoice(self.font, choice, position, (element_width, element_heigth))
            self.menu_choices.append(menu_choice)

    def is_choice_selected(self):
        """Return is menu has a chosen element"""
        return True in [choice.is_selected for choice in self.menu_choices]

    def show(self):
        """Init menu show animation"""
        self.animation_hide=False
        self.animation_show=True

    def hide(self):
        """Init menu hide animation"""
        self.animation_hide=True
        self.animation_show=False

    def toggle(self):
        """Change status of the menu"""
        if self.visible is True:
            self.hide()
        else:
            self.show()

    def update(self):
        """Update animation of the menu
        """
        limit_high = self.init_top-self.height-10
        limit_low = self.init_top
        if self.animation_show is True:
            if self.top-self.animation_increment < limit_high:
                self.top = limit_high
                self.animation_show = False
                self.visible = True
            else:
                self.top -= self.animation_increment
        
        if self.animation_hide is True:
            if self.top >= limit_low:
                self.top = limit_low
                self.animation_hide = False
                self.visible = False
            else:
                self.top += self.animation_increment

    def update_progress_bar(self, time, duration):
        """update time for menu progress bar
        """
        time = 0 if time < 0 else time
        time = duration if time > duration else time
        self.progress_bar_color = (255, int(255*(1-time/duration)), int(255*(1-time/duration)))
        self.progress_bar_rect.width = self.width*(1-time/duration)
        self.progress_bar_rect.center = (self.width/2, self.height-5)

    def get_surface(self):
        """Get surface menu object
        """
        # fill surface with transparency
        self.surface.fill(pygame.SRCALPHA)
        self.surface=self.surface.convert_alpha()
        # Banner with rounded edge
        pygame.draw.rect(self.surface, BANNER_COLOR, self.banner, 0, 10, 10, 10, 10)
        # Choices rendering
        choice: Choice
        for choice in self.menu_choices:
            self.surface.blit(choice.get_surface(self.is_choice_selected() is False), choice.position)
        # Add progress bar
        pygame.draw.rect(self.surface, self.progress_bar_color, self.progress_bar_rect, 0, 2, 2, 2, 2)

        return self.surface