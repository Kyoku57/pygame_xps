# Video Adventure Game

The aim of this little project is to offer a way to create a video adventure game with PyGame.

## Requirements

Add the following dependencies. 

- Python >= 3.12 : https://www.python.org/downloads/

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
# or 
python -m pip install pygame moviepy pyinstaller
```

## Prepare assets

The assets can be placed by default into the ```assets/``` directory

The game is calibrated to run video at the framerate of 25 img/sec. You can use the following ffmpeg command to resize video and put framerate to 25.

```bash
ffmpeg -i myvideo.mp4 -s 800x450 -filter:v fps=25 myvideo.resized.mp4
```

For the game, you can adapt and launch the ```assets/resize.sh``` script to batch video adaptations.

## How to use the ```configuration.py``` file

### Clips declaration

TODO

### Scene declaration

TODO

### Choices into 

TODO

## Launch the game 

```
python main.py # use default configuration with assets and cache directories
python main.py --fullscreen # start game in full screen
python main.py --help # start game with debug mode
```

The main program analyse the configuration file to register clip

## Build executable

```bash
pyinstaller main.spec
```




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