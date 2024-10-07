import os, pygame, uuid
from moviepy.editor import VideoFileClip
from enum import Enum

class Clip:
    """Clip that represent a subset of a video"""
    def __init__(self, id, assets_path, cache_path, filename, start, end):
        # time-management
        self.id=id
        self.start,self.end=start,end
        self.duration=self.end-self.start
        self.time=0
        # path
        self.assets_path=assets_path
        self.cache_path=cache_path
        self.filename=filename
        # video subclip
        self.video_path=os.path.join(assets_path,filename)
        self.clip=VideoFileClip(self.video_path)
        self.clip=self.clip.subclip(self.start, self.end)
        self.frame=self.clip.get_frame(t=self.time)
        # audio
        self.audio=None
        self.audio_filename=os.path.join(self.cache_path,
            self.id+"."+self.filename+"."+str(self.start)+"."+str(self.end)+".wav")
        self.cache_audio()

    def reset(self):
        self.time=0
       
    def update_and_return_isfinished(self):
        """Obtain the right frame"""
        self.frame=self.clip.get_frame(t=self.time)
        self.time += 1/25
        is_finished = self.time > self.duration
        if is_finished:
            self.reset()
        return is_finished
    
    def cache_audio(self):
        """Extract and create audio cache for the clip"""
        # cache intermediare file
        if not os.path.exists(self.audio_filename):
            self.clip.audio.write_audiofile(self.audio_filename)
        else:
            print(f"{self.audio_filename} already cached !")
        # cache audio object
        if self.audio is None:
            self.audio=pygame.mixer.Sound(self.audio_filename)


class ClipManager:
    """Object that manage which clip to render"""
    def __init__(self, first_clip):
        self.first_launch=True
        self.current_clip=first_clip
        self.next_clip=first_clip
        self.surface=pygame.surfarray.make_surface(self.current_clip.frame.swapaxes(0, 1))
        self.show_menu=False

    def update(self):
        """Update frame for Surface buffer and play audio if necessary"""
        if self.first_launch is True:
            self.play_associated_audio()
            self.first_launch=False
        if self.current_clip.update_and_return_isfinished():
            self.current_clip=self.next_clip
            self.play_associated_audio()
        # inform that the menu can be shown
        if self.get_progress() > 20:
            self.show_menu=True
        if self.get_progress() > 80:
            self.show_menu=False

    def get_surface(self):
        """Export updated Surface"""
        pygame.surfarray.blit_array(self.surface, self.current_clip.frame.swapaxes(0, 1))
        return self.surface
    
    def play_associated_audio(self):
        """Play audio"""
        self.current_clip.audio.play()

    def get_progress(self):
        return (self.current_clip.time)*100/(self.current_clip.duration)
    
    def get_time_by_duration(self):
        return self.current_clip.time, self.current_clip.duration
        

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


class ClipResources:
    """List of clips"""
    def __init__(self):
        self.clips = {}

    def add(self, clip):
        if clip.id in self.clips.keys():
            raise NameError(f"{clip.id} is already used !!!")
        self.clips[clip.id]=clip

    def get(self, clip_id):
        if clip_id not in self.clips.keys():
            raise NameError(f"{clip_id} is not in resources !!!")
        return self.clips[clip_id]

class Choice:
    pass

class Scene:
    def __init__(self, clips_resources):
        self.ordered_clips=[]
        self.choices=[]
        self.clips_resources=clips_resources

    def add_clip(self, clip_id):
        clip=self.clips_resources.get(clip_id)
        self.ordered_clips.append(clip)
    
    def get_duration(self):
        return sum([clip.duration for clip in self.ordered_clips])


# Initialize Pygame
pygame.init()

# assets and cache
assets_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
cache_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)), "cache")

# Clip management
clips=ClipResources()
clips.add(Clip("PIANO",assets_dir,cache_dir,"abba.mp4",1,9.5))
clips.add(Clip("I_WORK_ALL_NIGHT",assets_dir,cache_dir,"abba.mp4",13,29))
clips.add(Clip("WEATHLY_MEN",assets_dir,cache_dir,"abba.mp4",33.5,43))
clips.add(Clip("MONEY_MONEY",assets_dir,cache_dir,"abba.mp4",48,63))
clips.add(Clip("AHHHHHHHHHH",assets_dir,cache_dir,"abba.mp4",133.5,146))
clips.add(Clip("HIGHER",assets_dir,cache_dir,"abba.mp4",149.5,165))

# Create scenes
scene1=Scene(clips)
scene1.add_clip("PIANO")
scene1.add_clip("I_WORK_ALL_NIGHT")

scene2=Scene(clips)
scene2.add_clip("WEATHLY_MEN")
scene2.add_clip("MONEY_MONEY")

scene3=Scene(clips)
scene3.add_clip("AHHHHHHHHHH")
scene3.add_clip("HIGHER")

print(f"scene1 is about {scene1.get_duration()} seconds")
print(f"scene2 is about {scene2.get_duration()} seconds")
print(f"scene3 is about {scene3.get_duration()} seconds")

# ClipManagement
clip_manager=ClipManager(clips.get("WEATHLY_MEN"))
screen_size=clip_manager.get_surface().get_size()

# init menu
menu=Menu(dimension=(screen_size[0]-50,60))

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
        if clip_manager.show_menu:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                clip_manager.next_clip=clips.get("PIANO")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                clip_manager.next_clip=clips.get("I_WORK_ALL_NIGHT")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                clip_manager.next_clip=clips.get("WEATHLY_MEN")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_v:
                clip_manager.next_clip=clips.get("MONEY_MONEY")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                clip_manager.next_clip=clips.get("AHHHHHHHHHH")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                clip_manager.next_clip=clips.get("HIGHER")
          
    # update objects to draw
    clip_manager.update()
    if clip_manager.show_menu:
        menu.show() 
    else: 
        menu.hide()
    menu.update()

    # Draw the surface onto the window
    screen.blit(clip_manager.get_surface(), (0, 0))
    screen.blit(menu.get_surface(), ((screen_size[0]-menu.width)/2, screen_size[1]-menu.height))
    pygame.display.flip()

    # debug
    time, duration=clip_manager.get_time_by_duration()
    print(f"{clip_manager.current_clip.id}: {time:.3f} / {duration:.3f} " 
          + f" ({clip_manager.get_progress():.1f}%) -> {'Menu On' if clip_manager.show_menu else 'Menu Off'}"
          + f" -> {clip_manager.next_clip.id}")
    
# Quit Pygame
pygame.quit()