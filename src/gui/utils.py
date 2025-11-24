import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk

def embed_matplotlib_figure(master, figure):
    """Embeds a matplotlib figure into a customtkinter frame."""
    canvas = FigureCanvasTkAgg(figure, master=master)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    return canvas

def clear_frame(frame):
    """Clears all widgets from a frame."""
    for widget in frame.winfo_children():
        widget.destroy()
