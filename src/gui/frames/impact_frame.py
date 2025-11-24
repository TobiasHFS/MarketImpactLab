import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
from src.impact_models.parametric import AlmgrenChrissModel, ImpactParams
from src.gui.utils import embed_matplotlib_figure, clear_frame

class ImpactFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.label = ctk.CTkLabel(self.sidebar, text="Impact Analysis", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.pack(pady=20)
        
        self.eta_label = ctk.CTkLabel(self.sidebar, text="Eta (Temp Impact):")
        self.eta_label.pack(pady=(10, 0))
        self.eta_entry = ctk.CTkEntry(self.sidebar)
        self.eta_entry.insert(0, "0.1")
        self.eta_entry.pack(pady=5)
        
        self.gamma_label = ctk.CTkLabel(self.sidebar, text="Gamma (Perm Impact):")
        self.gamma_label.pack(pady=(10, 0))
        self.gamma_entry = ctk.CTkEntry(self.sidebar)
        self.gamma_entry.insert(0, "0.01")
        self.gamma_entry.pack(pady=5)
        
        self.plot_btn = ctk.CTkButton(self.sidebar, text="Plot Curves", command=self.plot_curves)
        self.plot_btn.pack(pady=20)
        
        self.plot_frame = ctk.CTkFrame(self)
        self.plot_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    def plot_curves(self):
        try:
            eta = float(self.eta_entry.get())
            gamma = float(self.gamma_entry.get())
            
            params = ImpactParams(eta=eta, gamma=gamma)
            model = AlmgrenChrissModel(params)
            
            rates = np.linspace(0, 1000, 100)
            temp_impacts = [model.calculate_temporary_impact(r, 0.02) for r in rates]
            
            clear_frame(self.plot_frame)
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(rates, temp_impacts)
            ax.set_title("Temporary Impact vs Trading Rate")
            ax.set_xlabel("Rate")
            ax.set_ylabel("Cost")
            
            embed_matplotlib_figure(self.plot_frame, fig)
            
        except ValueError:
            print("Invalid input")
