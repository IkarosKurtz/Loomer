# src/loomer/ui/tabs/image_to_code_tab.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


from ...core.image_processor import ImageProcessor
from ..styles import AppStyles
from ..components import ImageDisplayFrame, CodeFormatComboBox
from rich.console import Console

console = Console()


class ImageToCodeTab:
  def __init__(self, parent: ttk.Notebook):
    self.parent = parent
    self.styles = AppStyles
    self.tab = ttk.Frame(parent)
    self.setup_ui()

  def setup_ui(self):
    # Frame izquierdo para la imagen y controles
    left_frame = tk.Frame(self.tab, bg=self.styles.COLOR_FONDO)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Componente para mostrar la imagen
    self.image_display = ImageDisplayFrame(
        left_frame,
        title="Imagen",
        bg=self.styles.COLOR_FONDO,
        text_color=self.styles.COLOR_TEXTO,
        button_color=self.styles.COLOR_SECUNDARIO,
        image_size=(300, 300)
    )
    self.image_display.set_load_command(self.load_image)
    self.image_display.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)    # Dropdown y texto
    code_label = tk.Label(left_frame, text="Código de cadena a obtener:",
                         fg=self.styles.COLOR_TEXTO, bg=self.styles.COLOR_FONDO)
    code_label.pack(anchor=tk.W, pady=(20, 5))

    # Componente para la selección de formato y botón de procesamiento
    self.code_format_selector = CodeFormatComboBox(
        left_frame,
        label_text=None,  # Ya tenemos una etiqueta arriba
        bg=self.styles.COLOR_FONDO,
        text_color=self.styles.COLOR_TEXTO,
        combo_bg=self.styles.COLOR_PRIMARIO,
        button_text="Procesar",
        button_command=self.process_image,
        button_color=self.styles.COLOR_SECUNDARIO
    )
    self.code_format_selector.pack(anchor=tk.W, fill=tk.X, expand=False)

    # Frame derecho para el resultado del código
    right_frame = tk.Frame(self.tab, bg=self.styles.COLOR_FONDO)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Etiqueta para el código de cadena
    result_label = tk.Label(right_frame, text="Código de cadena:",
                          fg=self.styles.COLOR_TEXTO, bg=self.styles.COLOR_FONDO)
    result_label.pack(anchor=tk.W, pady=(0, 5))

    # Área de resultado (código generado desde la imagen)
    self.result_text = tk.Text(right_frame, bg=self.styles.COLOR_PRIMARIO, height=15,
                             width=30, state="disabled")
    self.result_text.pack(fill=tk.BOTH, expand=True)
    self.insert_result_text("")

  def load_image(self):
    """Carga una imagen desde un archivo y la muestra en el componente"""
    from PIL import Image
    from tkinter import filedialog

    file_path = filedialog.askopenfilename(
      filetypes=[("Imágenes permitidas", "*.png;*.jpg;*.jpeg")]
    )

    if file_path:
      try:
        # Cargar la imagen con PIL
        image = Image.open(file_path)
        # Establecer la imagen en el componente
        self.image_display.set_image(image, file_path)
        # Guardar referencia para el procesamiento
        self.current_image = image
      except Exception as e:
        console.print_exception()
        messagebox.showerror("Error", f"No se pudo cargar la imagen: {str(e)}")

  def process_image(self):
    # Procesar la imagen actual si existe
    _, image_path = self.image_display.get_image()
    console.print(f"Imagen cargada: {image_path}")
    if image_path:
      self.generate_code_from_image(image_path)
    else:
      # Si no hay imagen cargada, mostrar mensaje en área de resultado
      messagebox.showwarning("Advertencia", "No hay imagen para procesar. Por favor cargue una imagen primero.")

  def generate_code_from_image(self, image_path):
    try:
      # Obtener el formato seleccionado para procesar la imagen
      selected_format = self.code_format_selector.get_selected_format()
      # Pasar el formato al procesador de imágenes
      code = ImageProcessor.generate_code_from_image(image_path, code_format=selected_format)
      self.insert_result_text(code)
    except Exception as e:
      console.print_exception()
      error_msg = f"Error al procesar la imagen: {str(e)}"
      messagebox.showerror("Error de procesamiento", error_msg)
      self.insert_result_text(f"Error: {str(e)}")

  def insert_result_text(self, text):
    self.result_text.config(state="normal")
    self.result_text.delete(1.0, tk.END)
    self.result_text.insert(tk.END, text)
    self.result_text.config(state="disabled")
