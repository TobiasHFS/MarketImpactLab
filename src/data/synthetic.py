import numpy as np
import pandas as pd
from typing import Tuple, Optional

class SyntheticLOBGenerator:
    """
    Generates synthetic Level-2 Limit Order Book (LOB) data.
    Simulates price process and order flow (limit orders, cancellations, market orders).
    """

    def __init__(self, 
                 symbol: str = "SYM", 
                 initial_price: float = 100.0, 
                 volatility: float = 0.02, 
                 dt: float = 1.0,
                 seed: Optional[int] = None):
        """
        Args:
            symbol: Ticker symbol.
            initial_price: Starting mid-price.
            volatility: Annualized volatility.
            dt: Time step in seconds.
            seed: Random seed.
        """
        self.symbol = symbol
        self.initial_price = initial_price
        self.volatility = volatility
        self.dt = dt
        self.rng = np.random.default_rng(seed)

    def generate_price_process(self, n_steps: int) -> np.ndarray:
        """Generates a Geometric Brownian Motion price path."""
        # Daily volatility -> per-step volatility
        sigma = self.volatility / np.sqrt(252 * 23400) # Approx seconds in trading day
        # Adjust for dt
        sigma_dt = sigma * np.sqrt(self.dt)
        
        returns = self.rng.normal(0, sigma_dt, n_steps)
        price_path = self.initial_price * np.exp(np.cumsum(returns))
        return np.insert(price_path, 0, self.initial_price)

    def generate_lob_events(self, n_events: int = 10000) -> pd.DataFrame:
        """
        Generates a stream of LOB events.
        
        Events:
        - 1: Submission of new limit order
        - 2: Cancellation (Partial)
        - 3: Deletion (Full cancellation)
        - 4: Execution (Visible)
        - 5: Execution (Hidden - ignored for now)
        """
        
        # 1. Generate underlying mid-price process
        # We assume roughly 1 event per time step for simplicity in this baseline
        mid_prices = self.generate_price_process(n_events)
        
        events = []
        current_time = 0.0
        
        for i in range(n_events):
            mid = mid_prices[i]
            current_time += self.rng.exponential(self.dt) # Random inter-arrival time
            
            # Determine event type
            # Probabilities: Limit Order (50%), Market Order (30%), Cancel (20%)
            event_type_rand = self.rng.random()
            
            if event_type_rand < 0.5:
                # Limit Order
                side = 1 if self.rng.random() < 0.5 else -1 # 1=Buy, -1=Sell
                # Price logic: centered around mid, with some spread
                spread = self.rng.lognormal(mean=-4, sigma=0.5) * mid # Relative spread
                distance = self.rng.exponential(scale=spread)
                price = mid - distance if side == 1 else mid + distance
                price = np.round(price, 2)
                size = int(self.rng.pareto(a=1.5) * 100) # Power law size
                event_code = 1
                
            elif event_type_rand < 0.8:
                # Market Order (Execution)
                side = 1 if self.rng.random() < 0.5 else -1
                # Market orders hit the best quote. For synthetic gen, we approximate execution price.
                # In a real replay, we'd match against the book. Here we just log the "trade".
                price = mid # Approx
                price = np.round(price, 2)
                size = int(self.rng.pareto(a=1.5) * 50)
                event_code = 4
                
            else:
                # Cancellation
                side = 1 if self.rng.random() < 0.5 else -1
                price = mid # Approx
                price = np.round(price, 2)
                size = int(self.rng.pareto(a=1.5) * 50)
                event_code = 3 # Deletion
            
            events.append({
                "timestamp": current_time,
                "symbol": self.symbol,
                "event_type": event_code,
                "side": side,
                "price": price,
                "size": size,
                "order_id": i # Simple sequential ID
            })
            
        df = pd.DataFrame(events)
        return df

def generate_synthetic_lob(n_events: int = 10000, **kwargs) -> pd.DataFrame:
    """Wrapper function to generate data easily."""
    generator = SyntheticLOBGenerator(**kwargs)
    return generator.generate_lob_events(n_events)

if __name__ == "__main__":
    # Test run
    df = generate_synthetic_lob(n_events=100)
    print(df.head())
