import random

class SyntheticPFC:
    def __init__(self, max_energy=100.0):
        # 1. Executive Energy (The fatigue budget)
        self.max_energy = max_energy
        self.executive_energy = max_energy
        
        # 2. Working Memory
        # Format: { 'memory_key': {'data': any, 'confidence': 1.0, 'timestamp': int} }
        self.working_memory = {}
        
        # 3. Rule Switching & Stagnation
        self.stagnation_counter = 0
        self.stagnation_threshold = 50 # Ticks before triggering a heuristic search
        self.current_rule = "FORAGE"
        
        # Costs for cognitive functions (Metabolic Cost of Logic)
        self.cost_inhibit = 5.0
        self.cost_memory_retain = 0.5
        self.cost_rule_switch = 15.0

    def get_fatigue_level(self):
        """Returns 0.0 (fresh) to 1.0 (completely depleted/Lizard Brain)"""
        return 1.0 - (max(0, self.executive_energy) / self.max_energy)

    def is_depleted(self):
        """Has Ego Depletion occurred? If True, PFC logic fails."""
        return self.executive_energy <= 0

    def top_down_modulate(self, incoming_impulse, impulse_strength, logic_override_value):
        """
        The Filter: Decides whether to allow a Limbic impulse (e.g. FEAR) or override it with Logic.
        """
        if self.is_depleted():
            # PFC has failed. Limbic system (impulse) takes over.
            return incoming_impulse

        # It costs energy to inhibit a strong impulse
        inhibition_effort = self.cost_inhibit * impulse_strength

        if self.executive_energy >= inhibition_effort:
            # PFC successfully suppresses the impulse and enforces logic
            self.executive_energy -= inhibition_effort
            return logic_override_value
        else:
            # PFC tries but doesn't have the energy. Impulse wins, energy is still burned.
            self.executive_energy = 0
            return incoming_impulse

    def update_working_memory(self, key, data, current_tick):
        """Add or refresh data in the online buffer."""
        # Only add to memory if we have the energy to do so
        if not self.is_depleted():
            self.working_memory[key] = {
                'data': data,
                'confidence': 1.0,
                'timestamp': current_tick
            }
            self.executive_energy -= 1.0 # Cost of encoding new memory

    def process_memory_decay(self, stress_level):
        """
        Working memory decays every tick. 
        High stress (Limbic arousal) or high fatigue makes memory decay faster (Tunnel Vision).
        """
        fatigue = self.get_fatigue_level()
        # Decay modifier increases if stressed or tired
        decay_rate = 0.05 + (stress_level * 0.1) + (fatigue * 0.1)
        
        keys_to_remove = []
        for key, mem in self.working_memory.items():
            mem['confidence'] -= decay_rate
            self.executive_energy -= self.cost_memory_retain # Holding memory costs energy

            if mem['confidence'] <= 0:
                keys_to_remove.append(key)
                
        for key in keys_to_remove:
            del self.working_memory[key]

    def check_rule_switch(self, goal_achieved):
        """Monitors the Reward-to-Effort ratio and switches strategies if stagnant."""
        if self.is_depleted():
            self.current_rule = "IMPULSE_DRIVEN"
            return self.current_rule

        if goal_achieved:
            self.stagnation_counter = 0
        else:
            self.stagnation_counter += 1

        if self.stagnation_counter >= self.stagnation_threshold:
            if self.executive_energy >= self.cost_rule_switch:
                # Spend massive energy to break out of a loop and try a new heuristic
                self.executive_energy -= self.cost_rule_switch
                self.stagnation_counter = 0
                
                # Prototype rules: FORAGE, HIDE, EXPLORE
                possible_rules = ["FORAGE", "HIDE", "EXPLORE"]
                possible_rules.remove(self.current_rule) if self.current_rule in possible_rules else None
                self.current_rule = random.choice(possible_rules)
            else:
                # Too tired to think of a new plan. Stuck in a rut.
                self.current_rule = "STAGNANT"
                
        return self.current_rule

    def rest(self, recovery_amount):
        """Recovers Executive Energy when not under load."""
        self.executive_energy = min(self.max_energy, self.executive_energy + recovery_amount)

    def tick(self, current_tick, stress_level, goal_achieved):
        """The main update loop for the PFC."""
        self.process_memory_decay(stress_level)
        self.check_rule_switch(goal_achieved)
        
        # If deeply depleted, force a "mental breakdown" state
        if self.is_depleted():
            self.working_memory.clear() # Drop all working memory
