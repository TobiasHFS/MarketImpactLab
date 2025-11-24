import pandas as pd
import numpy as np
from typing import Union, List

class DataLoader:
    """
    Handles loading and normalization of LOB data.
    """
    
    @staticmethod
    def load_from_csv(filepath: str) -> pd.DataFrame:
        """Loads LOB data from a CSV file."""
        df = pd.read_csv(filepath)
        return DataLoader.normalize(df)
    
    @staticmethod
    def normalize(df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalizes column names and types.
        Expected columns: timestamp, event_type, side, price, size, order_id
        """
        # Ensure required columns exist
        required_cols = ['timestamp', 'event_type', 'side', 'price', 'size']
        if not all(col in df.columns for col in required_cols):
            # Try to map common names if exact matches aren't found
            # This is a placeholder for more complex mapping logic
            pass
            
        # Sort by timestamp
        df = df.sort_values('timestamp').reset_index(drop=True)
        
        # Ensure types
        df['timestamp'] = df['timestamp'].astype(float)
        df['event_type'] = df['event_type'].astype(int)
        df['side'] = df['side'].astype(int)
        df['price'] = df['price'].astype(float)
        df['size'] = df['size'].astype(float)
        
        return df

    @staticmethod
    def validate(df: pd.DataFrame) -> bool:
        """Basic validation checks."""
        if df.empty:
            return False
        if (df['price'] <= 0).any():
            return False
        if (df['size'] <= 0).any():
            return False
        return True
