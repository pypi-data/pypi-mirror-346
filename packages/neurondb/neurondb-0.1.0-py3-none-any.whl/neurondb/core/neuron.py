from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime
import math

class Neuron:
    def __init__(self, data: Dict[str, Any] = None):
        self.id = str(uuid.uuid4())
        self.data = data or {}
        self.connections: List['Synapse'] = []
        self.created_at = datetime.now()
        self.last_activated = self.created_at
        self.activation_count = 0
        self._activation_strength = 0.0  # Current activation level (0-1)
        self._decay_rate = 0.1  # Rate at which activation decreases over time
        self._update_callbacks: List = []

    def activate(self, strength: float = 1.0) -> None:
        """Activate the neuron, increasing its activation strength."""
        self._activation_strength = min(1.0, self._activation_strength + strength)
        self.last_activated = datetime.now()
        self.activation_count += 1
        self.notify_update()

    def decay(self) -> None:
        """Decay the neuron's activation over time."""
        time_diff = (datetime.now() - self.last_activated).total_seconds()
        decay_amount = self._decay_rate * time_diff
        self._activation_strength = max(0.0, self._activation_strength - decay_amount)
        self.notify_update()

    def get_activation_strength(self) -> float:
        """Get the current activation strength of the neuron."""
        self.decay()  # Update decay before returning
        return self._activation_strength

    def add_connection(self, target: 'Neuron', weight: float = 1.0, 
                      relationship_type: str = "ASSOCIATED") -> 'Synapse':
        """Create a connection to another neuron with a specific weight."""
        from .synapse import Synapse  # Import here to avoid circular dependency
        synapse = Synapse(self, target, weight, relationship_type)
        self.connections.append(synapse)
        target.connections.append(synapse)
        return synapse

    def get_connections(self, relationship_type: Optional[str] = None) -> List['Synapse']:
        """Get all connections or filter by relationship type."""
        if relationship_type is None:
            return self.connections
        return [conn for conn in self.connections if conn.relationship_type == relationship_type]

    def update_data(self, new_data: Dict[str, Any]) -> None:
        """Update the neuron's data and refresh the timestamp."""
        self.data.update(new_data)
        self.last_activated = datetime.now()
        self.notify_update()

    def calculate_similarity(self, other: 'Neuron') -> float:
        """Calculate similarity between this neuron and another based on data."""
        if not self.data or not other.data:
            return 0.0

        # Calculate similarity based on common keys and values
        common_keys = set(self.data.keys()) & set(other.data.keys())
        if not common_keys:
            return 0.0

        similarities = []
        for key in common_keys:
            val1 = self.data[key]
            val2 = other.data[key]
            
            if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                # For numeric values, calculate normalized difference
                max_val = max(abs(val1), abs(val2))
                if max_val == 0:
                    similarity = 1.0
                else:
                    similarity = 1.0 - (abs(val1 - val2) / max_val)
            elif isinstance(val1, (list, set)) and isinstance(val2, (list, set)):
                # For collections, calculate Jaccard similarity
                set1 = set(val1)
                set2 = set(val2)
                if not set1 and not set2:
                    similarity = 1.0
                else:
                    similarity = len(set1 & set2) / len(set1 | set2)
            else:
                # For other types, use exact match
                similarity = 1.0 if val1 == val2 else 0.0
            
            similarities.append(similarity)

        return sum(similarities) / len(similarities)

    def add_update_callback(self, callback):
        self._update_callbacks.append(callback)

    def remove_update_callback(self, callback):
        if callback in self._update_callbacks:
            self._update_callbacks.remove(callback)

    def notify_update(self):
        for callback in self._update_callbacks:
            callback(self)

    def __str__(self) -> str:
        return f"Neuron(id={self.id}, activation={self._activation_strength:.2f}, data={self.data})" 