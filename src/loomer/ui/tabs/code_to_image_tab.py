# src/loomer/ui/tabs/code_to_image_tab.py
import tkinter as tk
from tkinter import ttk

from ...utils.validators import validate_numeric_input, check_numeric_content
from ...utils.file_handlers import save_image_file
from ...core.image_processor import ImageProcessor
from ..styles import AppStyles
from ..components import ImageDisplayFrame, CodeFormatComboBox


class CodeToImageTab:
  def __init__(self, parent):
    self.parent = parent
    self.styles = AppStyles
    self.tab = ttk.Frame(parent)
    self.current_image = None
    self.setup_ui()

  def setup_ui(self):
    # Frame izquierdo para ingresar el código
    left_frame = tk.Frame(self.tab, bg=self.styles.COLOR_FONDO)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Etiqueta para el código de cadena
    code_label = tk.Label(left_frame, text="Código de cadena:",
                        fg=self.styles.COLOR_TEXTO, bg=self.styles.COLOR_FONDO)
    code_label.pack(anchor=tk.W, pady=(0, 5))

    # Área para ingresar el código (solo números)
    self.code_text = tk.Text(left_frame, bg=self.styles.COLOR_PRIMARIO, height=15,
                            width=30)
    self.code_text.pack(fill=tk.BOTH, expand=True)
    self.code_text.insert(tk.END, "021301233210")

    # Validación para permitir solo números
    # self.code_text.bind("<KeyPress>", self.on_key_press)
    self.code_text.bind("<KeyRelease>", self.on_key_release)    # Dropdown y texto
    code_label = tk.Label(left_frame, text="Código de cadena a leer:",
                         fg=self.styles.COLOR_TEXTO, bg=self.styles.COLOR_FONDO)
    code_label.pack(anchor=tk.W, pady=(20, 5))

    # Componente para la selección de formato y botón de generación
    self.code_format_selector = CodeFormatComboBox(
        left_frame,
        label_text=None,  # Ya tenemos una etiqueta arriba
        bg=self.styles.COLOR_FONDO,
        text_color=self.styles.COLOR_TEXTO,
        combo_bg=self.styles.COLOR_PRIMARIO,
        button_text="Generar Imagen",
        button_command=self.generate_image_from_code_input,
        button_color=self.styles.COLOR_SECUNDARIO
    )
    self.code_format_selector.pack(anchor=tk.W, fill=tk.X, expand=False, pady=(0, 10))

    # Frame derecho para la imagen generada
    right_frame = tk.Frame(self.tab, bg=self.styles.COLOR_FONDO)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Componente para mostrar la imagen generada
    self.image_display = ImageDisplayFrame(
        right_frame,
        title="Imagen Generada",
        bg=self.styles.COLOR_FONDO,
        text_color=self.styles.COLOR_TEXTO,
        button_color=self.styles.COLOR_SECUNDARIO,
        image_size=(300, 300)
    )
    # Cambiamos el texto del botón a "Guardar"
    self.image_display.load_btn.config(text="Guardar")
    self.image_display.set_load_command(self.save_image)
    self.image_display.pack(fill=tk.BOTH, expand=True, pady=10)

  def on_key_press(self, event):
    return validate_numeric_input(event)

  def on_key_release(self, event):
    check_numeric_content(self.code_text)

  def generate_image_from_code_input(self):
    # Obtener el código ingresado por el usuario
    code = self.code_text.get("1.0", tk.END).strip()
    # Obtener el formato seleccionado
    selected_format = self.code_format_selector.get_selected_format()
    self.generate_image_from_code(code, selected_format)

  def generate_image_from_code(self, code, code_format):
    # Generar imagen basada en el código y formato seleccionado
    self.current_image = ImageProcessor.generate_image_from_code(code, code_format=code_format)
    # Mostrar la imagen en el componente
    if self.current_image:
      self.image_display.set_image(self.current_image, None)
    else:
      print("No se pudo generar la imagen desde el código")

  def save_image(self):
    # Obtenemos la imagen actual del componente
    image, _ = self.image_display.get_image()
    if image:
      save_image_file(image)
