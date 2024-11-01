import pygame
from menu import Menu
from configuration import scene_resources
from scene import SceneManager

# Global variables
BLACK=(0,0,0)

class History:
    """Define history of choice"""
    pass

# Initialize Pygame
pygame.init()

# Screen size
screen_size=(1000,500)

# Init Current scene 
scene_manager = SceneManager(scene_resources,"SCENE_1")

# init menu
menu_dimension=(screen_size[0]-50,60)
menu_init_position=((screen_size[0]-menu_dimension[0])/2, screen_size[1])
menu=Menu(menu_init_position, menu_dimension)

# Prepare SCREEN
screen=pygame.display.set_mode(screen_size, 0, 32)
#screen=pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption("Clip/Scene test")

# Run the Pygame loop to keep the window open
running=True
clock=pygame.time.Clock()
while running:
    clock.tick(25)
    
    # check for events
    for event in pygame.event.get():
        # manage quit()
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        if menu.visible:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                scene_manager.set_next_scene("SCENE_1")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                scene_manager.set_next_scene("SCENE_2")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                scene_manager.set_next_scene("SCENE_3")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_v:
                scene_manager.set_next_scene("SCENE_1")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                scene_manager.set_next_scene("SCENE_2")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                scene_manager.set_next_scene("SCENE_3")

    # Update
    scene_manager.update()

    # Get time reference of the scene and current clip
    clip_time, clip_duration = scene_manager.clip_manager.get_time_by_duration()
    scene_time, scene_duration = scene_manager.get_time_by_duration()

    # Detect if the scene start to update menu
    if scene_manager.is_starting is True:
        menu.update_menu_choices_from_scene(scene_manager.current_scene)

    # Show menu or not 
    menu_to_show = False
    if (scene_time > scene_manager.current_scene.menu_start_time and \
        scene_time < scene_manager.current_scene.menu_start_time + scene_manager.current_scene.menu_duration):
        menu.show()
    else:
        menu.hide()
    menu.update()

    # Draw the surface onto the window
    screen.fill(BLACK)
    screen.blit(scene_manager.get_surface(), (0, 0))
    screen.blit(menu.get_surface(), (menu.left, menu.top))

    # debug
    print("------------------------------------------------------------")
    print(f"Scene       : {scene_manager.current_scene.id.ljust(20)} \t {scene_time:.3f} / {scene_duration:.3f}")
    print(f"Clip        : {scene_manager.clip_manager.current_clip.id.ljust(20)} \t {clip_time:.3f} / {clip_duration:.3f}")
    print(f"Choices     : {",".join([choice.description for choice in scene_manager.current_scene.choices])}")
    print(f"Next Scene  : {scene_manager.next_scene.id}")
    print(f"Menu between {scene_manager.current_scene.menu_start_time:.3f} and "+
          f"{scene_manager.current_scene.menu_start_time + scene_manager.current_scene.menu_duration:.3f} " +
          f"-> {"Visible" if menu.visible else "Hidden"}")

    pygame.draw.rect(screen, pygame.Color(255,int(255*scene_time/scene_duration),0), pygame.Rect(0,screen_size[1]-5,screen_size[0]*scene_time/scene_duration,5))
    
    # render
    pygame.display.flip()

# Quit Pygame
pygame.quit()