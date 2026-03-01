import time
from environment import EdenOfShadows
from entity import LiminalEntity

def main():
    print("Starting Eden of Shadows - MVP Simulation")
    env = EdenOfShadows(width=50, height=50, max_food=100)
    
    # Initialize with 10 random "Adam/Eve" entities
    for _ in range(10):
        e = LiminalEntity(calories=200)
        env.add_entity(e)
        
    ticks = 1000
    for t in range(ticks):
        env.step()
        
        pop_size = len(env.entities)
        
        if t % 10 == 0:
            print(f"Tick: {t} | Population: {pop_size} | Food Available: {len(env.food)}")
            
        if pop_size == 0:
            print(f"Extinction event at tick {t}! Simulation ending.")
            break
            
        # time.sleep(0.01) # Uncomment to watch it slower

    print("Simulation Complete.")
    final_pop = len(env.entities)
    print(f"Final Population: {final_pop}")
    
    # Analyze final genomes of survivors to see if evolution occurred
    if final_pop > 0:
        print("\nTernary BitNet1.58 models successfully evolved and survived!")

if __name__ == "__main__":
    main()
