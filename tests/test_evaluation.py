import pytest
import pandas as pd
from src.evaluation.backtest import BacktestRunner
from src.evaluation.metrics import ExecutionMetrics
from src.execution.strategies import TWAPStrategy
from src.impact_models.parametric import AlmgrenChrissModel, ImpactParams
from src.simulation.engine import Trade

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

def test_metrics():
    trades = [
        Trade(timestamp=1.0, price=100.0, size=10, side=1),
        Trade(timestamp=2.0, price=101.0, size=10, side=1)
    ]
    
    # VWAP = (1000 + 1010) / 20 = 100.5
    vwap = ExecutionMetrics.calculate_vwap(trades)
    assert vwap == 100.5
    
    # Slippage vs Arrival (100.0)
    # (100.5 - 100.0) / 100.0 * 10000 = 0.5% = 50 bps
    slippage = ExecutionMetrics.calculate_slippage(trades, benchmark_price=100.0)
    assert slippage == 50.0

def test_backtest_runner(sample_data):
    params = ImpactParams(eta=0.0, gamma=0.0)
    model = AlmgrenChrissModel(params)
    runner = BacktestRunner(sample_data, model)
    
    strategy_params = {
        'total_size': 10,
        'duration': 5.0,
        'start_time': 0.0,
        'n_slices': 2
    }
    
    trades = runner.run(TWAPStrategy, strategy_params)
    assert len(trades) == 2
