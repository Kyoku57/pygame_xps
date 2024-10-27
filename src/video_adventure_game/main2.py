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

    # Update
    scene_manager.update()

    # Get time reference of the scene and current clip
    clip_time, clip_duration = scene_manager.clip_manager.get_time_by_duration()
    scene_time, scene_duration = scene_manager.get_time_by_duration()

    # Draw the surface onto the window
    screen.fill(BLACK)
    screen.blit(scene_manager.get_surface(), (0, 0))
    screen.blit(menu.get_surface(), (menu.left, menu.top))

    # debug
    print("-------------------------------")
    print(f"Scene : {scene_manager.current_scene.id}: {scene_time:.3f} / {scene_duration:.3f}")
    print(f"Clip  : {scene_manager.clip_manager.current_clip.id}: {clip_time:.3f} / {clip_duration:.3f}")
    pygame.draw.rect(screen, pygame.Color(255,int(255*scene_time/scene_duration),0), pygame.Rect(0,screen_size[1]-5,screen_size[0]*scene_time/scene_duration,5))
    
    # render
    pygame.display.flip()

# Quit Pygame
pygame.quit()