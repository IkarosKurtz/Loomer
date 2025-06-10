# src/loomer/app.py
import tkinter as tk
from tkinter import Tk, ttk

from .ui.styles import AppStyles
from .ui.tabs.image_to_code_tab import ImageToCodeTab
from .ui.tabs.code_to_image_tab import CodeToImageTab
from .ui.tabs.code_translation_tab import CodeTranslationTab


class LoomerApp:
  def __init__(self, root: Tk):
    self.root = root
    self.root.title("Loomer")
    self.root.geometry("960x540")

    # Apply styles
    self.styles = AppStyles

    # Configure window
    self.root.configure(bg=self.styles.COLOR_FONDO)

    # Create main layout
    self.create_layout()

  def create_layout(self):
    # Main content frame
    self.content_frame = tk.Frame(self.root, bg=self.styles.COLOR_FONDO)
    self.content_frame.pack(fill=tk.BOTH, expand=True)

    # Notebook (tabbed interface)
    self.notebook = ttk.Notebook(self.content_frame)

    # Configure tab styles
    AppStyles.configure_styles()

    # Create tabs
    self.image_to_code_tab = ImageToCodeTab(self.notebook)
    self.code_to_image_tab = CodeToImageTab(self.notebook)
    self.code_translation_tab = CodeTranslationTab(self.notebook)

    # Add tabs to notebook
    self.notebook.add(self.image_to_code_tab.tab, text="Imagen a Código")
    self.notebook.add(self.code_to_image_tab.tab, text="Código a Imagen")
    self.notebook.add(self.code_translation_tab.tab, text="Traducción")

    self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
