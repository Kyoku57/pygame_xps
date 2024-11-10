import os
from clip import ClipResources
from scene import Scene, SceneResources

# Screen size
screen_size = (830,500)
full_screen = False

# debug mode
debug_mode = True

# assets and cache
assets_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
cache_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "cache")

# Clip inventory
clips = ClipResources(assets_dir,cache_dir)
clips.add("GAB_DORT", "PXL_20241102_124442799.TSR.mp4", 0,2)
clips.add("RAPH_ENTRE", "PXL_20241102_124508854.TSR.mp4", 0,2)
clips.add("GAB_DORT_ZOOM", "PXL_20241102_124530530.TSR.mp4", 0,2)

# Create Scenes inventory
scene_resources = SceneResources()

scene_resources.add(Scene(clips, "REVEIL_DE_GAB", 1, 5)
    .add_clip("GAB_DORT")
    .add_clip("RAPH_ENTRE")
    .add_clip("GAB_DORT_ZOOM")
    .add_clip("RAPH_ENTRE")
    .add_choice("BOUCLE2A", "Boucle 2", "REVEIL_DE_GAB2")
    .add_choice("BOUCLE3A", "Boucle 3", "REVEIL_DE_GAB3")
    .add_choice("BOUCLE2B", "Boucle 2", "REVEIL_DE_GAB2")
    .add_choice("BOUCLE3B", "Boucle 3", "REVEIL_DE_GAB3")
    .set_default_choice(1))

scene_resources.add(Scene(clips, "REVEIL_DE_GAB2", 1, 5)
    .add_clip("GAB_DORT")
    .add_clip("RAPH_ENTRE")
    .add_clip("GAB_DORT_ZOOM")
    .add_clip("RAPH_ENTRE")
    .add_choice("BOUCLE1C", "Boucle 1", "REVEIL_DE_GAB")
    .add_choice("BOUCLE2C", "Boucle 2", "REVEIL_DE_GAB2")
    .add_choice("BOUCLE3C", "Boucle 3", "REVEIL_DE_GAB3")
    .set_default_choice(1))

scene_resources.add(Scene(clips, "REVEIL_DE_GAB3", 1, 5)
    .add_clip("GAB_DORT")
    .add_clip("RAPH_ENTRE")
    .add_clip("GAB_DORT_ZOOM")
    .add_clip("RAPH_ENTRE")
    .add_choice("BOUCLE1", "Boucle 1", "REVEIL_DE_GAB")
    .set_default_choice(1))


# ------------------ CHECK -------------------------------

print("Check coherence with ...")
for scene_id,scene in scene_resources.scenes.items():
    scene.duration()
print(" ... durations: OK")

for scene_id,scene in scene_resources.scenes.items():
    for choice in scene.choices:
        scene_resources.get(choice.next_scene)
print(" ... scene in choice: OK")

print("EVERYTHING IS OK ! Good Game !")