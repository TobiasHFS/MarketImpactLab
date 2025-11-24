import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from typing import Tuple

class PricePredictor:
    """
    Predicts short-term price movement (Up/Down/Stationary).
    """
    
    def __init__(self):
        self.model = LogisticRegression(multi_class='multinomial', solver='lbfgs')
        self.scaler = StandardScaler()
        self.is_trained = False

    def prepare_features(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepares features and targets.
        Features: OFI, Spread, Depth Imbalance (if available).
        Target: Next mid-price move direction.
        """
        # Placeholder feature engineering
        # Assuming df has 'ofi' and 'spread' columns from feature engineering step
        
        # Create targets: 1 (Up), 0 (Flat), -1 (Down)
        # We need future returns
        # For this mock, we'll generate dummy features if not present
        
        X = df[['ofi', 'tfi']].fillna(0).values
        
        # Target: Sign of next return
        # We need to shift returns backwards
        # Assuming df has 'mid_price' or we use 'price'
        if 'price' in df.columns:
            returns = df['price'].pct_change().shift(-1)
            y = np.sign(returns).fillna(0).astype(int)
        else:
            y = np.zeros(len(df))
            
        return X, y

    def train(self, df: pd.DataFrame):
        """Trains the prediction model."""
        X, y = self.prepare_features(df)
        
        # Filter out NaNs
        mask = ~np.isnan(X).any(axis=1)
        X = X[mask]
        y = y[mask]
        
        if len(X) > 100:
            X_scaled = self.scaler.fit_transform(X)
            self.model.fit(X_scaled, y)
            self.is_trained = True

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predicts probabilities of [Down, Flat, Up]."""
        if not self.is_trained:
            return np.ones((len(X), 3)) / 3 # Uniform prior
            
        X_scaled = self.scaler.transform(X)
        return self.model.predict_proba(X_scaled)
