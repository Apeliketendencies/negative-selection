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
        print("\nSurvivor Gene Averages [N, E, S, W, Stay]:")
        avg_genes = [0] * 5
        for e in env.entities:
            for i, w in enumerate(e.genome.weights):
                avg_genes[i] += w
                
        avg_genes = [w / final_pop for w in avg_genes]
        for i, direction in enumerate(['N', 'E', 'S', 'W', 'Stay']):
            print(f"{direction}: {avg_genes[i]:.2f}")

if __name__ == "__main__":
    main()
