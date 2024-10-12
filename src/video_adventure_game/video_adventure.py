import os, pygame, time
from moviepy.editor import VideoFileClip
from clip import ClipResources
from menu import Menu

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
        

class Choice:
    def __init__(self, choice_id, description, next_scene):
        self.choice_id = choice_id
        self.description = description
        self.next_scene = next_scene


class Scene:
    """A scene is a chain of clips and choices"""
    def __init__(self, clips_resources, scene_id, menu_start_time, menu_duration):
        # Cache data
        self.id = scene_id
        self.ordered_clips = []
        self.clips_resources = clips_resources
        # Menu management
        self.menu_start_time = menu_start_time
        self.menu_duration = menu_duration
        self.show_menu = False
        # Choices management
        self.choices = []
        self.default_choice = None

    def add_clip(self, clip_id):
        clip = self.clips_resources.get(clip_id)
        self.ordered_clips.append(clip)

    def add_choice(self, choice_id, description, next_scene):
        choice = Choice(choice_id, description, next_scene)
        self.choices.append(choice)
    
    def check_duration(self):
        scene_duration = sum([clip.duration for clip in self.ordered_clips])
        if self.menu_start_time + self.menu_duration > scene_duration:
            raise Exception(f"Menu duration({self.menu_start_time}) and Menu duration({self.menu_duration}) are superior to Scene duration({scene_duration})") 
        if self.menu_duration < 10:
            raise Exception(f"Too low value for menu_duration") 
        return scene_duration


class SceneResources:
    def __init__(self):
        self.scenes = {}

    def add(self, scene):
        """Add a new scene into resources"""
        if scene.id in self.scenes.keys():
            raise NameError(f"{scene.id} is already used !!!")
        self.scenes[scene.id]=scene

    def get(self, scene_id):
        """Get Scene by scene identifier"""
        if scene_id not in self.scenes.keys():
            raise NameError(f"{scene_id} is not in resources !!!")
        return self.scenes[scene_id]
    
    def check_coherence(self):
        pass # need to check every scene / choice exists



class SceneManager:
    def __init__(self, scene_resources):
        pass

    def get_first_scene(self):
        pass

    def get_current_scene(self):
        pass

    def get_next_scene(self):
        pass

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
scene_resources = SceneResources()
# Scene 1
scene1=Scene(clips, "SCENE_1", 3, 10)
scene1.add_clip("PIANO")
scene1.add_clip("I_WORK_ALL_NIGHT")
scene1.add_choice("GOTO_SCENE2", "Allez à la scène 2", "SCENE_2")
scene1.add_choice("GOTO_SCENE3", "Allez à la scène 3", "SCENE_3")
print(f"scene1 is about {scene1.check_duration()} seconds")
scene_resources.add(scene1)
# Scene 2
scene2=Scene(clips, "SCENE_2", 3, 10)
scene2.add_clip("WEATHLY_MEN")
scene2.add_clip("MONEY_MONEY")
scene1.add_choice("GOTO_SCENE1", "Allez à la scène 1", "SCENE_1")
scene1.add_choice("GOTO_SCENE3", "Allez à la scène 3", "SCENE_3")
print(f"scene2 is about {scene2.check_duration()} seconds")
scene_resources.add(scene2)
# Scene 3
scene3=Scene(clips,"SCENE_3", 3, 10)
scene3.add_clip("AHHHHHHHHHH")
scene3.add_clip("HIGHER")
scene1.add_choice("GOTO_SCENE1", "Allez à la scène 1", "SCENE_1")
scene1.add_choice("GOTO_SCENE2", "Allez à la scène 2", "SCENE_2")
print(f"scene3 is about {scene3.check_duration()} seconds")
scene_resources.add(scene3)

# Current scene 
current_scene = scene_resources.get("SCENE_1")

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

    # debug
    time, duration=clip_manager.get_time_by_duration()
    print(f"{clip_manager.current_clip.id}: {time:.3f} / {duration:.3f} " 
          + f" ({clip_manager.get_progress():.1f}%) -> {'Menu On' if clip_manager.show_menu else 'Menu Off'}"
          + f" -> {clip_manager.next_clip.id}")
    pygame.draw.rect(screen, pygame.Color(255,int(255*time/duration),0), pygame.Rect(0,0,screen_size[0]*time/duration,5))
    
    # render
    pygame.display.flip()


    
# Quit Pygame
pygame.quit()