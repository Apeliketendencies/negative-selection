import random
from evolution import Genome

class LiminalEntity:
    def __init__(self, calories=200, genome=None):
        self.calories = calories
        self.x = 0
        self.y = 0
        
        # Basal metabolic rate
        self.metabolism = 1 
        self.movement_cost = 2 
        
        self.genome = Genome(parent_genes=genome)
        
    def act(self, environment):
        """
        The Brainstem decision loop.
        """
        self.calories -= self.metabolism
        
        # Very simple heuristic action based on genes for MVP
        # Genome weights: [N, E, S, W, Stay]
        action = random.choices(
            ['N', 'E', 'S', 'W', 'Stay'], 
            weights=self.genome.weights, 
            k=1
        )[0]
        
        if action != 'Stay':
            self.calories -= self.movement_cost
            dx, dy = 0, 0
            if action == 'N': dy = -1
            elif action == 'S': dy = 1
            elif action == 'E': dx = 1
            elif action == 'W': dx = -1
            
            environment.move_entity(self, dx, dy)
            
        # Check if we landed on food
        if environment.check_food_collision(self):
            self.calories += 100 # Food value
            
    def try_reproduce(self):
        # Asexual splitting if energy is high enough
        if self.calories > 200:
            self.calories -= 100 # Cost of splitting
            child = LiminalEntity(calories=200, genome=self.genome.weights)
            return child
        return None
