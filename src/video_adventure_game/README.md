# Video Adventure Game

The aim of this little project is to offer a way to create a video adventure game with PyGame.

![SplashScreen](./splash.png)

## Requirements

Install Python >= 3.12 : https://www.python.org/downloads/

Get game from GitHub:
```bash
# Clone package with git 
git clone https://github.com/Kyoku57/pygame_xps.git
cd pygame_xps/src/video_adventure_game
```
OR download direct and unzip from:
https://github.com/Kyoku57/pygame_xps/archive/refs/heads/main.zip  

Go into ```pygame_xps/src/video_adventure_game``` directory.

Install dependencies:
```bash
# install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
# OR if you want to install the three dependencies by yourselves
python -m pip install pygame moviepy pyinstaller
```

## Quick run

The project is provided with a default scenario and clips.

To test it, just run the following command
```bash
python main.py
# or 
python main.py --fullscreen --debug
```

or if you want a packaged version with splash screen, run the following commands
```bash
pyinstaller main.spec
```

After build, double-click on the ```main``` executable in the ```./dist/``` directory.  

> **NOTE:** You can create a shortcut or use command line to add option like ```--fullscreen``` or ```--debug``` during launch.


## Some notes before starting ...

The game is calibrated to run video at the framerate of 25 img/sec. You can use the following ffmpeg command to resize video and put framerate to 25.

```bash
ffmpeg -i myvideo.mp4 -s 800x450 -filter:v fps=25 myvideo.resized.mp4
```

## How to structure the game

There are two ways to structure and describe the scenario
- usage of the default structure (used for packaging - see later):
    - put your ```*.mp4``` files into ```./assets/``` directory
    - the ```./cache/``` directory will be used for audio cache
    - edit ```configuration.py``` file
- usage external configuration structure:
    - create a assets directory to store ```*.mp4``` files
    - create an empty directory to store the cache
    - create a python file to define scenario


## How to edit the scenario file

### Requirements

- Put your ```*.mp4``` files into the default ```./assets/``` directory or create a new one,
- If needed, use the ```resize.sh``` scripts to batch resize your files,
- And open the default ```configuration.py``` scenario file or create a new one.

For next example, we want 4 Scenes linked each other to create the scenario.

### Step 1: Edit scenario and start with mandatory imports

```python
import globals
from clip import ClipResources
from scene import Scene, SceneResources
```

Define the windowed mode resolution
```python
screen_size = (830,500) # can be clips resolution but can be other values too
```

### Step 2: Declare your clips

We declare clips from the different videos (but can be the same)

```python
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
```
> **NOTE:** the ClipID should be unique. The clips are cached in memory.

### Step 3: Declare your first Scene

```python
scene_resources = SceneResources()
```

We want a first scene that launch the following clips:
- SCENE_1_CLIP_1 > SCENE_1_CLIP_2 > SCENE_1_CLIP_3 

The menu appears at the third second of the scene and last 6 secondes. If no choice is selected, it will be the default one or the first one.

And we want the following available Choices:
- Go scene 2
    - ChoiceIdentifier for history: CHOIX_2
    - Go to SceneIdentifier: SCENE_2
    - Condition: Always True
- Go scene 3
    - ChoiceIdentifier for history: CHOIX_3
    - Go to SceneIdentifier: SCENE_3
    - Condition: Always True
- Go scene 2 (bis)
    - ChoiceIdentifier for history: CHOIX_2_AGAIN
    - Go to SceneIdentifier: SCENE_3
    - Condition: the history of Events contains ChoiceIdendifier "CHOIX_0"
- Go scene 4
    - Choice identifier for history: CHOIX_4
    - Go to SceneIdentifier: SCENE_4
    - Condition: Always True

Go scene 2 (bis) will be the default choice (hidden or not).

In the scenario file, the code looks like

```python
scene_resources.add(Scene(clips_resources=clips, scene_id="SCENE_1",  menu_start_time=3, menu_duration=6)
    .add_clip("SCENE_1_CLIP_1")
    .add_clip("SCENE_1_CLIP_2")
    .add_clip("SCENE_1_CLIP_3")
    .add_choice("CHOIX_2", "Go Scene 2", "SCENE_2")
    .add_choice("CHOIX_3", "Go Scene 3", "SCENE_3")
    .add_choice("CHOIX_2_BIS", "Go Scene 2 (bis)", "SCENE_2", """history.event_has_choice_id("CHOIX_0")""")
    .add_choice("CHOIX_4", "Go Scene 4", "SCENE_4")
    .set_default_choice("CHOIX_2_BIS"))
```

### Step 4: Declare others Scenes

```python
# New scene with 4 choice, the second is the default one
scene_resources.add(Scene(clips, "SCENE_2", 1, 5)
scene_resources.add(Scene(clips, "SCENE_2", 5, 7)
    .add_clip("SCENE_2_CLIP_1")
    .add_clip("SCENE_2_CLIP_2")
    .add_clip("SCENE_2_CLIP_3")
    .add_choice("CHOIX_1", "Go Scene 1", "SCENE_1")
    .add_choice("CHOIX_2", "Go Scene 2", "SCENE_2")
    .add_choice("CHOIX_3", "Go Scene 3", "SCENE_3")
    .add_choice("CHOIX_3", "Go Scene 4", "SCENE_4")
    .set_default_choice("CHOIX_2"))

# New scene but there is only one choice
# Menu will not show when only one visible choice.
scene_resources.add(Scene(clips, "SCENE_3", 3, 6)
    .add_clip("SCENE_3_CLIP_1")
    .add_clip("SCENE_3_CLIP_2")
    .add_clip("SCENE_3_CLIP_3")
    .add_choice("CHOIX_0", "Go Scene 1", "SCENE_1")
    .set_default_choice("CHOIX_0"))

# Same as SCENE_3 with the omission of the default choice
# Default choice can be omitted because there is only one choice
# Menu will not show when only one visible choice.
scene_resources.add(Scene(clips, "SCENE_4", 1, 5)
    .add_clip("SCENE_4_CLIP_123")
    .add_choice("CHOIX_0", "Go Scene 1", "SCENE_1"))
```

Your scenario is ready !

## Launch the game for testing

```bash
# start with default config with assets, cache directories and configuration.py file
python main.py 

# start in full screen
python main.py --fullscreen 

# start with debug mode
python main.py --debug

# start with custom assets directory
python main.py --assets-dir=<path_to_assets>\
  --cache-dir=<path_to_cache>\
  --config-file=<path_to_scenario_file>
```

The main program analyses the scenario file to register clips, create audio cache, calculate menu timing. Errors are raised if:
- assets_dir, cache_dir, scenario file missing,
- Clips or Scenes don't exist,
- Clip ID or Scene ID are duplicated,
- Choice is linked to a missing Scene Identifier,
- if timing for menu is not coherent with the scene duration,

If no error, the game is launched ! Congratulations !


## Build executable

You can build a .exe version of your game with pyinstaller module.  
The version depends on the installed version of Python and Operating System.

### First option - default configuration

You have put your ```*.mp4``` files into the default ```./assets/``` directory and edit the default ```configuration.py``` file.

```bash
pyinstaller main.spec
```

A new ```./dist/``` directory contains the ```main.exe```.

Double click on it to launch the game. 

### Other option - custom configuration

First launch default pyinstaller configuration

```bash
pyinstaller main.spec
```

A new```./dist/``` directory contains the ```main.exe```.

Just launch the game directly on command line or with a custom shorcut

```bash
main.exe --assets-dir=<path_to_assets> --config-file=<path_to_scenario_file>
# You can had the other classic parameters --fullscreen and --cache-dir if needed
```

> **NOTE:** it depends if you want to release the game as a directory with main, scenario and assets seperatly or all in the .exe file.

### More customization

You can change the splash screen configuration:
- edit the ```splash.png``` image or create a new PNG file.
- edit the ```main.spec``` to the Splash section to edit font, size, ...


## References

### Pygame

- https://ryanstutorials.net/pygame-tutorial/pygame-keyboard-input.php
- https://pygame.readthedocs.io/en/latest/rect/rect.html
- https://www.pygame.org/docs/tut/ChimpLineByLine.html
- https://fr.wikibooks.org/wiki/Pygame/Chimp_-_Ligne_par_ligne
- https://stackoverflow.com/questions/21356439/how-to-load-and-play-a-video-in-pygame 
- https://www.pygame.org/docs/tut/MoveIt.html
- https://numerique.ostralo.net/pygame/partie4_les_objets_de_type_surface/b_dessiner.htm
- https://stackoverflow.com/questions/61578694/difference-between-rect-move-and-rect-move-ip-in-pygame
- https://www.reddit.com/r/pygame/comments/wpotwv/how_do_i_make_an_entity_move_forward_relative_to/
- https://www.pygame.org/docs/ref/rect.html#pygame.Rect.collideobjects
- https://medium.com/featurepreneur/extracting-audio-from-video-using-pythons-moviepy-library-e351cd652ab8 
- https://stackoverflow.com/questions/23982907/how-to-center-text-in-pygame 

### FFmpeg

- https://www.malekal.com/comment-utiliser-ffmpeg-exemples/

### Pyinstaller
- https://pyinstaller.org/en/stable/
- https://pyinstaller.org/en/stable/spec-files.html
- https://pyinstaller.org/en/stable/advanced-topics.html#pyi-splash-module-detailed