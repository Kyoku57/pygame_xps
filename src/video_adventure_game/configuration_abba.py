import os
from clip import ClipResources
from scene import Scene, SceneResources

# Screen size
screen_size = (1000,500)
full_screen = False

# debug mode
debug_mode = True

# assets and cache
assets_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
cache_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "cache")

# Clip inventory
clips = ClipResources(assets_dir,cache_dir)
clips.add("PIANO","abba.mp4",1,9.5)
clips.add("I_WORK_ALL_NIGHT","abba.mp4",13,29)
clips.add("WEATHLY_MEN","abba.mp4",33.5,43)
clips.add("MONEY_MONEY","abba.mp4",48,63)
clips.add("AHHHHHHHHHH","abba.mp4",133,146)
clips.add("HIGHER","abba.mp4",149.5,165)

# Create Scenes inventory
scene_resources = SceneResources()

# Scene 1
scene_resources.add(Scene(clips, "SCENE_1", 3, 15)
    .add_clip("PIANO")
    .add_clip("I_WORK_ALL_NIGHT")
    .add_choice("GOTO_SCENE2", "Allez à la scène 2", "SCENE_2")
    .add_choice("GOTO_SCENE3", "Allez à la scène 3", "SCENE_3"))

# Scene 2
scene_resources.add(Scene(clips, "SCENE_2", 3, 15)
    .add_clip("WEATHLY_MEN")
    .add_clip("MONEY_MONEY")
    .add_choice("GOTO_SCENE1", "Allez à la scène 1", "SCENE_1")
    .add_choice("GOTO_SCENE3", "Allez à la scène 3", "SCENE_3"))

# Scene 3
scene_resources.add(Scene(clips,"SCENE_3", 3, 15)
    .add_clip("AHHHHHHHHHH")
    .add_clip("HIGHER")
    .add_choice("GOTO_SCENE1", "Allez à la scène 1", "SCENE_1")
    .add_choice("GOTO_SCENE2", "Allez à la scène 2", "SCENE_2"))




# ------------------ CHECK -------------------------------
scene_resources.check_coherence()
