import numpy as np

def activation_quant_8bit(x):
    """
    Quantizes activations to 8-bit (-128 to 127), fitting the BitNet paradigm
    where weights are ternary and activations are 8-bit.
    """
    max_val = max(np.max(np.abs(x)), 1e-5)
    scale = 127.0 / max_val
    return np.clip(np.round(x * scale), -128, 127).astype(np.int8)

class BitNetLayer:
    def __init__(self, in_features, out_features, weights=None):
        if weights is None:
            # Strict 1.58-bit ternary initialization (-1, 0, 1)
            self.weights = np.random.choice([-1, 0, 1], size=(in_features, out_features)).astype(np.int8)
        else:
            self.weights = weights.copy()
            
    def forward(self, x_quant):
        # Native dot-product: multiplying int8 activations by ternary int8 weights
        # Because weights are just -1, 0, 1, this represents pure additions/subtractions on hardware
        return np.dot(x_quant, self.weights).astype(np.float32)

class BitNetGenome:
    def __init__(self, layer_sizes, parent_genes=None):
        self.layer_sizes = layer_sizes
        self.layers = []
        
        if parent_genes is None:
            for i in range(len(layer_sizes) - 1):
                self.layers.append(BitNetLayer(layer_sizes[i], layer_sizes[i+1]))
        else:
            # Inherit and reconstruct layers from parent's ternary matrices
            for w in parent_genes:
                self.layers.append(BitNetLayer(w.shape[0], w.shape[1], w))
            self.mutate()
            
    def mutate(self):
        # Mutate ternary weights with a small probability
        mutation_chance = 0.05
        
        for layer in self.layers:
            mask = np.random.rand(*layer.weights.shape) < mutation_chance
            if np.any(mask):
                # Flipping bits to randomly sample from -1, 0, 1
                new_weights = np.random.choice([-1, 0, 1], size=layer.weights.shape).astype(np.int8)
                layer.weights = np.where(mask, new_weights, layer.weights)
                
    def get_genes(self):
        return [layer.weights for layer in self.layers]
        
    def forward(self, x):
        # Pass through the network
        curr = x.astype(np.float32)
        for i, layer in enumerate(self.layers):
            # Quantize activations to 8-bit integers before linear projection
            curr_quant = activation_quant_8bit(curr)
            curr = layer.forward(curr_quant)
            
            # Apply non-linear ReLU if it's a hidden layer
            if i < len(self.layers) - 1:
                curr = np.maximum(0, curr)
                
        # Returns output logits (float32, to drive final probabilities)
        return curr
