import os
from clip import ClipResources
from scene import Scene, SceneResources

# Screen size
screen_size=(830,450)

# assets and cache
assets_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
cache_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)), "cache")

# Clip inventory
clips = ClipResources(assets_dir,cache_dir)
clips.add("GAB_DORT", "PXL_20241102_124442799.TSR.mp4")
clips.add("RAPH_ENTRE", "PXL_20241102_124508854.TSR.mp4")
clips.add("GAB_DORT_ZOOM", "PXL_20241102_124530530.TSR.mp4")

# Create Scenes inventory
scene_resources = SceneResources()

scene_resources.add(Scene(clips, "REVEIL_DE_GAB", 15, 9)\
    .add_clip("GAB_DORT")\
    .add_clip("RAPH_ENTRE")\
    .add_clip("GAB_DORT_ZOOM")
    .add_choice("BOUCLE", "Réveiller fort !!", "REVEIL_DE_GAB"))

# Check coherence with time
for scene_id,scene in scene_resources.scenes.items():
    print(f"scene {scene_id} is about {scene.duration()} seconds")
print("EVERYTHING IS OK ! Good Game !")