import os
from clip import ClipResources
from scene import Scene, SceneResources

# assets and cache
assets_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
cache_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)), "cache")

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
scene1 = Scene(clips, "SCENE_1", 3, 10)
scene1.add_clip("PIANO")
scene1.add_clip("I_WORK_ALL_NIGHT")
scene1.add_choice("GOTO_SCENE2", "Allez à la scène 2", "SCENE_2")
scene1.add_choice("GOTO_SCENE3", "Allez à la scène 3", "SCENE_3")
print(f"scene1 is about {scene1.duration()} seconds")
scene_resources.add(scene1)
# Scene 2
scene2 = Scene(clips, "SCENE_2", 3, 10)
scene2.add_clip("WEATHLY_MEN")
scene2.add_clip("MONEY_MONEY")
scene1.add_choice("GOTO_SCENE1", "Allez à la scène 1", "SCENE_1")
scene1.add_choice("GOTO_SCENE3", "Allez à la scène 3", "SCENE_3")
print(f"scene2 is about {scene2.duration()} seconds")
scene_resources.add(scene2)
# Scene 3
scene3 = Scene(clips,"SCENE_3", 3, 10)
scene3.add_clip("AHHHHHHHHHH")
scene3.add_clip("HIGHER")
scene1.add_choice("GOTO_SCENE1", "Allez à la scène 1", "SCENE_1")
scene1.add_choice("GOTO_SCENE2", "Allez à la scène 2", "SCENE_2")
print(f"scene3 is about {scene3.duration()} seconds")
scene_resources.add(scene3)