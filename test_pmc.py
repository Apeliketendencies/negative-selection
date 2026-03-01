from pmc import SyntheticM1

def test_pmc_friction():
    print("Initializing Synthetic Primary Motor Cortex (sM1)...\n")
    sm1 = SyntheticM1()
    
    current_grid_pos = (5, 5)
    
    # 1. Test Clean Movement (Low Stress)
    print("--- TEST 1: The Focused Sprint ---")
    print(f"Goal: Move exact North (0, -1) with Legs.")
    
    sm1.receive_command(current_tick=0, body_part="LEGS", target_vector=(0, -1), force_multiplier=1.0, limbic_stress=0.0)
    print(f"Action Queued. Base Latency = {sm1.base_latency_ticks} ticks.")
    
    for tick in range(1, 4):
        vector, force = sm1.execute_tick(tick, current_grid_pos)
        if vector != (0, 0):
            print(f"Tick {tick}: Signal arrived! Movement vector: {vector}")
            current_grid_pos = (current_grid_pos[0] + vector[0], current_grid_pos[1] + vector[1])
        else:
            print(f"Tick {tick}: Signal traveling down spinal cord...")
            

    # 2. Test Limbic Hijack (Tremor in Hands under stress)
    print("\n--- TEST 2: The Panic Grab ---")
    print(f"Goal: Precise horizontal use of HANDS (1, 0) under 100% Panic.")
    sm1.receive_command(current_tick=4, body_part="HANDS", target_vector=(1, 0), force_multiplier=1.0, limbic_stress=1.0)
    
    for tick in range(5, 7):
        vector, force = sm1.execute_tick(tick, current_grid_pos)
        if vector != (0, 0):
            print(f"Tick {tick}: Tremor Execution! Movement vector changed by noise: {vector}")
            current_grid_pos = (current_grid_pos[0] + vector[0], current_grid_pos[1] + vector[1])
            
            
    # 3. Test Proprioceptive Desync (The Plague causes code-lag in the environment)
    print("\n--- TEST 3: The Virtual Trip (Proprioceptive Failure) ---")
    print("Goal: Move East, but the environment (Plague) freezes the entity.")
    sm1.receive_command(current_tick=8, body_part="LEGS", target_vector=(1, 0), force_multiplier=1.0, limbic_stress=0.0)
    
    # Tick 9: Expected execution tick is reached
    vector, force = sm1.execute_tick(10, current_grid_pos)
    print(f"Tick 10: sM1 fired successfully. Target Vector: {vector}")
    
    # But the environment LAGS and doesn't update actual grid pos!
    print("ENV LAG: Entity remains at previous coordinate...")
    
    # Next tick, M1 realizes the body didn't move!
    vector, force = sm1.execute_tick(11, current_grid_pos) # Feeding it old pos
    if sm1.tripped:
        print(f"Tick 11: sM1 trips! Proprioceptive mismatch detected.")
        print(f"  -> Recovery Ticks Remaining: {sm1.trip_recovery_ticks}")

if __name__ == "__main__":
    test_pmc_friction()
