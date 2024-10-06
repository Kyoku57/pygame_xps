import os, pygame
from moviepy.editor import VideoFileClip
from enum import Enum

class Clip:
    """Clip that represent a subset of a video"""
    def __init__(self, id, video_path, start, end):
        self.id=id
        self.video_path=video_path
        self.start=start
        self.end=end
        self.time=start        
        self.clip=VideoFileClip(video_path)
        self.frame=self.clip.get_frame(t=self.time)

    def update(self):
        self.time += 1/25
        is_finished = self.time > self.end
        if is_finished:
            self.time = self.start
        self.frame=self.clip.get_frame(t=self.time)
        return is_finished

class ClipSurfaceManager:
    """Object that manage which clip to render"""
    def __init__(self, clip):
        self.current_clip=clip
        self.next_clip=clip
        self.surface=pygame.surfarray.make_surface(self.current_clip.frame.swapaxes(0, 1))

    def update(self):
        if self.current_clip.update():
            self.current_clip=self.next_clip

    def get_surface(self):
        pygame.surfarray.blit_array(self.surface, self.current_clip.frame.swapaxes(0, 1))
        return self.surface

class Menu:
    """Menu"""
    def __init__(self, dimension):
        self.height=dimension[1]
        self.width=dimension[0]
        self.surface=pygame.Surface(dimension)
        self.banner=pygame.Rect(0,self.height, self.width,self.height)
        self.animation_show=False
        self.animation_hide=False

    def show_menu(self):
        self.animation_hide=False
        self.animation_show=True

    def hide_menu(self):
        self.animation_hide=True
        self.animation_show=False

    def update(self):
        if self.animation_show is True:
            if self.banner.top < 0:
                self.banner.top=0
                self.animation_show=False
            else:
                self.banner.move_ip(0,-2)
        
        if self.animation_hide is True:
            if self.banner.top >= self.height:
                self.banner.top=self.height
                self.animation_hide=False
            else:
                self.banner.move_ip(0,2)


    def get_surface(self):
        self.surface.fill(pygame.Color(50,100,100))
        pygame.draw.rect(self.surface, pygame.Color(0,50,50), menu.banner)
        return self.surface

    

# Initialize Pygame
pygame.init()

# Clip management
dir_path = os.path.dirname(os.path.realpath(__file__))
video1=Clip("CLIP1",os.path.join(dir_path,"assets","abba.mp4"),40,42)
video2=Clip("CLIP2",os.path.join(dir_path,"assets","abba.mp4"),50,52)
clip_surface_manager=ClipSurfaceManager(video1)
screen_size=clip_surface_manager.get_surface().get_size()


# init menu
menu=Menu(dimension=(screen_size[0]-20,50))

# Prepare SCREEN
screen = pygame.display.set_mode(screen_size, 0, 32)
pygame.display.set_caption("ABBA test")

# Run the Pygame loop to keep the window open
running = True
clock=pygame.time.Clock()
while running:
    clock.tick(25)
    
    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            clip_surface_manager.next_clip=video1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            clip_surface_manager.next_clip=video2
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            menu.show_menu()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
            menu.hide_menu()
          
    # update objects
    clip_surface_manager.update()
    menu.update()


    # Draw the surface onto the window
    screen.blit(clip_surface_manager.get_surface(), (0, 0))
    screen.blit(menu.get_surface(), ((screen_size[0]-menu.width)/2, screen_size[1]-menu.height))
   
    pygame.display.flip()
    
# Quit Pygame
pygame.quit()