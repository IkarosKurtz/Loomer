# src/loomer/ui/styles.py
from tkinter import ttk


class AppStyles:
  # Color scheme
  COLOR_FONDO = "#EAEFEF"
  COLOR_PRIMARIO = "#B8CFCE"
  COLOR_SECUNDARIO = "#7F8CAA"
  COLOR_TEXTO = "#333446"

  @staticmethod
  def configure_styles():
    """Configure ttk styles for the application"""
    style = ttk.Style()
    style.configure("TNotebook", background=AppStyles.COLOR_FONDO, borderwidth=0)
    style.configure("TFrame", background=AppStyles.COLOR_FONDO)
    style.configure("TNotebook.Tab", background=AppStyles.COLOR_FONDO, padding=[10, 2])
