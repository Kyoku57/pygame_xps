import globals
from clip import ClipResources
from scene import Scene, SceneResources

# Windowed screen size
screen_size = (1280,720)

# Clip inventory
clips = ClipResources(globals.assets_dir, globals.cache_dir)
clips.add(clip_id="SCENE_1_CLIP_1", video_filename="source_video_1.mp4", start=1, end=5)
clips.add("SCENE_1_CLIP_2", "source_video_1.mp4", 6, 10)
clips.add("SCENE_1_CLIP_3", "source_video_1.mp4", 12, 16)
clips.add("SCENE_2_CLIP_1", "source_video_2.mp4", 1, 5)
clips.add("SCENE_2_CLIP_2", "source_video_2.mp4", 6, 12)
clips.add("SCENE_2_CLIP_3", "source_video_2.mp4", 13,17)
clips.add("SCENE_3_CLIP_1", "source_video_3.mp4", 2,6)
clips.add("SCENE_3_CLIP_2", "source_video_3.mp4", 8,12)
clips.add("SCENE_3_CLIP_3", "source_video_3.mp4", 14,18)
clips.add("SCENE_4_CLIP_123", "source_video_4.mp4")

# Scenes inventory
scene_resources = SceneResources()

scene_resources.add(Scene(clips_resources=clips, scene_id="SCENE_1",  menu_start_time=3, menu_duration=6)
    .add_clip("SCENE_1_CLIP_1")
    .add_clip("SCENE_1_CLIP_2")
    .add_clip("SCENE_1_CLIP_3")
    .add_choice("CHOIX_2", "Go scene 2", "SCENE_2")
    .add_choice("CHOIX_3", "Go scene 3", "SCENE_3")
    .add_choice("CHOIX_2_AGAIN", "Go scene 2 (bis)", "SCENE_2", """history.event_has_choice_id("CHOIX_0")""")
    .add_choice("CHOIX_4", "Go scene 4", "SCENE_4")
    .set_default_choice("CHOIX_2_AGAIN"))

scene_resources.add(Scene(clips, "SCENE_2", 5, 7)
    .add_clip("SCENE_2_CLIP_1")
    .add_clip("SCENE_2_CLIP_2")
    .add_clip("SCENE_2_CLIP_3")
    .add_choice("CHOIX_1", "Go scene 1", "SCENE_1")
    .add_choice("CHOIX_2", "Go scene 2", "SCENE_2")
    .add_choice("CHOIX_3", "Go scene 3", "SCENE_3")
    .add_choice("CHOIX_3", "Go scene 4", "SCENE_4")
    .set_default_choice("CHOIX_1"))

scene_resources.add(Scene(clips, "SCENE_3", 3, 6)
    .add_clip("SCENE_3_CLIP_1")
    .add_clip("SCENE_3_CLIP_2")
    .add_clip("SCENE_3_CLIP_3")
    .add_choice("CHOIX_0", "Go scene 1", "SCENE_1")
    .set_default_choice("CHOIX_0"))

scene_resources.add(Scene(clips, "SCENE_4", 1, 5)
    .add_clip("SCENE_4_CLIP_123")
    .add_choice("CHOIX_0", "Go scene 1", "SCENE_1"))
