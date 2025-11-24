import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
from src.impact_models.parametric import AlmgrenChrissModel

@dataclass
class Order:
    id: int
    side: int # 1=Buy, -1=Sell
    size: float
    type: str # 'MARKET', 'LIMIT'
    price: Optional[float] = None
    timestamp: float = 0.0
    filled: float = 0.0
    status: str = 'NEW' # NEW, FILLED, CANCELED

@dataclass
class Trade:
    timestamp: float
    price: float
    size: float
    side: int
    cost: float = 0.0 # Transaction cost / slippage

class SimulationEngine:
    """
    Event-driven LOB replay engine.
    """
    
    def __init__(self, data: pd.DataFrame, impact_model: Optional[AlmgrenChrissModel] = None):
        self.data = data.sort_values('timestamp').reset_index(drop=True)
        self.impact_model = impact_model
        self.current_time = 0.0
        self.current_price = 100.0 # Default fallback
        self.trades: List[Trade] = []
        self.active_orders: List[Order] = []
        self.order_id_counter = 0

    def submit_order(self, side: int, size: float, order_type: str = 'MARKET', price: Optional[float] = None) -> int:
        """Submits an order to the simulation."""
        self.order_id_counter += 1
        order = Order(
            id=self.order_id_counter,
            side=side,
            size=size,
            type=order_type,
            price=price,
            timestamp=self.current_time
        )
        self.active_orders.append(order)
        return order.id

    def run(self, strategy_step_func: Callable[['SimulationEngine'], None]):
        """
        Runs the simulation.
        strategy_step_func: Callback function called on every event (or periodically).
        """
        for _, event in self.data.iterrows():
            self.current_time = event['timestamp']
            
            # Update market state
            if event['event_type'] in [1, 4]: # Limit or Trade
                # Update price estimate (using last trade or mid approx)
                self.current_price = event['price']
            
            # 1. Check for fills (Limit Orders)
            # Simplified: If price crosses limit, fill.
            # Real matching would require full LOB reconstruction.
            self._match_limit_orders()
            
            # 2. Execute Market Orders immediately
            self._execute_market_orders()
            
            # 3. Strategy Step
            strategy_step_func(self)
            
    def _match_limit_orders(self):
        """Matches active limit orders against current price."""
        for order in self.active_orders:
            if order.status != 'NEW' or order.type != 'LIMIT':
                continue
                
            # Buy Limit: Fill if Current Price <= Limit Price
            if order.side == 1 and self.current_price <= order.price:
                self._fill_order(order, self.current_price)
                
            # Sell Limit: Fill if Current Price >= Limit Price
            elif order.side == -1 and self.current_price >= order.price:
                self._fill_order(order, self.current_price)

    def _execute_market_orders(self):
        """Executes market orders with impact."""
        for order in self.active_orders:
            if order.status != 'NEW' or order.type != 'MARKET':
                continue
            
            # Calculate execution price with impact
            exec_price = self.current_price
            
            if self.impact_model:
                # Estimate impact
                # We assume instantaneous impact for the trade
                # Rate is infinite for instantaneous, but we use a proxy or just the perm/temp formula
                # For simplicity: Price + Impact
                # Impact = eta * size (simplified linear impact for single trade)
                impact = self.impact_model.params.eta * order.size * 0.01 # Scaling factor
                if order.side == 1:
                    exec_price += impact
                else:
                    exec_price -= impact
            
            self._fill_order(order, exec_price)

    def _fill_order(self, order: Order, price: float):
        """Records a fill."""
        order.filled = order.size
        order.status = 'FILLED'
        
        trade = Trade(
            timestamp=self.current_time,
            price=price,
            size=order.size,
            side=order.side
        )
        self.trades.append(trade)
