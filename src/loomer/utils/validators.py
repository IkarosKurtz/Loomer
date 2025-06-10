# src/loomer/utils/validators.py
import tkinter as tk


def validate_numeric_input(event):
  """
  Validate that only numeric input is allowed
  Returns 'break' if the input is not allowed to prevent it from being inserted
  """
  # Permitir solo números, teclas de control y navegación
  allowed_keys = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                 'BackSpace', 'Delete', 'Left', 'Right', 'Up', 'Down',
                 'Home', 'End', 'Tab']

  if event.keysym not in allowed_keys and len(event.char) > 0:
    return "break"  # Evita que se inserte el carácter no permitido


def check_numeric_content(widget):
  """
  Check and correct the content of a text widget to ensure it only contains numeric characters
  """
  content = widget.get("1.0", tk.END).strip()
  # Eliminar cualquier carácter no numérico
  numeric_content = ''.join(filter(str.isdigit, content))
  if content != numeric_content:
    widget.delete("1.0", tk.END)
    widget.insert("1.0", numeric_content)
