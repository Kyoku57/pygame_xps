import pygame
from clip import Clip

class Choice:
    def __init__(self, id, description, next_scene, condition, summary):
        self.id = id
        self.description = description
        self.summary = summary
        self.next_scene = next_scene
        self.condition = condition


class Scene:
    """A scene is a chain of clips and choices. It contains index"""
    def __init__(self, clips_resources, scene_id, menu_start_time, menu_duration):
        """Init scene object"""
        # Cache data
        self.id = scene_id
        self.ordered_clips = []
        self.clips_resources = clips_resources
        # Menu management
        self.menu_start_time = menu_start_time
        self.menu_duration = menu_duration
        self.menu_end_time = menu_start_time + menu_duration
        # Choices management
        self.choices = []
        self.default_choice = None

    def add_clip(self, clip_id):
        """Add a clip to the scene"""
        clip = self.clips_resources.get(clip_id)
        self.ordered_clips.append(clip)
        return self

    def add_choice(self, choice_id, description, next_scene, condition="True", summary=""):
        """Add a choice to the scene"""
        choice = Choice(choice_id, description, next_scene, condition, summary)
        self.choices.append(choice)
        if len(self.choices)==1:
            self.default_choice = choice
        return self
    
    def set_default_choice(self, default_choice_id):
        """Set the default choice
        """
        for choice in self.choices:
            if choice.id == default_choice_id:
                self.default_choice = choice
        if self.default_choice is None:
            raise Exception(f"In scene {self.id}, choice ID {default_choice_id} doesn't exist.")
        return self

    def duration_to_index(self, index):
        """Get duration from beginning of the scene, to the time index"""
        return sum([self.ordered_clips[i].duration for i in range(index)])

    def duration(self):
        """Get total duration and perform check on duration from menu and scene"""
        scene_duration = sum([clip.duration for clip in self.ordered_clips])
        if self.menu_start_time + self.menu_duration > scene_duration:
            raise Exception(f"In scene {self.id}, Menu start({self.menu_start_time}) + Menu duration({self.menu_duration}) are superior to Scene duration({scene_duration})") 
        if self.menu_duration < 3:
            raise Exception(f"In scene {self.id}, too low value for menu_duration") 
        return scene_duration
    

class SceneResources:
    def __init__(self):
        self.scenes = {}
        self.first_id = None

    def add(self, scene):
        """Add a new scene into resources"""
        if scene.id in self.scenes.keys():
            raise NameError(f"{scene.id} is already used !!!")
        self.scenes[scene.id]=scene
        if self.first_id is None:
            self.first_id = scene.id

    def get(self, scene_id):
        """Get Scene by scene identifier"""
        if scene_id not in self.scenes.keys():
            raise NameError(f"{scene_id} is not in resources !!!")
        return self.scenes[scene_id]
    
    def check_coherence(self):
        """Test scene coherence
            - Duration
            - Choice existence
            - Scene existence
        """
        print("Check coherence with ...")
        for scene_id,scene in self.scenes.items():
            scene.duration()
        print(" ... durations: OK")

        for scene_id,scene in self.scenes.items():
            if len(scene.choices) == 0:
                raise Exception(f"In scene {scene_id}, there is no choice. You need at least one choice to define next scene.")
            for choice in scene.choices:
                self.get(choice.next_scene)
        print(" ... scene in choice: OK")
        print("EVERYTHING IS OK ! Good Game !")


class SceneManager:
    """Manager for scene
    Get current scene
    Get current clip: if clip_index is 0 then the Scene is starting
    """
    def __init__(self, scene_resources, first_scene_id):
        # Scene
        self.scene_resources = scene_resources
        self.current_scene = self.scene_resources.get(first_scene_id)
        self.next_scene = self.current_scene
        # Clips
        self.clip_index = 0
        self.current_clip = self.current_scene.ordered_clips[self.clip_index]
        # Status
        self.is_starting = True
        self.__is_never_updated = True
        self.is_clip_finished = False

    def update_and_return_isfinished(self):
        # Tricky start detection for the very first time of update
        if self.__is_never_updated is True:
            self.__is_never_updated = False
        else:
            self.is_starting = False

        # Launch audio is needed
        if self.current_clip.time == 0:
            self.current_clip.play_audio()

        # Update clip and detect end. Reset will be done in the next "tick"
        if self.current_clip.update_and_return_isfinished():
            self.is_clip_finished = True

        return self.is_clip_finished

    def process_next_clip(self):
        """Rendering is already done in the previous "tick" so get next_scene
        """
        # reset flag
        self.is_clip_finished = False
        # next clip of the scene or next scene if finished
        self.clip_index += 1
        if self.clip_index >= len(self.current_scene.ordered_clips):
            self.current_scene = self.next_scene
            self.clip_index = 0
            self.is_starting = True
        # next clip
        next_clip = self.current_scene.ordered_clips[self.clip_index]
        self.current_clip = next_clip
        self.current_clip.reset()

    def set_next_scene(self, scene_id):
        self.next_scene = self.scene_resources.get(scene_id)

    def get_surface(self, screen_size):
        """Export updated Surface depends on screen size for scale
           and prepare next clip after rendering
        """
        surface = None
        if (self.current_clip.get_surface().get_size() == screen_size):
            surface = self.current_clip.get_surface()
        else:
            ratio_source = self.current_clip.get_surface().get_size()[0]/self.current_clip.get_surface().get_size()[1]
            ratio_screen = screen_size[0]/screen_size[1]
            if ratio_source > ratio_screen:
                target_width = screen_size[0]
                target_height = screen_size[0] / ratio_source
            else:
                target_height = screen_size[1]
                target_width = screen_size[1] * ratio_source
            surface = pygame.transform.scale(self.current_clip.get_surface(), (target_width, target_height))

        return surface

    def get_time_by_duration(self):
        clip_time, clip_duration = self.current_clip.get_time_by_duration()
        scene_time = self.current_scene.duration_to_index(self.clip_index) + clip_time
        return scene_time, self.current_scene.duration()
 
    def get_progress(self):
        scene_time, scene_duration = self.get_time_by_duration()
        return (scene_time)*100/(scene_duration)
