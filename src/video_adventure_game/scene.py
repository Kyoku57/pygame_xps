from clip import ClipManager

class Choice:
    def __init__(self, choice_id, description, next_scene):
        self.choice_id = choice_id
        self.description = description
        self.next_scene = next_scene


class Scene:
    """A scene is a chain of clips and choices. It contains index"""
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

    def duration_to_index(self, index):
        return sum([self.ordered_clips[i].duration for i in range(index)])

    def duration(self):
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
    """Manager for scene
    Get current scene
    Get current clip
    """
    def __init__(self, scene_resources, first_scene_name):
        # Scene
        self.scene_resources = scene_resources
        self.current_scene = self.scene_resources.get(first_scene_name)
        self.next_scene = self.current_scene
        # Clips
        self.clip_index = 0
        self.clip_manager = ClipManager(self.current_scene.ordered_clips[self.clip_index])

    def update(self):
        if self.clip_manager.update_and_return_isfinished():
            # next clip if clip is finished
            self.clip_index += 1
            # is last clip of the scene ?
            if self.clip_index >= len(self.current_scene.ordered_clips):
                self.current_scene = self.next_scene
                self.clip_index = 0
            self.clip_manager.current_clip = self.current_scene.ordered_clips[self.clip_index]

    def get_surface(self):
        """Export updated Surface"""
        return self.clip_manager.get_surface()

    def get_time_by_duration(self):
        clip_time, clip_duration = self.clip_manager.get_time_by_duration()
        scene_time = self.current_scene.duration_to_index(self.clip_index) + clip_time
        return scene_time, self.current_scene.duration()
 
    def get_progress(self):
        scene_time, scene_duration = self.get_time_by_duration()
        return (scene_time)*100/(scene_duration)