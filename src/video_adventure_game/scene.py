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