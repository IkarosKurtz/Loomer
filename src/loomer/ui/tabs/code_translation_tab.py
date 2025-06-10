# src/loomer/ui/tabs/code_translation_tab.py
import tkinter as tk
from tkinter import ttk

from ...utils.validators import validate_numeric_input, check_numeric_content
from ...core.code_processor import CodeProcessor
from ..styles import AppStyles
from ..components import CodeFormatComboBox


class CodeTranslationTab:
  def __init__(self, parent):
    self.parent = parent
    self.styles = AppStyles
    self.tab = ttk.Frame(parent)
    self.setup_ui()

  def setup_ui(self):
    # Frame principal
    main_frame = tk.Frame(self.tab, bg=self.styles.COLOR_FONDO)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Frame izquierdo para el código de entrada
    left_frame = tk.Frame(main_frame, bg=self.styles.COLOR_FONDO)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

    # Etiqueta para el código de cadena de entrada
    left_label = tk.Label(left_frame, text="Código de cadena:",
                        fg=self.styles.COLOR_TEXTO, bg=self.styles.COLOR_FONDO)
    left_label.pack(anchor=tk.W, pady=(0, 5))

    # Área para el código de entrada (solo números)
    self.source_code_text = tk.Text(left_frame, bg=self.styles.COLOR_PRIMARIO, height=20,
                                    width=30)
    self.source_code_text.pack(fill=tk.BOTH, expand=True)
    self.source_code_text.insert(tk.END, "021301233210")

    # Validación para permitir solo números
    self.source_code_text.bind("<KeyPress>", self.on_key_press)
    self.source_code_text.bind("<KeyRelease>", self.on_key_release)

    # Frame central para los controles de traducción
    center_frame = tk.Frame(main_frame, bg=self.styles.COLOR_FONDO, width=150)
    center_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)    # Etiqueta para el traductor
    translate_label = tk.Label(center_frame, text="Traducir a:",
                                fg=self.styles.COLOR_TEXTO, bg=self.styles.COLOR_FONDO)
    translate_label.pack(anchor=tk.CENTER, pady=(120, 5))

    # Componente para la selección de formato y botón de traducción
    self.code_format_selector = CodeFormatComboBox(
        center_frame,
        label_text=None,  # Ya tenemos una etiqueta arriba
        bg=self.styles.COLOR_FONDO,
        text_color=self.styles.COLOR_TEXTO,
        combo_bg=self.styles.COLOR_PRIMARIO,
        button_text="Traducir",
        button_command=self.translate_code,
        button_color=self.styles.COLOR_SECUNDARIO
    )
    self.code_format_selector.pack(fill=tk.X)

    # Frame derecho para el código de salida
    right_frame = tk.Frame(main_frame, bg=self.styles.COLOR_FONDO)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

    # Etiqueta para el código de cadena de salida
    right_label = tk.Label(right_frame, text="Código de cadena:",
                            fg=self.styles.COLOR_TEXTO, bg=self.styles.COLOR_FONDO)
    right_label.pack(anchor=tk.W, pady=(0, 5))

    # Área para el código de salida (solo lectura)
    self.target_code_text = tk.Text(right_frame, bg=self.styles.COLOR_PRIMARIO, height=20,
                                    width=30, state="disabled")
    self.target_code_text.pack(fill=tk.BOTH, expand=True)
    self.insert_target_code("021301233210")

  def on_key_press(self, event):
    return validate_numeric_input(event)

  def on_key_release(self, event):
    check_numeric_content(self.source_code_text)

  def translate_code(self):
    # Obtener el código ingresado por el usuario
    source_code = self.source_code_text.get("1.0", tk.END).strip()
    target_format = self.code_format_selector.get_selected_format()

    # Realizar la traducción
    translated_code = CodeProcessor.translate_code(source_code, target_format=target_format)
    self.insert_target_code(translated_code)

  def insert_target_code(self, text):
    self.target_code_text.config(state="normal")
    self.target_code_text.delete(1.0, tk.END)
    self.target_code_text.insert(tk.END, text)
    self.target_code_text.config(state="disabled")
