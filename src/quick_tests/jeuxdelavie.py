import pygame
import random
import sys

# Initialisation de Pygame
pygame.init()

# Constantes
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
MENU_WIDTH = 300
GRID_WIDTH = WINDOW_WIDTH - MENU_WIDTH
GRID_HEIGHT = WINDOW_HEIGHT

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 200)
RED = (255, 0, 0)

class GameOfLife:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Jeu de la Vie - Conway")
        self.clock = pygame.time.Clock()
        
        # Paramètres configurables
        self.grid_size = 20
        self.fill_percentage = 30  # Pourcentage de remplissage
        self.iterations_per_second = 10  # Vitesse de simulation
        
        # État du jeu
        self.running = True
        self.simulating = False
        self.grid = None
        self.iteration_count = 0
        
        # Interface
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        
        # Boutons
        self.buttons = {}
        self.setup_ui()
        
        # Initialiser la grille
        self.init_grid()
    
    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        button_width = 200
        button_height = 40
        x_offset = 50
        
        # Bouton pour remplir aléatoirement
        self.buttons['random'] = {
            'rect': pygame.Rect(x_offset, 250, button_width, button_height),
            'text': 'Remplir Aléatoirement',
            'color': GREEN,
            'hover_color': DARK_GREEN
        }
        
        # Bouton pour lancer la simulation
        self.buttons['simulate'] = {
            'rect': pygame.Rect(x_offset, 300, button_width, button_height),
            'text': 'Lancer Simulation',
            'color': BLUE,
            'hover_color': DARK_BLUE
        }
        
        # Bouton pour effacer
        self.buttons['clear'] = {
            'rect': pygame.Rect(x_offset, 350, button_width, button_height),
            'text': 'Effacer Grille',
            'color': RED,
            'hover_color': (200, 0, 0)
        }
    
    def init_grid(self):
        """Initialise la grille vide"""
        cols = GRID_WIDTH // self.grid_size
        rows = GRID_HEIGHT // self.grid_size
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.rows = rows
        self.cols = cols
    
    def fill_random(self):
        """Remplit la grille aléatoirement selon le pourcentage défini"""
        for i in range(self.rows):
            for j in range(self.cols):
                if random.randint(1, 100) <= self.fill_percentage:
                    self.grid[i][j] = 1
                else:
                    self.grid[i][j] = 0
    
    def clear_grid(self):
        """Efface la grille"""
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j] = 0
        self.iteration_count = 0
    
    def count_neighbors(self, row, col):
        """Compte les voisins vivants d'une cellule"""
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                new_row = (row + i) % self.rows
                new_col = (col + j) % self.cols
                count += self.grid[new_row][new_col]
        return count
    
    def update_grid(self):
        """Met à jour la grille selon les règles du jeu de la vie"""
        new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        
        for i in range(self.rows):
            for j in range(self.cols):
                neighbors = self.count_neighbors(i, j)
                
                if self.grid[i][j] == 1:  # Cellule vivante
                    if neighbors < 2:
                        new_grid[i][j] = 0  # Meurt par sous-population
                    elif neighbors == 2 or neighbors == 3:
                        new_grid[i][j] = 1  # Survit
                    else:
                        new_grid[i][j] = 0  # Meurt par surpopulation
                else:  # Cellule morte
                    if neighbors == 3:
                        new_grid[i][j] = 1  # Naît
        
        self.grid = new_grid
        self.iteration_count += 1
    
    def draw_grid(self):
        """Dessine la grille"""
        grid_surface = pygame.Surface((GRID_WIDTH, GRID_HEIGHT))
        grid_surface.fill(WHITE)
        
        for i in range(self.rows):
            for j in range(self.cols):
                x = j * self.grid_size
                y = i * self.grid_size
                
                if self.grid[i][j] == 1:
                    pygame.draw.rect(grid_surface, BLACK, 
                                   (x, y, self.grid_size, self.grid_size))
                
                # Grille
                pygame.draw.rect(grid_surface, GRAY, 
                               (x, y, self.grid_size, self.grid_size), 1)
        
        self.screen.blit(grid_surface, (MENU_WIDTH, 0))
    
    def draw_menu(self):
        """Dessine le menu à gauche"""
        menu_surface = pygame.Surface((MENU_WIDTH, GRID_HEIGHT))
        menu_surface.fill(LIGHT_GRAY)
        
        # Titre
        title = self.font.render("Jeu de la Vie", True, BLACK)
        menu_surface.blit(title, (20, 20))
        
        # Paramètres
        y_offset = 60
        
        # Taille de la grille
        size_text = self.small_font.render(f"Taille cellule: {self.grid_size}", True, BLACK)
        menu_surface.blit(size_text, (20, y_offset))
        
        # Contrôles pour la taille
        size_minus = pygame.Rect(20, y_offset + 25, 30, 25)
        size_plus = pygame.Rect(60, y_offset + 25, 30, 25)
        
        pygame.draw.rect(menu_surface, WHITE, size_minus)
        pygame.draw.rect(menu_surface, BLACK, size_minus, 2)
        pygame.draw.rect(menu_surface, WHITE, size_plus)
        pygame.draw.rect(menu_surface, BLACK, size_plus, 2)
        
        minus_text = self.small_font.render("-", True, BLACK)
        plus_text = self.small_font.render("+", True, BLACK)
        menu_surface.blit(minus_text, (30, y_offset + 30))
        menu_surface.blit(plus_text, (70, y_offset + 30))
        
        # Stocker les rectangles pour les événements (coordonnées absolues)
        self.size_minus_rect = pygame.Rect(20, y_offset + 25, 30, 25)
        self.size_plus_rect = pygame.Rect(60, y_offset + 25, 30, 25)
        
        # Nombre d'itérations
        y_offset += 70
        
        # Pourcentage de remplissage
        fill_text = self.small_font.render(f"Remplissage: {self.fill_percentage}%", True, BLACK)
        menu_surface.blit(fill_text, (20, y_offset))
        
        # Contrôles pour le pourcentage
        fill_minus = pygame.Rect(20, y_offset + 25, 30, 25)
        fill_plus = pygame.Rect(60, y_offset + 25, 30, 25)
        
        pygame.draw.rect(menu_surface, WHITE, fill_minus)
        pygame.draw.rect(menu_surface, BLACK, fill_minus, 2)
        pygame.draw.rect(menu_surface, WHITE, fill_plus)
        pygame.draw.rect(menu_surface, BLACK, fill_plus, 2)
        
        menu_surface.blit(minus_text, (30, y_offset + 30))
        menu_surface.blit(plus_text, (70, y_offset + 30))
        
        # Stocker les rectangles pour les événements (coordonnées absolues)
        self.fill_minus_rect = pygame.Rect(20, y_offset + 25, 30, 25)
        self.fill_plus_rect = pygame.Rect(60, y_offset + 25, 30, 25)
        
        # Vitesse de simulation
        y_offset += 70
        speed_text = self.small_font.render(f"Vitesse: {self.iterations_per_second} it/s", True, BLACK)
        menu_surface.blit(speed_text, (20, y_offset))
        
        # Contrôles pour la vitesse
        speed_minus = pygame.Rect(20, y_offset + 25, 30, 25)
        speed_plus = pygame.Rect(60, y_offset + 25, 30, 25)
        
        pygame.draw.rect(menu_surface, WHITE, speed_minus)
        pygame.draw.rect(menu_surface, BLACK, speed_minus, 2)
        pygame.draw.rect(menu_surface, WHITE, speed_plus)
        pygame.draw.rect(menu_surface, BLACK, speed_plus, 2)
        
        menu_surface.blit(minus_text, (30, y_offset + 30))
        menu_surface.blit(plus_text, (70, y_offset + 30))
        
        # Stocker les rectangles pour les événements (coordonnées absolues)
        self.speed_minus_rect = pygame.Rect(20, y_offset + 25, 30, 25)
        self.speed_plus_rect = pygame.Rect(60, y_offset + 25, 30, 25)
        
        # Boutons
        mouse_pos = pygame.mouse.get_pos()
        
        for button_name, button in self.buttons.items():
            # Ajuster la position pour le menu
            button_rect = button['rect'].copy()
            
            # Vérifier si la souris survole le bouton
            if button_rect.collidepoint(mouse_pos):
                color = button['hover_color']
            else:
                color = button['color']
            
            pygame.draw.rect(menu_surface, color, button['rect'])
            pygame.draw.rect(menu_surface, BLACK, button['rect'], 2)
            
            # Texte du bouton
            text = self.small_font.render(button['text'], True, BLACK)
            text_rect = text.get_rect(center=button['rect'].center)
            menu_surface.blit(text, text_rect)
        
        # Informations sur l'état
        y_offset = 400
        if self.simulating:
            status_text = self.small_font.render("Simulation en cours...", True, BLACK)
        else:
            status_text = self.small_font.render("Simulation arrêtée", True, BLACK)
        menu_surface.blit(status_text, (20, y_offset))
        
        # Compteur d'itérations
        iter_count_text = self.small_font.render(f"Itération: {self.iteration_count}", True, BLACK)
        menu_surface.blit(iter_count_text, (20, y_offset + 25))
        
        # Instructions
        y_offset += 70
        instructions = [
            "Instructions:",
            "- Cliquer sur la grille pour",
            "  activer/désactiver une cellule",
            "- Maintenir 'Lancer Simulation'",
            "  pour démarrer",
            "- Relâcher pour arrêter",
            "- Ajuster le % de remplissage",
            "  puis cliquer 'Remplir'",
            "- Régler la vitesse en it/s"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, BLACK)
            menu_surface.blit(text, (20, y_offset + i * 20))
        
        self.screen.blit(menu_surface, (0, 0))
    
    def handle_click(self, pos):
        """Gère les clics de souris"""
        x, y = pos
        
        # Clic sur les boutons principaux
        for button_name, button in self.buttons.items():
            if button['rect'].collidepoint(pos):
                if button_name == 'random':
                    self.fill_random()
                elif button_name == 'clear':
                    self.clear_grid()
                    self.simulating = False
                return
        
        # Contrôles de taille (vérifier si on est dans le menu)
        if x < MENU_WIDTH:
            if hasattr(self, 'size_minus_rect') and self.size_minus_rect.collidepoint(pos):
                if self.grid_size > 5:
                    self.grid_size -= 5
                    self.init_grid()
            elif hasattr(self, 'size_plus_rect') and self.size_plus_rect.collidepoint(pos):
                if self.grid_size < 50:
                    self.grid_size += 5
                    self.init_grid()
            
            # Contrôles de pourcentage de remplissage
            elif hasattr(self, 'fill_minus_rect') and self.fill_minus_rect.collidepoint(pos):
                if self.fill_percentage > 5:
                    self.fill_percentage -= 5
            elif hasattr(self, 'fill_plus_rect') and self.fill_plus_rect.collidepoint(pos):
                if self.fill_percentage < 95:
                    self.fill_percentage += 5
            
            # Contrôles de vitesse
            elif hasattr(self, 'speed_minus_rect') and self.speed_minus_rect.collidepoint(pos):
                if self.iterations_per_second > 1:
                    self.iterations_per_second -= 1
            elif hasattr(self, 'speed_plus_rect') and self.speed_plus_rect.collidepoint(pos):
                if self.iterations_per_second < 60:
                    self.iterations_per_second += 1
        
        # Clic sur la grille
        elif x > MENU_WIDTH:
            grid_x = (x - MENU_WIDTH) // self.grid_size
            grid_y = y // self.grid_size
            
            if 0 <= grid_x < self.cols and 0 <= grid_y < self.rows:
                self.grid[grid_y][grid_x] = 1 - self.grid[grid_y][grid_x]
    
    def run(self):
        """Boucle principale du jeu"""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        self.handle_click(event.pos)
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.simulating = not self.simulating
                    elif event.key == pygame.K_r:
                        self.fill_random()
                    elif event.key == pygame.K_c:
                        self.clear_grid()
            
            # Gestion du bouton de simulation (maintenir enfoncé)
            mouse_pressed = pygame.mouse.get_pressed()[0]
            mouse_pos = pygame.mouse.get_pos()
            
            if (mouse_pressed and 
                self.buttons['simulate']['rect'].collidepoint(mouse_pos)):
                self.simulating = True
            elif not mouse_pressed:
                self.simulating = False
            
            # Mise à jour de la simulation
            if self.simulating:
                self.update_grid()
            
            # Dessin
            self.screen.fill(WHITE)
            self.draw_grid()
            self.draw_menu()
            
            pygame.display.flip()
            self.clock.tick(self.iterations_per_second)  # Utilise la vitesse configurée
        
        pygame.quit()
        sys.exit()

# Lancement du jeu
if __name__ == "__main__":
    game = GameOfLife()
    game.run()