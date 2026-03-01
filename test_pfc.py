from pfc import SyntheticPFC

def test_pfc_fatigue():
    print("Initializing Synthetic PFC (CEO of the brain)...")
    pfc = SyntheticPFC(max_energy=100.0)
    
    # 1. Test Working Memory
    print(f"\n[Working Memory Test]")
    pfc.update_working_memory("PREDATOR_LOCATION", (14, 22), current_tick=0)
    print(f"Stored predator location. PFC Energy: {pfc.executive_energy:.1f}")
    
    # Simulate high stress for 5 ticks
    for tick in range(1, 6):
        pfc.tick(current_tick=tick, stress_level=0.8, goal_achieved=False)
        print(f"Tick {tick}: Energy [{pfc.executive_energy:.1f}], Fatigue Level [{pfc.get_fatigue_level():.2f}]")
        if "PREDATOR_LOCATION" in pfc.working_memory:
            conf = pfc.working_memory["PREDATOR_LOCATION"]["confidence"]
            print(f"  -> Memory Confidence: {conf:.2f}")
        else:
            print("  -> Memory lost due to stress decay!")
            break

    # 2. Test Inhibitory Control (Modulation) under fatigue
    print(f"\n[Top-Down Modulation Test]")
    fear_impulse = "RUN_ERRATICALLY"
    logic_override = "HESITATE_AND_ASSESS"
    
    print(f"Amygdala screams: {fear_impulse}.")
    print(f"PFC attempting to override with Logic: {logic_override}...")
    
    # PFC is tired now, let's see if it can inhibit a massive impulse (strength 10)
    # The cost to inhibit is cost_inhibit (5.0) * impulse_strength (10) = 50.0 energy
    result = pfc.top_down_modulate(fear_impulse, impulse_strength=10.0, logic_override_value=logic_override)
    print(f"Resulting Action: {result} | PFC Energy Remaining: {pfc.executive_energy:.1f}")
    
    if result == fear_impulse:
        print("  -> PFC FAILED! Ego Depletion occurred. Organism reverts to Lizard Brain.")
    else:
        print("  -> PFC SUCCESS! Logic prevailed over impulse.")

if __name__ == "__main__":
    test_pfc_fatigue()
