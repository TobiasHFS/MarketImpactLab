import pandas as pd
from typing import List, Dict, Type
from src.simulation.engine import SimulationEngine, Trade
from src.execution.strategies import ExecutionStrategy
from src.impact_models.parametric import AlmgrenChrissModel

class BacktestRunner:
    """
    Runs backtests for a given strategy and data.
    """
    
    def __init__(self, data: pd.DataFrame, impact_model: AlmgrenChrissModel):
        self.data = data
        self.impact_model = impact_model

    def run(self, strategy_cls: Type[ExecutionStrategy], strategy_params: Dict) -> List[Trade]:
        """
        Runs a single backtest.
        """
        engine = SimulationEngine(self.data, self.impact_model)
        
        # Instantiate strategy
        # We assume strategy_params contains all necessary args except those derived from data/context
        # For simplicity, we pass them directly.
        strategy = strategy_cls(**strategy_params)
        
        engine.run(strategy.on_step)
        
        return engine.trades
