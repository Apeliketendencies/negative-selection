import random

class EdenOfShadows:
    def __init__(self, width=50, height=50, max_food=100):
        self.width = width
        self.height = height
        self.max_food = max_food
        self.entities = []
        self.food = set()
        
    def add_entity(self, entity, x=None, y=None):
        if x is None or y is None:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
        entity.x = x
        entity.y = y
        self.entities.append(entity)
        
    def spawn_food(self):
        # Replenish food up to max_food
        while len(self.food) < self.max_food:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            self.food.add((x, y))
            
    def get_local_vision(self, x, y, radius=1):
        # Returns a simple list of what's nearby: 1 for food, 0 for empty
        # (For now, we just detect food to keep the Brainstem simple)
        vision = []
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                nx, ny = (x + dx) % self.width, (y + dy) % self.height
                if (nx, ny) in self.food:
                    vision.append(1)
                else:
                    vision.append(0)
        return vision

    def move_entity(self, entity, dx, dy):
        # Toroidal grid (wraps around)
        entity.x = (entity.x + dx) % self.width
        entity.y = (entity.y + dy) % self.height
        
    def check_food_collision(self, entity):
        pos = (entity.x, entity.y)
        if pos in self.food:
            self.food.remove(pos)
            return True
        return False

    def step(self):
        self.spawn_food()
        
        # Entities take action
        for entity in list(self.entities): # Copy list for safe removal
            entity.act(self)
            
            # Check survival
            if entity.calories <= 0:
                self.entities.remove(entity)
                
        # Handle reproduction (after all actions to avoid modifying list during iteration)
        new_entities = []
        for entity in self.entities:
            child = entity.try_reproduce()
            if child:
                # Spawn child near parent
                new_entities.append((child, entity.x, entity.y))
                
        for child, x, y in new_entities:
            self.add_entity(child, x, y)
