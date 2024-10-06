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
    def __init__(self):
        pass
    

# Initialize Pygame
pygame.init()

# Clip management
dir_path = os.path.dirname(os.path.realpath(__file__))
video1=Clip("CLIP1",os.path.join(dir_path,"assets","abba.mp4"),40,42)
video2=Clip("CLIP2",os.path.join(dir_path,"assets","abba.mp4"),50,52)
clip_surface_manager=ClipSurfaceManager(video1)

# Prepare SCREEN
screen = pygame.display.set_mode(clip_surface_manager.get_surface().get_size(), 0, 32)

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

          
    # update objects
    clip_surface_manager.update()

    # Draw the surface onto the window
    screen.blit(clip_surface_manager.get_surface(), (0, 0))
    pygame.display.flip()
    
# Quit Pygame
pygame.quit()