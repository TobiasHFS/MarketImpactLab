import pytest
import pandas as pd
from src.simulation.engine import SimulationEngine
from src.execution.strategies import TWAPStrategy
from src.impact_models.parametric import AlmgrenChrissModel, ImpactParams

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'timestamp': [1.0, 2.0, 3.0, 4.0, 5.0],
        'event_type': [1, 1, 1, 1, 1],
        'price': [100.0, 100.0, 100.0, 100.0, 100.0],
        'size': [100, 100, 100, 100, 100],
        'side': [1, -1, 1, -1, 1],
        'order_id': [1, 2, 3, 4, 5]
    })

def test_engine_run(sample_data):
    engine = SimulationEngine(sample_data)
    
    def dummy_strategy(eng):
        pass
        
    engine.run(dummy_strategy)
    assert engine.current_time == 5.0

def test_twap_execution(sample_data):
    engine = SimulationEngine(sample_data)
    # Total size 10, duration 5s, 2 slices -> 5 per slice
    strategy = TWAPStrategy(total_size=10, duration=5.0, start_time=0.0, n_slices=2)
    
    engine.run(strategy.on_step)
    
    assert len(engine.trades) == 2
    assert engine.trades[0].size == 5.0
    assert engine.trades[1].size == 5.0

def test_market_impact_execution(sample_data):
    params = ImpactParams(eta=1.0, gamma=0.0) # High temp impact
    model = AlmgrenChrissModel(params)
    engine = SimulationEngine(sample_data, impact_model=model)
    
    # Submit market buy
    # Impact = eta * size * 0.01 = 1.0 * 10 * 0.01 = 0.1
    # Price = 100 + 0.1 = 100.1
    
    def one_shot_strategy(eng):
        if eng.current_time == 1.0:
            eng.submit_order(side=1, size=10, order_type='MARKET')
            
    engine.run(one_shot_strategy)
    
    assert len(engine.trades) == 1
    assert engine.trades[0].price > 100.0
    assert engine.trades[0].price == 100.1
