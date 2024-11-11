import pygame
from menu import Menu
from history import History
from scene import SceneManager
from tools import update_splash_text

# Global variables
BLACK = (0,0,0)

# Parse arguments
import argparse
parser = argparse.ArgumentParser(description='PyGame-VideoGame', epilog='Try it and good luck !!!')
parser.add_argument("-f", "--fullscreen", action="store_true", help="fullscreen")
parser.add_argument("-d", "--debug", action="store_true", help="debug mode")
args = vars(parser.parse_args())
full_screen = args["fullscreen"]
debug_mode = args["debug"]

# Parse configuration and check
update_splash_text('Cache creation ...')
from configuration_test import scene_resources, screen_size
scene_resources.check_coherence()
update_splash_text('Cache and verification DONE !')

# Initialize Pygame
pygame.init()
update_splash_text('Game initialized ...')

# Prepare SCREEN
if full_screen is False:
    screen = pygame.display.set_mode(screen_size, 0, 32)
    #screen=pygame.display.set_mode(screen_size, pygame.RESIZABLE) # Forget it :-D
else:
    screen=pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption("Clip/Scene test")
screen_size = (screen.get_rect().width, screen.get_rect().height)

# Init History
history = History()

# Init Current scene 
scene_manager = SceneManager(scene_resources,scene_resources.first_id)

# init menu
menu = Menu(screen_size)

# Run the Pygame loop to keep the window open
running = True
TICK_VALUE = 25  # 25 tick per second // 0.04 secondes per frame
clock = pygame.time.Clock()
update_splash_text('Game run !!!', close=True)
while running:
    clock.tick(TICK_VALUE)

    # check for events ---------------------------------------------------------------------------
    for event in pygame.event.get():
        # manage quit()
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        # Only if menu is visible
        if menu.visible is True:
            # Focus or not ?
            for menu_choice in menu.menu_choices:
                rect = pygame.Rect((menu_choice.position[0]+menu.left, menu_choice.position[1]+menu.top),
                                   (menu_choice.width,menu_choice.height))
                menu_choice.is_focus = rect.collidepoint(pygame.mouse.get_pos())

            # If click on menu, select, block it and choose next scene
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu.is_choice_selected() is False:
                    for menu_choice in menu.menu_choices:
                        if menu_choice.is_focus is True:
                            menu.selected = menu_choice
                            menu.selected.is_selected = True
                            scene_manager.set_next_scene(menu.selected.choice.next_scene)
                            history.add_event(menu.selected.choice)
    # end events --------------------------------------------------------------------------------

    # Get time reference of the scene and current clip
    clip_time, clip_duration = scene_manager.current_clip.get_time_by_duration()
    scene_time, scene_duration = scene_manager.get_time_by_duration()

    # Detect if the scene start in order to update menu and know how many choices available
    if scene_manager.is_starting is True:
        default_scene_choice = None
        menu.update_menu_choices_from_scene(scene_manager.current_scene, history)

    # Update Menu and default first choice
    if (len(menu.menu_choices)>1 and \
        scene_time > scene_manager.current_scene.menu_start_time and \
        scene_time < scene_manager.current_scene.menu_end_time):

        menu.show()
    else:
        # If menu duration is over and not choice done, choose default
        if (default_scene_choice is None and\
            menu.is_choice_selected() is False and\
            scene_time > scene_manager.current_scene.menu_end_time):

            # default choice
            default_scene_choice = scene_manager.current_scene.default_choice
            # find equivalent from menu if exists (it can be an hidden choice)
            for menu_choice in menu.menu_choices:
                if default_scene_choice == menu_choice.choice:
                    selected_menu_choice = menu_choice
                    selected_menu_choice.is_selected = True
            scene_manager.set_next_scene(default_scene_choice.next_scene)
            history.add_event(default_scene_choice)

        menu.hide()
    menu.update()
    menu.update_progress_bar(scene_time-scene_manager.current_scene.menu_start_time, 
                             scene_manager.current_scene.menu_duration)

    # debug scene_manager / clip 
    if debug_mode is True:
        debug_buffer = []
        debug_buffer.append("--------------------------------------------------------------------------------------------------------")
        debug_buffer.append(f"Tick value        : {TICK_VALUE}")
        debug_buffer.append(f"Clip              : {scene_manager.current_clip.id.ljust(20)} {clip_time:.2f} / {clip_duration:.2f}")
        debug_buffer.append(f"Scene             : {scene_manager.current_scene.id.ljust(20)} {scene_time:.2f} / {scene_duration:.2f}")  
        debug_buffer.append(f"Next Scene        : {scene_manager.next_scene.id}")
        debug_buffer.append(f"Choices           : {" | ".join([f"{choice.id}{"(H)" if choice.condition is False else ""}".ljust(20) for choice in scene_manager.current_scene.choices])}")
        debug_buffer.append(f"Menu choice       : {" | ".join([f"{menu_choice.choice.id}".ljust(20) for menu_choice in menu.menu_choices])}")
        debug_buffer.append(f"Menu Flags        : {" | ".join([f"Focus: {"X" if menu_choice.is_focus else "-"}, Selected:{"X" if menu_choice.is_selected else "-"}".ljust(20) for menu_choice in menu.menu_choices])}")
        debug_buffer.append(f"Default choice    : {scene_manager.current_scene.default_choice.id}")
        debug_buffer.append(f"Menu is selected  : {menu.is_choice_selected()}")
        debug_buffer.append(f"Menu              : between {scene_manager.current_scene.menu_start_time:.2f} and "+
            f"{scene_manager.current_scene.menu_start_time + scene_manager.current_scene.menu_duration:.2f} of the scene " +
            f"-> {"Visible" if menu.visible else "Hidden"}")
        debug_buffer.append(f"History (last 5)  : {history.last(5)}")

    # Update scene/clip and if it is the end of the clip
    scene_manager.update_and_return_isfinished()

    # Draw the surface onto the window
    screen.fill(BLACK)
    scene_surface = scene_manager.get_surface(screen_size)
    screen.blit(scene_surface, scene_surface.get_rect(center=(screen_size[0]/2, screen_size[1]/2)))
    screen.blit(menu.get_surface(), (menu.left, menu.top))

    # debug Progress bar
    if debug_mode:
        pygame.draw.rect(screen, pygame.Color(255,255,100), pygame.Rect(0,0,screen_size[0]*scene_time/scene_duration,2))
        print("\n".join(debug_buffer))

    # if the clip was finished define launch next clip (with reset)
    if scene_manager.is_clip_finished is True:
        scene_manager.process_next_clip()

    # render
    pygame.display.flip()

# Quit Pygame
pygame.quit()