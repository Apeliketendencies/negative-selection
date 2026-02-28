import random

class Genome:
    def __init__(self, parent_genes=None):
        if parent_genes is None:
            # Random initial genes [Move_N, Move_E, Move_S, Move_W, Stay]
            self.weights = [random.random() for _ in range(5)]
        else:
            self.weights = list(parent_genes)
            self.mutate()
            
    def mutate(self):
        # Small mutation rate
        mutation_chance = 0.1
        mutation_amount = 0.1
        
        for i in range(len(self.weights)):
            if random.random() < mutation_chance:
                # Add or subtract a small amount
                change = random.uniform(-mutation_amount, mutation_amount)
                self.weights[i] = max(0.0, self.weights[i] + change)
                
        # Normalize weights so they sum to 1.0 (probabilities)
        total = sum(self.weights)
        if total > 0:
            self.weights = [w / total for w in self.weights]
        else:
            self.weights = [0.2] * 5
