from premotor import SyntheticPMC
from pmc import SyntheticM1

def test_spmc_tactics():
    print("Initializing Synthetic Premotor Cortex (sPMC) & Primary Motor Cortex (sM1)...\n")
    spmc = SyntheticPMC()
    
    # We mock the M1's receive_command to just print what it received instead of executing it
    class MockM1:
        def receive_command(self, current_tick, body_part, target_vector, force_multiplier, limbic_stress):
            print(f"  -> M1 Received Command @ Tick {current_tick}: {body_part} moves {target_vector} at {force_multiplier}x force. [Stress: {limbic_stress}]")

    mock_m1 = MockM1()

    # 1. Test Heuristic Stereotypy (Fear Overrides Creativity)
    print("--- TEST 1: Heuristic Stereotypy (The Panic Matrix) ---")
    print("Goal: Execute 'COMPLEX_EVADE' under 100% Limbic Stress.")
    spmc.prepare_macro("COMPLEX_EVADE", pfc_cognitive_load=0.0, limbic_stress=1.0, current_tick=0, m1_module=mock_m1)
    print("  * Notice that instead of the complex evade sequence, the sPMC locked up and fired the FREEZE macro!\n")

    # 2. Test Motor Clumsiness (Cognitive Load)
    print("--- TEST 2: Motor Clumsiness (Distracted Mind) ---")
    print("Goal: Execute 'PRECISE_GRASP' while the PFC is solving a difficult puzzle (Load > 0.8).")
    spmc.prepare_macro("PRECISE_GRASP", pfc_cognitive_load=0.9, limbic_stress=0.0, current_tick=10, m1_module=mock_m1)
    print("  * Notice the force_multiplier is severely reduced (clumsy/weak grasp) because the PFC is using all the energy.\n")

    # 3. Test Anticipatory Error (The Flinch)
    print("--- TEST 3: The Flinch (Jumping the Gun) ---")
    print("Goal: Execute 'FLEE_SPRINT' (a 3-tick sequence [0, 1, 2]) under High Stress (0.8).")
    # Setting seed for reproducible flinch testing
    import random
    random.seed(42) 
    
    spmc.prepare_macro("FLEE_SPRINT", pfc_cognitive_load=0.0, limbic_stress=0.8, current_tick=20, m1_module=mock_m1)
    print("  * Notice that Tick offset 2 was 'Flinched' and fired early because of panic!\n")

    # 4. Test Mirror Neurons (Herd Empathy)
    print("--- TEST 4: Mirror Neurons (Tribal Empathy) ---")
    print("Goal: The entity observes 3 peers executing 'FLEE_SPRINT'.")
    observed_actions = ["FORAGE", "FLEE_SPRINT", "FLEE_SPRINT", "FLEE_SPRINT"]
    
    mirrored_action = spmc.process_mirror_neurons(observed_actions)
    if mirrored_action:
        print(f"  -> Empathy Threshold Reached! sPMC automatically prepared macro: {mirrored_action}")
    else:
        print("  -> Observer remained calm.")

if __name__ == "__main__":
    test_spmc_tactics()
