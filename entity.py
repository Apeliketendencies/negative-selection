import random
import numpy as np
from evolution import BitNetGenome

class LiminalEntity:
    def __init__(self, calories=200, genome=None):
        self.calories = calories
        self.x = 0
        self.y = 0
        
        # Basal metabolic rate
        self.metabolism = 1 
        self.movement_cost = 2 
        
        # BitNet Architecture: 10 inputs (3x3 vision + 1 calorie scalar) -> 16 hidden -> 5 outputs (N,E,S,W,Stay)
        layer_sizes = [10, 16, 5]
        self.genome = BitNetGenome(layer_sizes=layer_sizes, parent_genes=genome)
        
    def act(self, environment):
        """
        The Brainstem decision loop, driven by purely ternary neural network.
        """
        self.calories -= self.metabolism
        
        # Build neural network input state
        vision = environment.get_local_vision(self.x, self.y, radius=1)
        # Normalize calories to act as an internal "hunger" scalar.
        caloric_score = self.calories / 200.0
        
        state = np.array(vision + [caloric_score])
        
        # Forward pass returning Float32 logits
        logits = self.genome.forward(state)
        # Softmax conversion to probability distribution
        e_x = np.exp(logits - np.max(logits))
        probs = e_x / e_x.sum()
        
        actions = ['N', 'E', 'S', 'W', 'Stay']
        action = np.random.choice(actions, p=probs)
        
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
            child = LiminalEntity(calories=200, genome=self.genome.get_genes())
            return child
        return None
