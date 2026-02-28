import pygame
import sys
from environment import EdenOfShadows
from entity import LiminalEntity

def main():
    width, height = 50, 50
    cell_size = 10
    
    pygame.init()
    screen = pygame.display.set_mode((width * cell_size, height * cell_size))
    pygame.display.set_caption("Eden of Shadows - Brainstem MVP")
    clock = pygame.time.Clock()

    env = EdenOfShadows(width=width, height=height, max_food=150)
    for _ in range(50):
        env.add_entity(LiminalEntity(calories=200))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        env.step()

        screen.fill((20, 20, 20)) # Dark background

        # Draw food (Green)
        for fx, fy in env.food:
            pygame.draw.rect(screen, (0, 255, 0), (fx * cell_size, fy * cell_size, cell_size, cell_size))

        # Draw entities (White, fading to Red as they starve)
        for entity in env.entities:
            health_ratio = min(1.0, entity.calories / 200.0)
            color = (int(255 * (1 - health_ratio)), int(255 * health_ratio), 0)
            if entity.calories > 300:
                color = (0, 255, 255) # Cyan if ready to reproduce
            pygame.draw.rect(screen, color, (entity.x * cell_size, entity.y * cell_size, cell_size, cell_size))

        pygame.display.flip()
        
        if len(env.entities) == 0:
            print("Extinction.")
            running = False
            
        clock.tick(30) # 30 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
