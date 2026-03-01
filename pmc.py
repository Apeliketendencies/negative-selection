import random
import math

class SyntheticM1:
    def __init__(self):
        # 1. The Motor Homunculus
        # Maps body parts to "Precision Space" (Higher = less susceptible to tremor, more expensive)
        self.homunculus = {
            "FACE":  0.9,
            "HANDS": 0.8,
            "LEGS":  0.3,
            "TORSO": 0.1
        }
        
        # 2. Action Queue (The Latency Gap)
        # Stores commands as: {'vector': (dx, dy), 'part': string, 'force': float, 'execute_tick': int}
        self.spinal_cord_queue = []
        self.base_latency_ticks = 2 # Minimum ticks between request and execution
        
        # 3. Proprioception Feedback
        self.last_expected_position = None
        self.tripped = False
        self.trip_recovery_ticks = 0

    def receive_command(self, current_tick, body_part, target_vector, force_multiplier, limbic_stress):
        """
        Translates an abstract goal into a physical vector command, applies noise, and queues it.
        target_vector: A tuple (dx, dy) representing the ideal mathematical movement.
        force_multiplier: 0.0 to 1.0 (Higher = more energy burned, larger movement).
        """
        
        # Step 1: Inhibit or apply Limbic Hijack (The Tremor)
        precision = self.homunculus.get(body_part, 0.5)
        
        # Tremor formula: High stress + Low precision = Massive noise. 
        # Even high precision parts shake if stress is at 1.0.
        tremor_magnitude = (limbic_stress * 1.5) * (1.0 - precision)
        
        # Apply rotational noise to the vector (The Tremor)
        noisy_vector = self._apply_rotational_noise(target_vector, tremor_magnitude)
        
        # Apply magnitude force (Rate Coding)
        final_dx = noisy_vector[0] * force_multiplier
        final_dy = noisy_vector[1] * force_multiplier
        
        # Normalize to grid steps for the MVP environment (rounding to nearest int)
        # In a physics sim this would stay as floats.
        step_dx = round(final_dx)
        step_dy = round(final_dy)
        if step_dx == 0 and step_dy == 0 and force_multiplier > 0:
            # Force at least a tiny movement if force was applied
            step_dx = 1 if final_dx > 0 else (-1 if final_dx < 0 else 0)
            step_dy = 1 if final_dy > 0 else (-1 if final_dy < 0 else 0)

        # Step 2: Queue for Execution (The Latency Gap)
        # High stress can slightly reduce latency (panic reflex) but costs accuracy.
        actual_latency = max(1, self.base_latency_ticks - int(limbic_stress * 2))
        
        command = {
            'vector': (step_dx, step_dy),
            'part': body_part,
            'force': force_multiplier,
            'execute_tick': current_tick + actual_latency
        }
        
        self.spinal_cord_queue.append(command)
        
    def _apply_rotational_noise(self, vector, magnitude):
        """Rotates the vector by a random angle based on tremor magnitude."""
        if magnitude <= 0: return vector
        
        dx, dy = vector
        
        # Calculate current angle
        angle = math.atan2(dy, dx)
        
        # magnitude of 1.0 means up to +/- 45 degrees of error (pi/4)
        noise_angle = random.uniform(-magnitude * (math.pi/4), magnitude * (math.pi/4))
        new_angle = angle + noise_angle
        
        # keep the original length
        length = math.sqrt(dx**2 + dy**2)
        if length == 0: return vector
        
        return (math.cos(new_angle) * length, math.sin(new_angle) * length)

    def execute_tick(self, current_tick, actual_position):
        """
        The Alpha-Motor Relay. Pops ripe commands from the queue and returns the physical Delta.
        Also checks proprioception (did we move where we expected?)
        """
        # Recovering from a trip
        if self.tripped:
            self.trip_recovery_ticks -= 1
            if self.trip_recovery_ticks <= 0:
                self.tripped = False
            return (0, 0), 0.0 # Cannot move while tripped

        # Proprioceptive Check
        # If the environment (Plague) prevented expected movement last tick
        if self.last_expected_position is not None:
            if self.last_expected_position != actual_position:
                # We expected to be at X, but we are at Y. 
                # This induces a "Trip" or confusion state.
                self.tripped = True
                self.trip_recovery_ticks = 2 # Lose 2 ticks of movement
                self.last_expected_position = actual_position
                self.spinal_cord_queue.clear() # Drop any pending commands (flailing)
                return (0, 0), 0.0

        # Execute ripe commands
        execution_vector = (0, 0)
        total_force_used = 0.0
        
        commands_to_keep = []
        for cmd in self.spinal_cord_queue:
            if current_tick >= cmd['execute_tick']:
                # Combine vectors if multiple commands fire at once
                execution_vector = (execution_vector[0] + cmd['vector'][0], execution_vector[1] + cmd['vector'][1])
                total_force_used += cmd['force']
            else:
                commands_to_keep.append(cmd)
                
        self.spinal_cord_queue = commands_to_keep
        
        # Set expectation for next tick's proprioceptive check
        if execution_vector != (0, 0):
            # In a real grid, the environment handles boundaries, so sM1 just expects delta + current
            self.last_expected_position = (actual_position[0] + execution_vector[0], 
                                           actual_position[1] + execution_vector[1])
        else:
            self.last_expected_position = actual_position

        return execution_vector, total_force_used
