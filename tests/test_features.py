import pytest
import pandas as pd
import numpy as np
from src.features.microstructure import MicrostructureFeatures
from src.features.volatility import VolatilityFeatures

@pytest.fixture
def sample_data():
    data = {
        'timestamp': [1.0, 2.0, 3.0, 4.0, 5.0],
        'event_type': [1, 1, 4, 3, 4], # Limit, Limit, Trade, Cancel, Trade
        'side': [1, -1, 1, 1, -1], # Bid, Ask, Buy, Bid, Sell
        'price': [100.0, 101.0, 101.0, 100.0, 100.0],
        'size': [10, 10, 5, 5, 5],
        'order_id': [1, 2, 3, 1, 4]
    }
    return pd.DataFrame(data)

def test_ofi(sample_data):
    # Test OFI calculation
    # Time window 10s to capture all
    ofi = MicrostructureFeatures.calculate_ofi(sample_data, time_window='10s')
    
    # Bid Flow:
    # t=1: +10 (Limit)
    # t=4: -5 (Cancel)
    # Total Bid = +5
    
    # Ask Flow:
    # t=2: +10 (Limit)
    # Total Ask = +10
    
    # OFI = 5 - 10 = -5
    
    assert not ofi.empty
    assert ofi['ofi'].iloc[0] == -5

def test_tfi(sample_data):
    # Test TFI calculation
    tfi = MicrostructureFeatures.calculate_tfi(sample_data, time_window='10s')
    
    # Trades:
    # t=3: Buy 5 (+5)
    # t=5: Sell 5 (-5)
    # Net = 0
    
    assert not tfi.empty
    assert tfi['tfi'].iloc[0] == 0

def test_realized_volatility():
    prices = pd.Series([100, 101, 102, 101, 100])
    vol = VolatilityFeatures.calculate_realized_volatility(prices, window=3)
    assert np.isnan(vol.iloc[0])
    assert np.isnan(vol.iloc[1])
    assert not np.isnan(vol.iloc[2])

def test_volume_profile(sample_data):
    vp = VolatilityFeatures.calculate_volume_profile(sample_data, time_window='10s')
    # Total volume traded = 5 + 5 = 10
    assert vp.iloc[0] == 10
