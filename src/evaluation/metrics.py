import pandas as pd
import numpy as np
from typing import List
from src.simulation.engine import Trade

class ExecutionMetrics:
    """
    Calculates execution performance metrics.
    """
    
    @staticmethod
    def calculate_vwap(trades: List[Trade]) -> float:
        """Calculates VWAP of executed trades."""
        if not trades:
            return 0.0
            
        total_vol = sum(t.size for t in trades)
        total_val = sum(t.price * t.size for t in trades)
        
        return total_val / total_vol if total_vol > 0 else 0.0

    @staticmethod
    def calculate_slippage(trades: List[Trade], benchmark_price: float) -> float:
        """
        Calculates slippage in basis points relative to a benchmark price (e.g. Arrival Price).
        Slippage (bps) = (ExecPrice - Benchmark) / Benchmark * 10000 * Side
        """
        if not trades:
            return 0.0
            
        exec_vwap = ExecutionMetrics.calculate_vwap(trades)
        side = trades[0].side # Assuming all trades same side
        
        return (exec_vwap - benchmark_price) / benchmark_price * 10000 * side

    @staticmethod
    def calculate_implementation_shortfall(trades: List[Trade], arrival_price: float, total_target_size: float) -> float:
        """
        Calculates Implementation Shortfall (IS).
        IS = Execution Cost + Opportunity Cost
        """
        if not trades:
            return 0.0
            
        executed_size = sum(t.size for t in trades)
        exec_vwap = ExecutionMetrics.calculate_vwap(trades)
        side = trades[0].side
        
        # Execution Cost: (ExecPrice - Arrival) * ExecutedSize
        exec_cost = (exec_vwap - arrival_price) * executed_size * side
        
        # Opportunity Cost: (ClosePrice - Arrival) * UnexecutedSize
        # Simplified: We assume opportunity cost is 0 for fully filled, or we need close price.
        # Here we just return Execution Cost part for simplicity if fully filled.
        
        return exec_cost
