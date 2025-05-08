from typing import Any, Dict, List, Optional, Set, Tuple, Callable
from collections import defaultdict
import heapq
from datetime import datetime
from .core.neuron import Neuron
from .core.synapse import Synapse
import uuid
import threading
import queue
import time

class NeuronDB:
    def __init__(self, activation_threshold: float = 0.3, recall_depth: int = 3):
        self._neurons: Dict[str, Neuron] = {}
        self._index: Dict[str, Set[str]] = defaultdict(set)
        self.activation_threshold = activation_threshold
        self.recall_depth = recall_depth
        self._update_queue = queue.Queue()
        self._update_thread = threading.Thread(target=self._process_updates, daemon=True)
        self._update_thread.start()
        self._update_callbacks: List[Callable] = []

    def add_update_callback(self, callback: Callable):
        """Add a callback function to be called when the database is updated."""
        self._update_callbacks.append(callback)

    def remove_update_callback(self, callback: Callable):
        """Remove a callback function."""
        if callback in self._update_callbacks:
            self._update_callbacks.remove(callback)

    def notify_update(self):
        """Notify all registered callbacks of an update."""
        for callback in self._update_callbacks:
            callback(self)

    def _process_updates(self):
        """Process updates in a background thread."""
        while True:
            try:
                update_func = self._update_queue.get(timeout=0.1)
                update_func()
                self.notify_update()
            except queue.Empty:
                time.sleep(0.01)  # Prevent CPU spinning
            except Exception as e:
                print(f"Error processing update: {e}")

    def _queue_update(self, update_func: Callable):
        """Queue an update to be processed in the background."""
        self._update_queue.put(update_func)

    def create_neuron(self, data: Dict[str, Any] = None) -> Neuron:
        """Create a new neuron with the given data."""
        neuron = Neuron(data)
        self._neurons[neuron.id] = neuron
        self._index_data(neuron)
        neuron.add_update_callback(lambda n: self._queue_update(lambda: self._index_data(n)))
        return neuron

    def _index_data(self, neuron: Neuron):
        """Index the neuron's data for efficient retrieval."""
        # Clear old indices
        for key, value in neuron.data.items():
            if isinstance(value, (list, set)):
                for v in value:
                    self._index[f"{key}:{v}"].add(neuron.id)
            else:
                self._index[f"{key}:{value}"].add(neuron.id)

    def get_neuron(self, neuron_id: str) -> Optional[Neuron]:
        """Get a neuron by its ID."""
        return self._neurons.get(neuron_id)

    def create_connection(self, source_id: str, target_id: str, weight: float = 0.5, 
                         relationship_type: str = "RELATED") -> Optional[Synapse]:
        """Create a connection between two neurons."""
        source = self.get_neuron(source_id)
        target = self.get_neuron(target_id)
        
        if not source or not target:
            return None
            
        synapse = Synapse(source, target, weight, relationship_type)
        source.connections.append(synapse)
        target.connections.append(synapse)
        synapse.add_update_callback(lambda s: self._queue_update(lambda: None))
        return synapse

    def recall(self, query: Dict[str, Any], max_results: int = 10) -> List[Tuple[Neuron, float]]:
        """Recall memories based on a query."""
        activation_scores = defaultdict(float)
        visited = set()
        
        # Initial activation
        for key, value in query.items():
            if isinstance(value, (list, set)):
                for v in value:
                    for neuron_id in self._index.get(f"{key}:{v}", set()):
                        neuron = self.get_neuron(neuron_id)
                        if neuron:
                            neuron.activate(0.5)
                            activation_scores[neuron_id] += 0.5
            else:
                for neuron_id in self._index.get(f"{key}:{value}", set()):
                    neuron = self.get_neuron(neuron_id)
                    if neuron:
                        neuron.activate(0.5)
                        activation_scores[neuron_id] += 0.5
        
        # Propagate activation
        for _ in range(self.recall_depth):
            new_scores = defaultdict(float)
            for neuron_id, score in activation_scores.items():
                if score < self.activation_threshold:
                    continue
                    
                neuron = self.get_neuron(neuron_id)
                if not neuron:
                    continue
                    
                for synapse in neuron.connections:
                    target = synapse.target if synapse.source == neuron else synapse.source
                    if target.id not in visited:
                        new_scores[target.id] += score * synapse.weight
                        target.activate(synapse.weight)
                        visited.add(target.id)
            
            activation_scores.update(new_scores)
        
        # Get top results
        results = []
        for neuron_id, score in activation_scores.items():
            neuron = self.get_neuron(neuron_id)
            if neuron and score >= self.activation_threshold:
                results.append((neuron, score))
        
        return heapq.nlargest(max_results, results, key=lambda x: x[1])

    def find_similar(self, neuron_id: str, max_results: int = 10) -> List[Tuple[Neuron, float]]:
        """Find neurons similar to the given neuron."""
        neuron = self.get_neuron(neuron_id)
        if not neuron:
            return []
            
        return self.recall(neuron.data, max_results)

    def update_neuron(self, neuron_id: str, data: Dict[str, Any]) -> bool:
        """Update a neuron's data."""
        neuron = self.get_neuron(neuron_id)
        if not neuron:
            return False
            
        neuron.data.update(data)
        self._queue_update(lambda: self._index_data(neuron))
        return True

    def delete_neuron(self, neuron_id: str) -> bool:
        """Delete a neuron and its connections."""
        neuron = self.get_neuron(neuron_id)
        if not neuron:
            return False
            
        # Remove connections
        for synapse in neuron.connections[:]:
            other = synapse.target if synapse.source == neuron else synapse.source
            other.connections.remove(synapse)
            neuron.connections.remove(synapse)
        
        # Remove from index
        for key, value in neuron.data.items():
            if isinstance(value, (list, set)):
                for v in value:
                    self._index[f"{key}:{v}"].discard(neuron_id)
            else:
                self._index[f"{key}:{value}"].discard(neuron_id)
        
        # Remove neuron
        del self._neurons[neuron_id]
        self._queue_update(lambda: self.notify_update())
        return True

    def get_network_stats(self) -> Dict[str, Any]:
        """Get statistics about the neural network."""
        total_neurons = len(self._neurons)
        total_connections = sum(len(n.connections) for n in self._neurons.values()) // 2
        avg_activation = sum(n.get_activation_strength() for n in self._neurons.values()) / total_neurons if total_neurons > 0 else 0
        
        return {
            'total_neurons': total_neurons,
            'total_connections': total_connections,
            'avg_activation': avg_activation,
            'activation_threshold': self.activation_threshold,
            'recall_depth': self.recall_depth
        } 