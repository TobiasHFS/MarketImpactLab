import customtkinter as ctk
import matplotlib.pyplot as plt
from src.data.synthetic import generate_synthetic_lob
from src.gui.utils import embed_matplotlib_figure, clear_frame

class DataFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar for controls
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.label = ctk.CTkLabel(self.sidebar, text="Data Generation", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.pack(pady=20)
        
        # Inputs
        self.vol_label = ctk.CTkLabel(self.sidebar, text="Volatility:")
        self.vol_label.pack(pady=(10, 0))
        self.vol_entry = ctk.CTkEntry(self.sidebar)
        self.vol_entry.insert(0, "0.02")
        self.vol_entry.pack(pady=5)
        
        self.events_label = ctk.CTkLabel(self.sidebar, text="Num Events:")
        self.events_label.pack(pady=(10, 0))
        self.events_entry = ctk.CTkEntry(self.sidebar)
        self.events_entry.insert(0, "1000")
        self.events_entry.pack(pady=5)
        
        self.generate_btn = ctk.CTkButton(self.sidebar, text="Generate", command=self.generate_data)
        self.generate_btn.pack(pady=20)
        
        # Main area for plot
        self.plot_frame = ctk.CTkFrame(self)
        self.plot_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        self.generated_data = None

    def generate_data(self):
        try:
            vol = float(self.vol_entry.get())
            n_events = int(self.events_entry.get())
            
            self.generated_data = generate_synthetic_lob(n_events=n_events, volatility=vol)
            
            # Plot
            clear_frame(self.plot_frame)
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(self.generated_data['timestamp'], self.generated_data['price'])
            ax.set_title("Synthetic Price Process")
            ax.set_xlabel("Time")
            ax.set_ylabel("Price")
            
            embed_matplotlib_figure(self.plot_frame, fig)
            
        except ValueError:
            print("Invalid input")
