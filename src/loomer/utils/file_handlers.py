# src/loomer/utils/file_handlers.py
from tkinter import filedialog
from PIL import Image, ImageTk


def load_image_file(display_widget, size=(300, 300)):
  """
  Open file dialog to select an image and display it in the given widget

  Args:
      display_widget: Tkinter widget to display the image
      size: Tuple with the desired size for the image (width, height)

  Returns:
      The loaded image object or None if no image was loaded
  """
  file_path = filedialog.askopenfilename(
      filetypes=[("Imágenes permitidas", "*.png;*.jpg;*.jpeg")]
  )

  if file_path:
    try:
      image = Image.open(file_path)
      image = image.resize(size, Image.LANCZOS)
      photo = ImageTk.PhotoImage(image)
      display_widget.config(image=photo)
      display_widget.image = photo  # Mantener referencia
      return image
    except Exception as e:
      print(f"Error al cargar la imagen: {e}")
      return None

  return None


def save_image_file(image):
  """
  Open file dialog to save an image

  Args:
      image: PIL Image object to save

  Returns:
      The file path where the image was saved or None if cancelled
  """
  file_path = filedialog.asksaveasfilename(
      defaultextension=".png",
      filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg;*.jpeg"), ("BMP", "*.bmp")]
  )

  if file_path and image:
    try:
      image.save(file_path)
      return file_path
    except Exception as e:
      print(f"Error al guardar la imagen: {e}")
      return None

  return None
