import customtkinter as ctk
from src.gui.frames.data_frame import DataFrame
from src.gui.frames.impact_frame import ImpactFrame
from src.gui.frames.simulation_frame import SimulationFrame

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MarketImpactApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Market Impact & Optimal Execution Lab")
        self.geometry("1000x600")
        
        # Grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Navigation Frame
        self.nav_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.nav_frame.grid(row=0, column=0, sticky="nsew")
        self.nav_frame.grid_rowconfigure(4, weight=1)
        
        self.nav_label = ctk.CTkLabel(self.nav_frame, text="Antigravity Lab", font=ctk.CTkFont(size=15, weight="bold"))
        self.nav_label.grid(row=0, column=0, padx=20, pady=20)
        
        self.btn_data = ctk.CTkButton(self.nav_frame, text="Data & Features", command=lambda: self.show_frame("data"))
        self.btn_data.grid(row=1, column=0, padx=20, pady=10)
        
        self.btn_impact = ctk.CTkButton(self.nav_frame, text="Impact Models", command=lambda: self.show_frame("impact"))
        self.btn_impact.grid(row=2, column=0, padx=20, pady=10)
        
        self.btn_sim = ctk.CTkButton(self.nav_frame, text="Simulation", command=lambda: self.show_frame("sim"))
        self.btn_sim.grid(row=3, column=0, padx=20, pady=10)
        
        # Frames
        self.frames = {}
        self.frames["data"] = DataFrame(self)
        self.frames["impact"] = ImpactFrame(self)
        self.frames["sim"] = SimulationFrame(self)
        
        self.show_frame("data")

    def show_frame(self, name):
        # Hide all
        for frame in self.frames.values():
            frame.grid_forget()
            
        # Show selected
        self.frames[name].grid(row=0, column=1, sticky="nsew")

if __name__ == "__main__":
    app = MarketImpactApp()
    app.mainloop()
