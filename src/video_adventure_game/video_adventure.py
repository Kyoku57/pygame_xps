import os, pygame, time
from moviepy.editor import VideoFileClip
from enum import Enum

class ClipResources:
    """List of clips"""
    def __init__(self, assets_dir, cache_dir):
        self.video_cache = {}
        self.clips = {}
        self.assets_dir=assets_dir
        self.cache_dir=cache_dir

    def add(self, clip_id, video_filename, start, end):
        """Add a new clip into resources"""
        if clip_id in self.clips.keys():
            raise NameError(f"{clip.id} is already used !!!")
        if video_filename in self.video_cache.keys():
            print(f"{video_filename} is already in video cache !!!")
        else:
            self.video_cache[video_filename]=VideoFileClip(os.path.join(assets_dir,video_filename))

        clip=Clip(clip_id, cache_dir, self.video_cache[video_filename], start, end)
        self.clips[clip.id]=clip

    def get(self, clip_id):
        """Get clip by clip identifier"""
        if clip_id not in self.clips.keys():
            raise NameError(f"{clip_id} is not in resources !!!")
        return self.clips[clip_id]

class Clip:
    """Clip that represent a subset of a video"""
    def __init__(self, id, cache_path, clip, start, end):
        # time-management
        self.id=id
        self.start,self.end=start,end
        self.duration=self.end-self.start
        self.time=0
        # path
        self.cache_path=cache_path
        # video subclip
        self.clip=clip
        self.clip=self.clip.subclip(self.start, self.end)
        self.frame=self.clip.get_frame(t=self.time)
        # audio
        self.audio=None
        self.audio_filename=os.path.join(self.cache_path,
            self.id+"."+str(self.start)+"."+str(self.end)+".wav")
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
    def __init__(self, init_position, dimension):
        # position, dimension
        self.width,self.height = dimension
        self.init_left,self.init_top = init_position
        self.left,self.top = init_position

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
        img=self.font.render("W -> Clip1    X -> Clip2    C -> Clip3", True, (200,200,200))
        img2=self.font.render("V -> Clip4    B -> Clip5    N -> Clip6", True, (200,200,200))
        self.surface.blit(img, (20,10))
        self.surface.blit(img2, (20,35))
        #experiment text rendering
        return self.surface

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
clips=ClipResources(assets_dir,cache_dir)
clips.add("PIANO","abba.mp4",1,9.5)
clips.add("I_WORK_ALL_NIGHT","abba.mp4",13,29)
clips.add("WEATHLY_MEN","abba.mp4",33.5,43)
clips.add("MONEY_MONEY","abba.mp4",48,63)
clips.add("AHHHHHHHHHH","abba.mp4",133,146)
clips.add("HIGHER","abba.mp4",149.5,165)

# Create scenes
scene1=Scene(clips)
scene1.add_clip("PIANO")
scene1.add_clip("I_WORK_ALL_NIGHT")
print(f"scene1 is about {scene1.get_duration()} seconds")

scene2=Scene(clips)
scene2.add_clip("WEATHLY_MEN")
scene2.add_clip("MONEY_MONEY")
print(f"scene2 is about {scene2.get_duration()} seconds")

scene3=Scene(clips)
scene3.add_clip("AHHHHHHHHHH")
scene3.add_clip("HIGHER")
print(f"scene3 is about {scene3.get_duration()} seconds")

# ClipManagement and screen size
clip_manager=ClipManager(clips.get("PIANO"))
screen_size=clip_manager.get_surface().get_size()

# init menu
menu_dimension=(screen_size[0]-50,60)
menu_init_position=((screen_size[0]-menu_dimension[0])/2, screen_size[1])
menu=Menu(menu_init_position, menu_dimension)

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
    screen.blit(menu.get_surface(), (menu.left, menu.top))
    pygame.display.flip()

    # debug
    time, duration=clip_manager.get_time_by_duration()
    print(f"{clip_manager.current_clip.id}: {time:.3f} / {duration:.3f} " 
          + f" ({clip_manager.get_progress():.1f}%) -> {'Menu On' if clip_manager.show_menu else 'Menu Off'}"
          + f" -> {clip_manager.next_clip.id}")
    
# Quit Pygame
pygame.quit()