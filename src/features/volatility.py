import pandas as pd
import numpy as np

class VolatilityFeatures:
    """
    Calculates volatility and liquidity features.
    """
    
    @staticmethod
    def calculate_realized_volatility(prices: pd.Series, window: int = 20) -> pd.Series:
        """
        Calculates rolling realized volatility (std dev of returns).
        """
        returns = prices.pct_change()
        return returns.rolling(window=window).std()

    @staticmethod
    def calculate_volume_profile(df: pd.DataFrame, time_window: str = '1min') -> pd.Series:
        """
        Calculates volume profile (total traded volume per bucket).
        """
        trades = df[df['event_type'] == 4].copy()
        if trades.empty:
            return pd.Series()
            
        trades['datetime'] = pd.to_datetime(trades['timestamp'], unit='s')
        return trades.set_index('datetime').resample(time_window)['size'].sum()
