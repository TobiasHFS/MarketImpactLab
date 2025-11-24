import numpy as np
from dataclasses import dataclass

@dataclass
class ImpactParams:
    eta: float = 0.1  # Temporary impact coefficient
    gamma: float = 0.01 # Permanent impact coefficient
    sigma: float = 0.02 # Volatility

class AlmgrenChrissModel:
    """
    Implements the Almgren-Chriss market impact model.
    
    Impact = Temporary Impact + Permanent Impact
    Temporary Impact (Slippage) = eta * (rate / volatility)
    Permanent Impact = gamma * size
    """
    
    def __init__(self, params: ImpactParams):
        self.params = params

    def calculate_temporary_impact(self, rate: float, volatility: float) -> float:
        """
        Calculates temporary impact (cost per share).
        h(v) = eta * v
        """
        # Simplified linear form: eta * rate
        # In AC2000: eta * sign(v) * |v|^beta
        # Here we assume linear: eta * rate
        return self.params.eta * rate

    def calculate_permanent_impact(self, size: float) -> float:
        """
        Calculates permanent impact (price shift).
        g(v) = gamma * size
        """
        return self.params.gamma * size

    def estimate_cost(self, size: float, time_horizon: float) -> float:
        """
        Estimates expected execution cost for a TWAP strategy over time_horizon.
        Rate = size / time_horizon
        """
        if time_horizon <= 0:
            return float('inf')
            
        rate = size / time_horizon
        temp_impact = self.calculate_temporary_impact(rate, self.params.sigma)
        perm_impact = self.calculate_permanent_impact(size)
        
        # Expected cost approx = 0.5 * Permanent * Size + Temporary * Size
        # (Assuming linear accumulation of permanent impact)
        return (0.5 * perm_impact * size) + (temp_impact * size)
