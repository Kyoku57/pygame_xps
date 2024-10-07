import os, pygame, uuid
from moviepy.editor import VideoFileClip
from enum import Enum

class Clip:
    """Clip that represent a subset of a video"""
    def __init__(self, id, assets_path, cache_path, filename, start, end):
        # time-management
        self.id=id
        self.start,self.end=start,end
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
        self.audio=None
        self.audio_filename=os.path.join(self.cache_path,
            self.id+"."+self.filename+"."+str(self.start)+"."+str(self.end)+".wav")
        self.cache_audio()
       
    def update_and_return_isfinished(self):
        """Obtain the right frame"""
        self.time += 1/25
        is_finished = self.time > self.end
        if is_finished:
            self.time = self.start
        self.frame=self.clip.get_frame(t=self.time)
        return is_finished
    
    def cache_audio(self):
        """Extract and create audio cache for the clip"""
        # cache intermediare file
        if not os.path.exists(self.audio_filename):
            self.clip.subclip(self.start, self.end).audio.write_audiofile(self.audio_filename)
        else:
            print(f"{self.audio_filename} already cached !")
        # cache audio object
        if self.audio is None:
            self.audio=pygame.mixer.Sound(self.audio_filename)

    def get_progress(self):
        return (self.time-self.start)*100/(self.end-self.start)


class ClipManager:
    """Object that manage which clip to render"""
    def __init__(self, first_clip):
        self.first_launch=True
        self.current_clip=first_clip
        self.next_clip=first_clip
        self.surface=pygame.surfarray.make_surface(self.current_clip.frame.swapaxes(0, 1))

    def update(self):
        """Update frame for Surface buffer and play audio if necessary"""
        if self.menu is not None:
            if self.current_clip.get_progress() > 20:
                self.menu.show()
            if self.current_clip.get_progress() > 80:
                self.menu.hide()
        if self.first_launch is True:
            self.play_associated_audio()
            self.first_launch=False
        if self.current_clip.update_and_return_isfinished():
            self.current_clip=self.next_clip
            self.play_associated_audio()

    def get_surface(self):
        """Export updated Surface"""
        pygame.surfarray.blit_array(self.surface, self.current_clip.frame.swapaxes(0, 1))
        return self.surface
    
    def play_associated_audio(self):
        """Play audio"""
        self.current_clip.audio.play()

    def set_menu(self, menu):
        self.menu=menu
        

class Menu:
    """Menu"""
    def __init__(self, dimension):
        self.height=dimension[1]
        self.width=dimension[0]
        self.surface=pygame.Surface(dimension, pygame.SRCALPHA)
        self.banner=pygame.Rect(0,self.height, self.width,self.height)
        self.visible=False
        self.animation_show=False
        self.animation_hide=False
    
    def toggle(self):
        if self.visible is True:
            self.hide()
        else:
            self.show()

    def show(self):
        self.animation_hide=False
        self.animation_show=True

    def hide(self):
        self.animation_hide=True
        self.animation_show=False

    def update(self):
        if self.animation_show is True:
            if self.banner.top-2 < 0:
                self.banner.top=0
                self.animation_show=False
                self.visible=True
            else:
                self.banner.move_ip(0,-2)
        
        if self.animation_hide is True:
            if self.banner.top >= self.height:
                self.banner.top=self.height
                self.animation_hide=False
                self.visible=False
            else:
                self.banner.move_ip(0,2)

    def get_surface(self):
        self.surface.fill(pygame.SRCALPHA)
        self.surface=self.surface.convert_alpha()
        pygame.draw.rect(self.surface, pygame.Color(0,50,80), menu.banner)
        return self.surface

    

# Initialize Pygame
pygame.init()

# assets and cache
assets_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
cache_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)), "cache")

# Clip management
weathly_men_video=Clip("WEATHLY_MEN_CLIP1",assets_dir,cache_dir,"abba.mp4",33.5,43)
money_money_video=Clip("MONEY_MONEY_CLIP2",assets_dir,cache_dir,"abba.mp4",48,55)
aahhhaahhhh_video=Clip("Aahhhaahhhh_CLIP3",assets_dir,cache_dir,"abba.mp4",133,146)


clip_manager=ClipManager(weathly_men_video)
screen_size=clip_manager.get_surface().get_size()

# init menu
menu=Menu(dimension=(screen_size[0]-50,60))
clip_manager.set_menu(menu)

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
        # manage quit()
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        # choose clip extract
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            clip_manager.next_clip=weathly_men_video
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            clip_manager.next_clip=money_money_video
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            clip_manager.next_clip=aahhhaahhhh_video
        # menu interaction
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            menu.show()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_h:
            menu.hide()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_t:
            menu.toggle()
          
    # update objects to draw
    clip_manager.update()
    menu.update()

    # Draw the surface onto the window
    screen.blit(clip_manager.get_surface(), (0, 0))
    screen.blit(menu.get_surface(), ((screen_size[0]-menu.width)/2, screen_size[1]-menu.height))
    pygame.display.flip()

    print(clip_manager.current_clip.get_progress())
    
# Quit Pygame
pygame.quit()