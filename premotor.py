import random

class SyntheticPMC:
    def __init__(self):
        # 1. Action Sequence Library (The Macros)
        # Format: "MACRO_NAME": [(tick_offset, body_part, target_vector, force_multiplier)]
        self.action_library = {
            "FREEZE": [(0, "LEGS", (0, 0), 0.0), (0, "TORSO", (0, 0), 0.0)],
            "FLEE_SPRINT": [(0, "LEGS", (0, -1), 1.0), (1, "LEGS", (0, -1), 1.0), (2, "LEGS", (0, -1), 1.0)],
            "COMPLEX_EVADE": [(0, "LEGS", (-1, -1), 0.8), (1, "TORSO", (1, 0), 0.5), (2, "LEGS", (1, -1), 1.0)],
            "PRECISE_GRASP": [(0, "HANDS", (1, 0), 0.4), (1, "HANDS", (0, 1), 0.2)]
        }
        
        # 2. Mirror Neuron state
        self.mirror_prepared_macro = None
        self.empathy_threshold = 2 # How many peers need to do an action before we mirror it

    def prepare_macro(self, macro_name, pfc_cognitive_load, limbic_stress, current_tick, m1_module):
        """
        Translates a Macro request into individual M1 commands, applying Anticipatory Errors
        like Flinching, Clumsiness, and Stereotypy.
        """
        
        # Feature: Heuristic Stereotypy
        # Under extreme fear, complex routines are lost. Revert to hardwired survival reflex.
        if limbic_stress >= 0.9 and macro_name not in ["FREEZE", "FLEE_SPRINT"]:
            # Override PFC's complex request with a dumb panic reflex
            macro_name = "FREEZE"
            
        macro_sequence = self.action_library.get(macro_name, [])
        if not macro_sequence:
            return # Unknown macro
            
        # Feature: Motor Clumsiness (Cognitive Load interference)
        # If the PFC is thinking too hard, the PMC loses precision.
        clumsiness_modifier = 1.0
        if pfc_cognitive_load > 0.8:
            clumsiness_modifier = 0.5 # Force multiplier drops, making actions weak/clumsy
            
        for step in macro_sequence:
            tick_offset, body_part, target_vector, force = step
            
            applied_force = force * clumsiness_modifier
            
            # Feature: Anticipatory Error (The Flinch)
            # High stress causes the PMC to send the signal to the M1 too early.
            actual_tick_to_fire = current_tick + tick_offset
            if limbic_stress > 0.7 and tick_offset > 0:
                if random.random() < (limbic_stress * 0.5):
                    # Flinch! Fire it immediately instead of waiting for the offset
                    actual_tick_to_fire = current_tick
                    
            # Dispatch to Primary Motor Cortex (M1)
            # We pass the instruction to the M1, which handles its own latency and tremor
            m1_module.receive_command(
                current_tick=actual_tick_to_fire, 
                body_part=body_part, 
                target_vector=target_vector, 
                force_multiplier=applied_force, 
                limbic_stress=limbic_stress
            )
            
    def process_mirror_neurons(self, observed_peer_actions):
        """
        Scans nearby entity actions. If enough are doing the same macro, emulate them.
        observed_peer_actions is a list of strings (macro names).
        """
        if not observed_peer_actions:
            self.mirror_prepared_macro = None
            return None
            
        # Count occurrences of actions
        action_counts = {}
        for action in observed_peer_actions:
            action_counts[action] = action_counts.get(action, 0) + 1
            
        # Check if any action exceeds the empathy threshold
        for action, count in action_counts.items():
            if count >= self.empathy_threshold:
                # Mirror Neurons fire! Automatically prepare this action
                self.mirror_prepared_macro = action
                return action
                
        self.mirror_prepared_macro = None
        return None
