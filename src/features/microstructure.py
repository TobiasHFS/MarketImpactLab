import pandas as pd
import numpy as np
from typing import Optional

class MicrostructureFeatures:
    """
    Calculates microstructure features from LOB data.
    """
    
    @staticmethod
    def calculate_spread(df: pd.DataFrame) -> pd.Series:
        """
        Calculates the bid-ask spread.
        Note: Requires a reconstructed book state. 
        For event-based data, this is an approximation based on recent best bid/ask updates.
        """
        # In a full LOB replay, we'd track the best bid/ask.
        # For this synthetic event stream, we can approximate spread if we had BBO data.
        # Since our synthetic generator outputs events, we need to reconstruct the BBO first.
        # For simplicity in this version, we will assume the 'price' in the event 
        # represents a touch of the spread (e.g. limit order at best bid/ask).
        
        # A robust implementation requires LOB reconstruction.
        # Here we will implement a simplified version that assumes we have BBO columns.
        if 'ask_price' in df.columns and 'bid_price' in df.columns:
            return df['ask_price'] - df['bid_price']
        else:
            # Return empty or error if BBO not present
            return pd.Series(np.nan, index=df.index)

    @staticmethod
    def calculate_ofi(df: pd.DataFrame, time_window: str = '1s') -> pd.DataFrame:
        """
        Calculates Order Flow Imbalance (OFI).
        OFI = Change in Bid Size - Change in Ask Size (at best quotes).
        
        This implementation aggregates events over a time window.
        """
        # Filter for Limit Orders (1) and Cancels (3)
        # Side: 1=Buy (Bid), -1=Sell (Ask)
        
        # We need to sign the size:
        # Limit Order (1): +Size
        # Cancel (3): -Size
        # Execution (4): -Size (removes liquidity)
        
        df = df.copy()
        df['signed_vol'] = df.apply(lambda x: x['size'] if x['event_type'] == 1 else -x['size'], axis=1)
        
        # Separate Bid and Ask flow
        # Bid Flow: Side 1
        # Ask Flow: Side -1
        
        df['bid_flow'] = np.where(df['side'] == 1, df['signed_vol'], 0)
        df['ask_flow'] = np.where(df['side'] == -1, df['signed_vol'], 0)
        
        # Resample
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
        resampled = df.set_index('datetime').resample(time_window)[['bid_flow', 'ask_flow']].sum()
        
        resampled['ofi'] = resampled['bid_flow'] - resampled['ask_flow']
        return resampled

    @staticmethod
    def calculate_tfi(df: pd.DataFrame, time_window: str = '1s') -> pd.DataFrame:
        """
        Calculates Trade Flow Imbalance (TFI).
        TFI = Buy Volume - Sell Volume.
        """
        df = df.copy()
        # Filter for Trades (4)
        trades = df[df['event_type'] == 4].copy()
        
        if trades.empty:
            return pd.DataFrame(columns=['tfi'])

        trades['signed_vol'] = np.where(trades['side'] == 1, trades['size'], -trades['size'])
        
        trades['datetime'] = pd.to_datetime(trades['timestamp'], unit='s')
        resampled = trades.set_index('datetime').resample(time_window)['signed_vol'].sum()
        
        return resampled.to_frame(name='tfi')
