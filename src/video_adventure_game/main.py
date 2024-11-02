import pygame
from menu import Menu
from configuration_test import scene_resources, screen_size
from scene import SceneManager

# Global variables
BLACK=(0,0,0)

class History:
    """Define history of choice"""
    pass

# Initialize Pygame
pygame.init()

# Prepare SCREEN
screen=pygame.display.set_mode(screen_size, 0, 32)
#screen=pygame.display.set_mode(screen_size, pygame.RESIZABLE)
#screen=pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen_size=(screen.get_rect().width, screen.get_rect().height)
pygame.display.set_caption("Clip/Scene test")

# Init Current scene 
scene_manager = SceneManager(scene_resources,scene_resources.first_id)

# init menu
menu_dimension=(screen_size[0]-100,60)
menu_init_position=((screen_size[0]-menu_dimension[0])/2, screen_size[1])
menu=Menu(menu_init_position, menu_dimension)

# Run the Pygame loop to keep the window open
running=True
clock=pygame.time.Clock()
while running:
    # 25 tick per second
    clock.tick(25)
    
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
                if menu.selected is None:
                    for menu_choice in menu.menu_choices:
                        if menu_choice.is_focus is True:
                            menu.selected = menu_choice
                            menu.selected.is_selected = True
                            scene_manager.set_next_scene(menu.selected.choice.next_scene)
    # end events --------------------------------------------------------------------------------

    # Update Scene / Clips
    scene_manager.update()

    # Get time reference of the scene and current clip
    clip_time, clip_duration = scene_manager.clip_manager.get_time_by_duration()
    scene_time, scene_duration = scene_manager.get_time_by_duration()

    # Detect if the scene start to update menu and know how many choices
    if scene_manager.is_starting is True:
        menu.update_menu_choices_from_scene(scene_manager.current_scene)
        if len(menu.menu_choices)==1:
            only_one_choice = True
            scene_manager.set_next_scene(menu.menu_choices[0].choice.next_scene)
        else:
            only_one_choice = False

    # Update Menu and default first choice
    if (only_one_choice is False and \
        scene_time > scene_manager.current_scene.menu_start_time and \
        scene_time < scene_manager.current_scene.menu_start_time + scene_manager.current_scene.menu_duration):
        menu.show()
    else:
        # If menu duration is over and not choice done, choose first
        if (menu.selected is None and\
            scene_time > scene_manager.current_scene.menu_start_time + scene_manager.current_scene.menu_duration):
            menu.selected = menu.menu_choices[0]
            menu.selected.is_selected = True
            scene_manager.set_next_scene(menu.selected.choice.next_scene)
        menu.hide()
    menu.update()
    menu.update_progress_bar(scene_time-scene_manager.current_scene.menu_start_time, 
                             scene_manager.current_scene.menu_duration)

    # Draw the surface onto the window
    screen.fill(BLACK)
    scene_manager_rect = scene_manager.get_surface().get_rect(center=(screen_size[0]/2, screen_size[1]/2))
    screen.blit(scene_manager.get_surface(), scene_manager_rect)
    screen.blit(menu.get_surface(), (menu.left, menu.top))

    # debug elements
    print("------------------------------------------------------------")
    print(f"Scene       : {scene_manager.current_scene.id.ljust(20)} \t {scene_time:.2f} / {scene_duration:.2f}")
    print(f"Clip        : {scene_manager.clip_manager.current_clip.id.ljust(20)} \t {clip_time:.2f} / {clip_duration:.2f}")
    print(f"Choices     : {", ".join([f"{choice.id}" for choice in scene_manager.current_scene.choices])} - Only one : {only_one_choice}")
    print(f"Menu Choices: {" | ".join([f"{menu_choice.choice.description} (Focus:{menu_choice.is_focus},Selected:{menu_choice.is_selected})" for menu_choice in menu.menu_choices])}")
    print(f"Next Scene  : {scene_manager.next_scene.id}")
    print(f"Menu between {scene_manager.current_scene.menu_start_time:.2f} and "+
          f"{scene_manager.current_scene.menu_start_time + scene_manager.current_scene.menu_duration:.2f} " +
          f"-> {"Visible" if menu.visible else "Hidden"}")
    # debug Progress bar
    pygame.draw.rect(screen, pygame.Color(255,int(255*scene_time/scene_duration),0), pygame.Rect(0,screen_size[1]-3,screen_size[0]*scene_time/scene_duration,3))

    # render
    pygame.display.flip()

# Quit Pygame
pygame.quit()