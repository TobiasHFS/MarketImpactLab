from abc import ABC, abstractmethod
from typing import List
import numpy as np
from src.simulation.engine import SimulationEngine

class ExecutionStrategy(ABC):
    """Base class for execution strategies."""
    
    def __init__(self, total_size: float, duration: float, start_time: float):
        self.total_size = total_size
        self.duration = duration
        self.start_time = start_time
        self.end_time = start_time + duration
        self.executed_size = 0.0

    @abstractmethod
    def on_step(self, engine: SimulationEngine):
        """Called on every simulation step."""
        pass

class TWAPStrategy(ExecutionStrategy):
    """
    Time-Weighted Average Price strategy.
    Slices order evenly over time buckets.
    """
    
    def __init__(self, total_size: float, duration: float, start_time: float, n_slices: int = 10):
        super().__init__(total_size, duration, start_time)
        self.slice_size = total_size / n_slices
        self.interval = duration / n_slices
        self.next_execution_time = start_time
        self.slices_remaining = n_slices

    def on_step(self, engine: SimulationEngine):
        if self.slices_remaining <= 0:
            return
            
        if engine.current_time >= self.next_execution_time:
            # Execute slice
            engine.submit_order(side=1, size=self.slice_size, order_type='MARKET') # Assuming Buy
            
            self.executed_size += self.slice_size
            self.slices_remaining -= 1
            self.next_execution_time += self.interval

class VWAPStrategy(ExecutionStrategy):
    """
    Volume-Weighted Average Price strategy.
    Follows a volume profile.
    """
    def __init__(self, total_size: float, duration: float, start_time: float, volume_profile: List[float]):
        super().__init__(total_size, duration, start_time)
        self.volume_profile = np.array(volume_profile) / np.sum(volume_profile)
        self.schedule = self.volume_profile * total_size
        self.current_slice_idx = 0
        # Assuming volume profile matches time intervals (e.g. 10 bins)
        self.interval = duration / len(volume_profile)
        self.next_execution_time = start_time

    def on_step(self, engine: SimulationEngine):
        if self.current_slice_idx >= len(self.schedule):
            return
            
        if engine.current_time >= self.next_execution_time:
            size_to_trade = self.schedule[self.current_slice_idx]
            engine.submit_order(side=1, size=size_to_trade, order_type='MARKET')
            
            self.executed_size += size_to_trade
            self.current_slice_idx += 1
            self.next_execution_time += self.interval
