import pytest
import pandas as pd
import numpy as np
from src.data.synthetic import generate_synthetic_lob, SyntheticLOBGenerator
from src.data.loader import DataLoader

def test_synthetic_generation():
    """Test that synthetic data is generated with correct shape and columns."""
    n_events = 100
    df = generate_synthetic_lob(n_events=n_events)
    
    assert len(df) == n_events
    expected_cols = ['timestamp', 'symbol', 'event_type', 'side', 'price', 'size', 'order_id']
    assert all(col in df.columns for col in expected_cols)
    assert (df['price'] > 0).all()
    assert (df['size'] > 0).all()

def test_price_process():
    """Test that price process is reasonable."""
    gen = SyntheticLOBGenerator(initial_price=100.0, volatility=0.0)
    prices = gen.generate_price_process(10)
    # With 0 vol, prices should stay constant
    assert np.allclose(prices, 100.0)

def test_data_loader_normalization():
    """Test normalization logic."""
    data = {
        'timestamp': [1.1, 1.0],
        'event_type': [1, 1],
        'side': [1, -1],
        'price': [100.0, 101.0],
        'size': [10, 20],
        'order_id': [1, 2]
    }
    df = pd.DataFrame(data)
    normalized_df = DataLoader.normalize(df)
    
    # Check sorting
    assert normalized_df.iloc[0]['timestamp'] == 1.0
    assert normalized_df.iloc[1]['timestamp'] == 1.1
    
    # Check validation
    assert DataLoader.validate(normalized_df)

def test_invalid_data():
    """Test validation fails on bad data."""
    data = {
        'timestamp': [1.0],
        'event_type': [1],
        'side': [1],
        'price': [-100.0], # Negative price
        'size': [10],
        'order_id': [1]
    }
    df = pd.DataFrame(data)
    # Note: normalize doesn't check validity, validate does
    df = DataLoader.normalize(df)
    assert not DataLoader.validate(df)
