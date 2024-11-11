import globals
from clip import ClipResources
from scene import Scene, SceneResources

# Windowed screen size
screen_size = (830,500)

# Clip inventory
clips = ClipResources(globals.assets_dir, globals.cache_dir)
clips.add("CLIP_1", "clip_video1.mp4", 0,2)
clips.add("CLIP_2", "clip_video2.mp4", 0,2)
clips.add("CLIP_3", "clip_video3.mp4", 0,2)

# Scenes inventory
scene_resources = SceneResources()

scene_resources.add(Scene(clips, "SCENE_1", 1, 5)
    .add_clip("CLIP_1")
    .add_clip("CLIP_2")
    .add_clip("CLIP_3")
    .add_clip("CLIP_2")
    .add_choice("CHOIX_2", "Go scene 2", "SCENE_2")
    .add_choice("CHOIX_3", "Go scene 3", "SCENE_3")
    .add_choice("CHOIX_2_AGAIN", "Go scene 2 (bis)", "SCENE_2", """history.event_has_choice_id("CHOIX_0")""")
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
