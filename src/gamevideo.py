import os, pygame
from moviepy.editor import VideoFileClip
from enum import Enum

class Menu:
    def __init__(self):
        pass


class Clip:
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
    def __init__(self, clip):
        self.current_clip=clip
        self.next_clip=clip
        self.surface=pygame.surfarray.make_surface(self.current_clip.frame.swapaxes(0, 1))

    def update(self):
        if self.current_clip.update():
            self.current_clip=self.next_clip

    def getSurface(self):
        pygame.surfarray.blit_array(self.surface, self.current_clip.frame.swapaxes(0, 1))
        return self.surface


# Initialize Pygame
pygame.init()

dir_path = os.path.dirname(os.path.realpath(__file__))
video1=Clip("CLIP1",os.path.join(dir_path,"assets","abba.mp4"),40,42)
video2=Clip("CLIP2",os.path.join(dir_path,"assets","abba.mp4"),50,52)

manager=ClipSurfaceManager(video1)

screen = pygame.display.set_mode(manager.getSurface().get_size(), 0, 32)
print(screen.get_size())

# Run the Pygame loop to keep the window open
running = True
isPushedLeft = False 
clock=pygame.time.Clock()

carree=pygame.Rect(0,0,100,100)
while running:
    clock.tick(25)
    
    manager.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            manager.next_clip=video1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            manager.next_clip=video2

    pressed=pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:
        carree.move_ip(-2,0)
    if pressed[pygame.K_RIGHT]:
        carree.move_ip(2,0)
        
    # Draw the surface onto the window
    screen.blit(manager.getSurface(), (0, 0))
    pygame.draw.rect(screen, pygame.Color(200,0,0), carree)
    pygame.display.flip()
    
# Quit Pygame
pygame.quit()