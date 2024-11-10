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
clips.add("CLIP_1", "PXL_20241102_124442799.TSR.mp4", 0,2)
clips.add("CLIP_2", "PXL_20241102_124508854.TSR.mp4", 0,2)
clips.add("CLIP_3", "PXL_20241102_124530530.TSR.mp4", 0,2)

# Create Scenes inventory
scene_resources = SceneResources()

scene_resources.add(Scene(clips, "SCENE_1", 1, 5)
    .add_clip("CLIP_1")
    .add_clip("CLIP_2")
    .add_clip("CLIP_3")
    .add_clip("CLIP_2")
    .add_choice("CHOIX_2", "Go scene 2", "SCENE_2")
    .add_choice("CHOIX_3", "Go scene 3", "SCENE_3")
    .add_choice("CHOIX_2_AGAIN", "Go scene 2 (bis)", "SCENE_2", 
                """history.event_has_choice_id("CHOIX_0")""")
    .add_choice("CHOIX_4", "Go scene 4", "SCENE_4")
    .set_default_choice("CHOIX_2_AGAIN"))

scene_resources.add(Scene(clips, "SCENE_2", 1, 5)
    .add_clip("CLIP_1")
    .add_clip("CLIP_2")
    .add_clip("CLIP_3")
    .add_clip("CLIP_2")
    .add_choice("CHOIX_1", "Go scene 1", "SCENE_1")
    .add_choice("CHOIX_2", "Go scene 2", "SCENE_2")
    .add_choice("CHOIX_3", "Go scene 3", "SCENE_3")
    .add_choice("CHOIX_3", "Go scene 4", "SCENE_4")
    .set_default_choice("CHOIX_1"))

scene_resources.add(Scene(clips, "SCENE_3", 1, 5)
    .add_clip("CLIP_1")
    .add_clip("CLIP_2")
    .add_clip("CLIP_3")
    .add_clip("CLIP_2")
    .add_choice("CHOIX_0", "Go scene 1", "SCENE_1")
    .set_default_choice("CHOIX_0"))

scene_resources.add(Scene(clips, "SCENE_4", 1, 5)
    .add_clip("CLIP_1")
    .add_clip("CLIP_2")
    .add_clip("CLIP_3")
    .add_clip("CLIP_2")
    .add_choice("CHOIX_0", "Go scene 1", "SCENE_1"))

# ------------------ CHECK -------------------------------
scene_resources.check_coherence()
