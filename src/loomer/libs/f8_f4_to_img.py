import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image

from src.loomer.utils.functions import calcular_entropia


# Corrected Freeman 8 directions for image coordinates (y positive = downward)
directions_8F = [
    (0, 1),   # 0: Derecha
    (1, 1),   # 1: Abajo-Derecha
    (1, 0),   # 2: Abajo
    (1, -1),  # 3: Abajo-Izquierda
    (0, -1),  # 4: Izquierda
    (-1, -1),  # 5: Arriba-Izquierda
    (-1, 0),  # 6: Arriba
    (-1, 1)   # 7: Arriba-Derecha
]
directions_4F = [
    (1, 0),   # 0: Derecha
    (0, 1),   # 1: Abajo
    (-1, 0),  # 2: Izquierda
    (0, -1)   # 3: Arriba
]


def fill_holes(binary_image):
  """
  Apply morphological operations to fill holes in a binary image.

  Args:
      binary_image: A binary image as a numpy array

  Returns:
      A binary image with holes filled
  """
  # Create a mask with the border set to 0 and the interior to 1
  h, w = binary_image.shape[:2]
  mask = np.zeros((h + 2, w + 2), np.uint8)

  # Make a copy of the image to work with
  img_copy = binary_image.copy()

  # Create a seed point in the background (top-left corner)
  seed_pt = (0, 0)

  # Value to fill with
  fill_value = 255

  # Perform the flood fill from the background
  # Any background pixel connected to the seed becomes 255
  cv2.floodFill(img_copy, mask, seed_pt, fill_value)

  # Invert the flood-filled image
  # Now the original foreground and holes are 0, and the background is 255
  img_inv = cv2.bitwise_not(img_copy)

  # Combine the original image with the inverted flood-fill
  # This keeps the original foreground and fills the holes
  filled_img = binary_image | img_inv

  return filled_img


def chain_code_to_coordinates(chain_code, directions):
  """
  Converts a chain code to a list of coordinates using the given directions.
  """
  x_coords = [0]
  y_coords = [0]
  current_x, current_y = 0, 0

  for code in chain_code:
    if code in range(len(directions)):
      dx, dy = directions[code]
      current_x += dx
      current_y += dy
      x_coords.append(current_x)
      y_coords.append(current_y)

  return x_coords, y_coords


def f8_to_image(chain_code, padding=5, scale=1):
  """
  Converts a Freeman 8-direction chain code to a PIL image.

  Args:
      chain_code: List of integers representing the Freeman 8-direction chain code
      padding: Padding around the image in pixels
      scale: Scale factor for the image

  Returns:
      PIL.Image: The generated image
  """
  # Convert string to list of integers if needed
  if isinstance(chain_code, str):
    chain_code = [int(c) for c in chain_code if c.isdigit() and int(c) in range(8)]

  # # Validate chain code
  # if not chain_code or any(int(code) not in [0, 1, 2, 3, 4, 5, 6, 7] for code in chain_code):
  #   print("\nADVERTENCIA: El código de cadena contiene direcciones inválidas para 8F!")
  #   print("Se ignorarán códigos inválidos.")
  #   # If there are no valid codes, return an empty image
  #   if not chain_code:
  #     return Image.new('L', (100, 100), 0)

  # Get coordinates
  x_coords, y_coords = chain_code_to_coordinates(chain_code, directions_8F)

  if not x_coords or not y_coords:
    return None

  min_x, max_x = min(x_coords), max(x_coords)
  min_y, max_y = min(y_coords), max(y_coords)

  # Create image
  width = (max_x - min_x + 1) * scale + 2 * padding
  height = (max_y - min_y + 1) * scale + 2 * padding
  img = np.zeros((height, width), dtype=np.uint8)

  # Draw chain code
  cx = (0 - min_x) * scale + padding
  cy = (0 - min_y) * scale + padding
  img[cy, cx] = 255

  for code in chain_code:
    if code in range(8):
      dx, dy = directions_8F[code]
      cx += dx
      cy += dy
      if 0 <= cx < width and 0 <= cy < height:
        img[cy, cx] = 255
      else:
        break

  img = fill_holes(img)

  # Convert to PIL image
  pil_img = Image.fromarray(img)

  # Calculate entropy for reporting
  # entropia = calcular_entropia(chain_code)
  # print(f"Imagen reconstruida con 8F desde la cadena de códigos.")
  # print(f"Dimensiones de la imagen: {width}x{height}")
  # print(f"Longitud de la cadena de códigos: {len(chain_code)}")
  # print(f"Entropía de la cadena de códigos: {entropia:.4f}")

  return pil_img


def f4_to_image(chain_code, padding=5, scale=10):
  """
  Converts a Freeman 4-direction chain code to a PIL image.

  Args:
      chain_code: List of integers or string representing the Freeman 4-direction chain code
      padding: Padding around the image in pixels
      scale: Scale factor for the image (larger for F4 for better visibility)

  Returns:
      PIL.Image: The generated image
  """
  # Convert string to list of integers if needed
  if isinstance(chain_code, str):
    chain_code = [int(c) for c in chain_code if c.isdigit() and int(c) in range(4)]

  # # Validate chain code
  # if not chain_code or any(code not in range(4) for code in chain_code):
  #   print("\nADVERTENCIA: El código de cadena contiene direcciones inválidas para 4F!")
  #   print("La reconstrucción 4F puede ser incorrecta. Se ignorarán códigos inválidos.")
  #   # If there are no valid codes, return an empty image
  #   if not chain_code:
  #     return Image.new('L', (100, 100), 0)

  # Get coordinates
  x_coords, y_coords = chain_code_to_coordinates(chain_code, directions_4F)

  if not x_coords or not y_coords:
    return None

  min_x, max_x = min(x_coords), max(x_coords)
  min_y, max_y = min(y_coords), max(y_coords)

  # Create image
  width = (max_x - min_x + 1) * scale + 2 * padding
  height = (max_y - min_y + 1) * scale + 2 * padding
  img = np.zeros((height, width), dtype=np.uint8)

  # Draw chain code as lines (for F4)
  cx = (0 - min_x) * scale + padding
  cy = (0 - min_y) * scale + padding

  for code in chain_code:
    if code in range(4):
      dx, dy = directions_4F[code]
      nx = cx + dx * scale
      ny = cy + dy * scale
      cv2.line(img, (cx, cy), (nx, ny), (255,), 1)
      cx, cy = nx, ny

  img = fill_holes(img)

  # Convert to PIL image
  pil_img = Image.fromarray(img)

  # Calculate entropy for reporting
  # entropia = calcular_entropia(chain_code)
  # print(f"Imagen reconstruida con 4F desde la cadena de códigos.")
  # print(f"Dimensiones de la imagen: {width}x{height}")
  # print(f"Longitud de la cadena de códigos: {len(chain_code)}")
  # print(f"Entropía de la cadena de códigos: {entropia:.4f}")

  return pil_img


def show_chain_code_image(img, title="Contorno reconstruido"):
  """
  Display a PIL image with matplotlib
  """
  plt.figure(figsize=(6, 6))
  plt.imshow(np.array(img), cmap='gray', interpolation='nearest')
  plt.title(title)
  plt.axis('off')
  plt.show()


# Example usage (can be commented out when imported as a module)
if __name__ == "__main__":
  # Example chain codes
  f8_chain_code = [0, 0, 0, 2, 3, 4, 4, 4, 6, 7]  # F8
  f4_chain_code = [0, 0, 0, 0, 1, 1, 2, 1, 2, 2, 1, 2, 3, 2, 3, 3, 0, 3]  # F4

  print("Ingresa 1 para usar el código de cadena 8F o 2 para usar el código de cadena 4F")
  option = int(input("Opción: "))

  if option == 1:
    img = f8_to_image(f8_chain_code)
    show_chain_code_image(img, "Contorno reconstruido 8F")
  elif option == 2:
    img = f4_to_image(f4_chain_code)
    show_chain_code_image(img, "Contorno reconstruido 4F")
  else:
    print("Opción inválida. Saliendo.")
