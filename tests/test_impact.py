import pytest
import numpy as np
import pandas as pd
from src.impact_models.parametric import AlmgrenChrissModel, ImpactParams
from src.impact_models.prediction import PricePredictor

def test_almgren_chriss():
    params = ImpactParams(eta=0.1, gamma=0.01)
    model = AlmgrenChrissModel(params)
    
    # Test Temporary Impact
    # Rate = 100 shares / 1 sec = 100
    temp = model.calculate_temporary_impact(rate=100, volatility=0.02)
    assert temp == 0.1 * 100 # 10.0
    
    # Test Permanent Impact
    # Size = 1000
    perm = model.calculate_permanent_impact(size=1000)
    assert perm == 0.01 * 1000 # 10.0
    
    # Test Cost Estimate
    cost = model.estimate_cost(size=1000, time_horizon=10)
    # Rate = 100
    # Temp = 10.0
    # Perm = 10.0
    # Cost = 0.5 * 10.0 * 1000 + 10.0 * 1000 = 5000 + 10000 = 15000
    assert cost == 15000

def test_price_predictor():
    predictor = PricePredictor()
    
    # Create dummy data
    df = pd.DataFrame({
        'ofi': np.random.randn(200),
        'tfi': np.random.randn(200),
        'price': np.linspace(100, 110, 200) + np.random.randn(200)
    })
    
    predictor.train(df)
    assert predictor.is_trained
    
    # Predict
    probs = predictor.predict_proba(np.array([[0.1, 0.1]]))
    assert probs.shape == (1, 3)
    assert np.isclose(probs.sum(), 1.0)
