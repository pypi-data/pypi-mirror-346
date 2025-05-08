from typing import Any, Dict, Optional
from datetime import datetime

class Synapse:
    def __init__(self, source: 'Neuron', target: 'Neuron', 
                 weight: float = 1.0, relationship_type: str = "ASSOCIATED"):
        self.source = source
        self.target = target
        self.weight = weight  # Connection strength (0-1)
        self.relationship_type = relationship_type
        self.created_at = datetime.now()
        self.last_activated = self.created_at
        self.activation_count = 0
        self._learning_rate = 0.1  # Rate at which the weight can change

    def activate(self, strength: float = 1.0) -> None:
        """Activate the synapse, potentially strengthening the connection."""
        self.last_activated = datetime.now()
        self.activation_count += 1
        
        # Hebbian learning: strengthen connection based on activation
        self.strengthen(strength * self._learning_rate)

    def strengthen(self, amount: float) -> None:
        """Strengthen the synaptic connection."""
        self.weight = min(1.0, self.weight + amount)

    def weaken(self, amount: float) -> None:
        """Weaken the synaptic connection."""
        self.weight = max(0.0, self.weight - amount)

    def update_weight(self, new_weight: float) -> None:
        """Update the synaptic weight directly."""
        self.weight = max(0.0, min(1.0, new_weight))

    def __str__(self) -> str:
        return (f"Synapse({self.source.id} -> {self.target.id}, "
                f"weight={self.weight:.2f}, type={self.relationship_type})") 