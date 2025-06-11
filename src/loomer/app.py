# src/loomer/app.py
import os
import sys
import tkinter as tk
from tkinter import Tk, ttk

from PIL import ImageTk
import PIL

from .ui.styles import AppStyles
from .ui.tabs.image_to_code_tab import ImageToCodeTab
from .ui.tabs.code_to_image_tab import CodeToImageTab
from .ui.tabs.code_translation_tab import CodeTranslationTab
from .ui.tabs.code_details_tab import CodeDetailsTab


class LoomerApp:
  def __init__(self, root: Tk):
    self.root = root
    self.root.title("Loomer")

    # Determina si el script está ejecutándose como un ejecutable PyInstaller
    if getattr(sys, 'frozen', False):
      # Ruta base cuando está compilado
      base_path = sys._MEIPASS
    else:
      # Ruta base cuando se ejecuta desde el script
      base_path = os.path.dirname(os.path.abspath(__file__))
    # Ruta completa al archivo PNG
    image_path = os.path.join(base_path, "assets", "Loomer.png")

    try:
      img = PIL.Image.open(image_path)
    except FileNotFoundError:
      print(f"Error: No se encontró la imagen en {image_path}")
      sys.exit(1)
    self.root.iconphoto(True, ImageTk.PhotoImage(img))

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
    AppStyles.configure_styles()    # Create tabs
    self.image_to_code_tab = ImageToCodeTab(self.notebook)
    self.code_to_image_tab = CodeToImageTab(self.notebook)
    self.code_translation_tab = CodeTranslationTab(self.notebook)
    self.code_details_tab = CodeDetailsTab(self.notebook)

    # Add tabs to notebook
    self.notebook.add(self.image_to_code_tab.tab, text="Imagen a Código")
    self.notebook.add(self.code_to_image_tab.tab, text="Código a Imagen")
    self.notebook.add(self.code_translation_tab.tab, text="Traducción")
    self.notebook.add(self.code_details_tab.tab, text="Detalles de Código")

    self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
