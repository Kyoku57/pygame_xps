import os, pygame, uuid
from moviepy.editor import VideoFileClip
from enum import Enum

class Clip:
    """Clip that represent a subset of a video"""
    def __init__(self, id, assets_path, cache_path, filename, start, end):
        # time-management
        self.id=id
        self.start=start
        self.end=end
        self.time=start
        # path
        self.assets_path=assets_path
        self.cache_path=cache_path
        self.filename=filename
        # video
        self.video_path=os.path.join(assets_path,filename)
        self.clip=VideoFileClip(self.video_path)
        self.frame=self.clip.get_frame(t=self.time)
        # audio
        self.audio_filename=os.path.join(cache_path,self.filename+"."+self.id+"."+str(self.start)+"."+str(self.end)+".wav")
        if not os.path.exists(self.audio_filename):
            self.clip.subclip(self.start, self.end).audio.write_audiofile(self.audio_filename)
        else:
            print(f"{self.audio_filename} already cached !")

    def update_and_return_isfinished(self):
        """Obtenir la bonne frame du clip"""
        self.time += 1/25
        is_finished = self.time > self.end
        if is_finished:
            self.time = self.start
        self.frame=self.clip.get_frame(t=self.time)
        return is_finished


class ClipManager:
    """Object that manage which clip to render"""
    def __init__(self, first_clip):
        self.first_launch=True
        self.current_clip=first_clip
        self.next_clip=first_clip
        self.surface=pygame.surfarray.make_surface(self.current_clip.frame.swapaxes(0, 1))

    def update(self):
        if self.first_launch is True:
            self.play_associated_audio()
            self.first_launch=False
        if self.current_clip.update_and_return_isfinished():
            self.current_clip=self.next_clip
            self.play_associated_audio()

    def get_surface(self):
        pygame.surfarray.blit_array(self.surface, self.current_clip.frame.swapaxes(0, 1))
        return self.surface
    
    def play_associated_audio(self):
        current_audio=pygame.mixer.Sound(self.current_clip.audio_filename)
        current_audio.play()
        

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
            if self.banner.top-2 < 0:
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
assets_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
cache_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)), "cache")

video1=Clip("CLIP1",assets_dir,cache_dir,"abba.mp4",40,42)
video2=Clip("CLIP2",assets_dir,cache_dir,"abba.mp4",50,52)

clip_manager=ClipManager(video1)
screen_size=clip_manager.get_surface().get_size()

# init menu
menu=Menu(dimension=(screen_size[0]-20,50))

# Prepare SCREEN
screen=pygame.display.set_mode(screen_size, 0, 32)
pygame.display.set_caption("ABBA test")

# Run the Pygame loop to keep the window open
running=True
clock=pygame.time.Clock()
while running:
    clock.tick(25)
    
    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            clip_manager.next_clip=video1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            clip_manager.next_clip=video2
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            menu.show_menu()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
            menu.hide_menu()
          
    # update objects
    clip_manager.update()
    menu.update()

    # Draw the surface onto the window
    screen.blit(clip_manager.get_surface(), (0, 0))
    screen.blit(menu.get_surface(), ((screen_size[0]-menu.width)/2, screen_size[1]-menu.height))
   
    pygame.display.flip()
    
# Quit Pygame
pygame.quit()