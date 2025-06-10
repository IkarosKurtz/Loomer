# src/loomer/ui/components.py
import tkinter as tk
from PIL import Image, ImageTk

from .styles import AppStyles


class ImageDisplayFrame:
  """Componente para mostrar y gestionar imágenes en la interfaz"""

  def __init__(self, parent, title="Imagen", bg=AppStyles.COLOR_FONDO,
               text_color=AppStyles.COLOR_TEXTO, button_color=AppStyles.COLOR_SECUNDARIO,
               image_size=(400, 400)):
    """
    Inicializa el componente de visualización de imágenes

    Args:
        parent: Widget padre donde se mostrará este componente
        title: Título para la etiqueta de la imagen
        bg: Color de fondo
        text_color: Color del texto
        button_color: Color para los botones
        image_size: Tamaño máximo de la imagen (ancho, alto)
    """
    self.parent = parent
    self.title = title
    self.bg = bg
    self.text_color = text_color
    self.button_color = button_color
    self.image_size = image_size
    self.current_image = None
    self.photo_image = None

    # Crear el frame principal
    self.frame = tk.Frame(parent, bg=bg)
    self.setup_ui()

  def setup_ui(self):
    """Configura los elementos de la interfaz"""
    # Header con título y botón
    header_frame = tk.Frame(self.frame, bg=self.bg)
    header_frame.pack(fill=tk.X, expand=False, anchor=tk.NE)

    # Etiqueta para la imagen
    img_label = tk.Label(header_frame, text=self.title,
                        fg=self.text_color, bg=self.bg)
    img_label.pack(side=tk.LEFT, anchor=tk.NW, padx=(0, 10))

    # Botón de carga (no conectado todavía)
    self.load_btn = tk.Button(header_frame, text="Cargar",
                            bg=self.button_color, fg="white")
    self.load_btn.pack(side=tk.RIGHT, anchor=tk.NE, padx=(0, 10))

    # Contenedor para la imagen con borde y fondo
    self.image_container = tk.Frame(self.frame, bg="black",
                                  bd=1, relief=tk.SUNKEN)
    self.image_container.pack(fill=tk.BOTH, expand=True, pady=10)

    # Etiqueta para mostrar la imagen
    self.img_display = tk.Label(self.image_container, bg="black")
    self.img_display.pack(fill=tk.BOTH, expand=True)

  def set_load_command(self, command):
    """Configura la función a ejecutar al presionar el botón de carga"""
    self.load_btn.config(command=command)

  def set_image(self, pil_image):
    """
    Establece una imagen PIL para mostrar en el componente

    Args:
        pil_image: Imagen PIL a mostrar
    """
    if pil_image:
      self.current_image = pil_image
      # Redimensionar manteniendo proporción
      img_width, img_height = pil_image.size
      max_width, max_height = self.image_size

      # Calcular la escala para ajustar la imagen al contenedor
      scale = min(max_width / img_width, max_height / img_height)

      if scale < 1:  # Solo redimensionar si la imagen es más grande que el tamaño máximo
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        resized_img = pil_image.resize((new_width, new_height), Image.LANCZOS)
      else:
        resized_img = pil_image

      # Crear PhotoImage y mostrarla
      self.photo_image = ImageTk.PhotoImage(resized_img)
      self.img_display.config(image=self.photo_image)

  def get_image(self):
    """Devuelve la imagen PIL actual"""
    return self.current_image

  def pack(self, **kwargs):
    """Empaqueta el frame principal con los parámetros dados"""
    self.frame.pack(**kwargs)


class CodeFormatComboBox:
  """Componente para seleccionar formatos de códigos de cadena"""

  # Lista de formatos de códigos de cadena disponibles
  AVAILABLE_FORMATS = ["3OT", "F4", "F8", "AF8", "VCC"]

  def __init__(self, parent, label_text=None, bg=AppStyles.COLOR_FONDO,
               text_color=AppStyles.COLOR_TEXTO, combo_bg=AppStyles.COLOR_PRIMARIO,
               button_text=None, button_command=None, button_color=AppStyles.COLOR_SECUNDARIO):
    """
    Inicializa el componente de selección de formato de código

    Args:
        parent: Widget padre donde se mostrará este componente
        label_text: Texto de la etiqueta para el combobox (None para no mostrar etiqueta)
        bg: Color de fondo
        text_color: Color del texto
        combo_bg: Color de fondo para el frame del combobox
        button_text: Texto para el botón opcional (None para no mostrar botón)
        button_command: Función a ejecutar cuando se presiona el botón
        button_color: Color para el botón
    """
    self.parent = parent
    self.bg = bg
    self.text_color = text_color
    self.combo_bg = combo_bg
    self.button_text = button_text
    self.button_command = button_command
    self.button_color = button_color

    # Crear el contenedor principal
    self.container = tk.Frame(parent, bg=bg)

    # Crear la etiqueta si se proporciona texto
    if label_text:
      self.label = tk.Label(self.container, text=label_text,
                          fg=text_color, bg=bg)
      self.label.pack(anchor=tk.W, pady=(0, 5))

    # Frame para el combobox y botón
    self.combo_container = tk.Frame(self.container, bg=bg)
    self.combo_container.pack(fill=tk.X, expand=True)

    # Frame para el combobox
    self.combo_frame = tk.Frame(self.combo_container, bg=combo_bg, padx=2, pady=2)
    self.combo_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

    # ComboBox
    from tkinter import ttk
    self.combo = ttk.Combobox(self.combo_frame, values=self.AVAILABLE_FORMATS, state="readonly")
    self.combo.current(0)  # Seleccionar el primer elemento por defecto
    self.combo.pack(fill=tk.X)

    # Añadir botón opcional
    if button_text and button_command:
      self.button = tk.Button(self.combo_container, text=button_text,
                            bg=button_color, fg="white",
                            command=button_command)
      self.button.pack(side=tk.RIGHT, padx=(10, 0))

  def get_selected_format(self):
    """Devuelve el formato de código seleccionado actualmente"""
    return self.combo.get()

  def set_selected_format(self, format_name):
    """Establece el formato de código seleccionado"""
    if format_name in self.AVAILABLE_FORMATS:
      self.combo.set(format_name)

  def pack(self, **kwargs):
    """Empaqueta el contenedor principal con los parámetros dados"""
    self.container.pack(**kwargs)
