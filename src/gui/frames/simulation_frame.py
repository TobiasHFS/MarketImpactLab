import customtkinter as ctk
import matplotlib.pyplot as plt
from src.data.synthetic import generate_synthetic_lob
from src.impact_models.parametric import AlmgrenChrissModel, ImpactParams
from src.execution.strategies import TWAPStrategy, VWAPStrategy
from src.evaluation.backtest import BacktestRunner
from src.evaluation.metrics import ExecutionMetrics
from src.gui.utils import embed_matplotlib_figure, clear_frame

class SimulationFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.label = ctk.CTkLabel(self.sidebar, text="Simulation", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.pack(pady=20)
        
        self.strategy_var = ctk.StringVar(value="TWAP")
        self.strategy_menu = ctk.CTkOptionMenu(self.sidebar, values=["TWAP", "VWAP"], variable=self.strategy_var)
        self.strategy_menu.pack(pady=10)
        
        self.size_label = ctk.CTkLabel(self.sidebar, text="Total Size:")
        self.size_label.pack(pady=(10, 0))
        self.size_entry = ctk.CTkEntry(self.sidebar)
        self.size_entry.insert(0, "1000")
        self.size_entry.pack(pady=5)
        
        self.run_btn = ctk.CTkButton(self.sidebar, text="Run Simulation", command=self.run_simulation)
        self.run_btn.pack(pady=20)
        
        self.result_label = ctk.CTkLabel(self.sidebar, text="")
        self.result_label.pack(pady=10)
        
        self.plot_frame = ctk.CTkFrame(self)
        self.plot_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    def run_simulation(self):
        try:
            size = float(self.size_entry.get())
            strategy_name = self.strategy_var.get()
            
            # Generate fresh data for sim
            df = generate_synthetic_lob(n_events=2000, volatility=0.1)
            start_time = df['timestamp'].min()
            duration = df['timestamp'].max() - start_time
            
            params = ImpactParams(eta=0.5, gamma=0.01)
            model = AlmgrenChrissModel(params)
            runner = BacktestRunner(df, model)
            
            strat_params = {
                'total_size': size,
                'duration': duration,
                'start_time': start_time
            }
            
            if strategy_name == "TWAP":
                strat_params['n_slices'] = 10
                strat_cls = TWAPStrategy
            else:
                strat_params['volume_profile'] = [1] * 10
                strat_cls = VWAPStrategy
                
            trades = runner.run(strat_cls, strat_params)
            
            # Metrics
            vwap = ExecutionMetrics.calculate_vwap(trades)
            slippage = ExecutionMetrics.calculate_slippage(trades, df.iloc[0]['price'])
            
            self.result_label.configure(text=f"VWAP: {vwap:.2f}\nSlippage: {slippage:.2f} bps")
            
            # Plot
            clear_frame(self.plot_frame)
            fig, ax = plt.subplots(figsize=(6, 4))
            
            # Plot market price
            ax.plot(df['timestamp'], df['price'], label='Market Price', alpha=0.5)
            
            # Plot executions
            trade_times = [t.timestamp for t in trades]
            trade_prices = [t.price for t in trades]
            ax.scatter(trade_times, trade_prices, color='red', label='Executions', zorder=5)
            
            ax.set_title(f"{strategy_name} Execution Analysis")
            ax.legend()
            
            embed_matplotlib_figure(self.plot_frame, fig)
            
        except ValueError:
            print("Invalid input")
