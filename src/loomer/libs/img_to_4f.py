import PIL
import PIL.Image
import numpy as np
from collections import Counter
import math

# Freeman 4-direction mapping
directions_4 = {
    (1, 0): 0,    # Derecha
    (0, 1): 1,    # Abajo
    (-1, 0): 2,   # Izquierda
    (0, -1): 3    # Arriba
}
inv_dir_4 = {v: k for k, v in directions_4.items()}


def calcular_entropia(cadena):
  total = len(cadena)
  conteo = Counter(cadena)
  entropia = -sum((f / total) * math.log2(f / total) for f in conteo.values())
  return entropia


def find_start_point(binary):
  """Find top-left object pixel with background neighbor"""
  padded = np.pad(binary, 1, 'constant', constant_values=0)
  for y in range(1, padded.shape[0] - 1):
    for x in range(1, padded.shape[1] - 1):
      if padded[y, x] == 255:  # Object pixel found
        # Check top and left neighbors
        if padded[y - 1, x] == 0 or padded[y, x - 1] == 0:
          return x, y
  return None


def trace_boundary(binary):
  """Trace boundary using vertex-based representation"""
  # Pad image to handle borders
  padded = np.pad(binary, 1, 'constant', constant_values=0)
  start_point = find_start_point(binary)
  if start_point is None:
    return [], []
  start_x, start_y = start_point

  # Adjust start to vertex coordinates (top-left corner)
  vx, vy = start_x, start_y  # Vertex position
  d = 0  # Initial direction: right
  chain = []
  visited = set()
  path = [(vx, vy)]  # Track vertices

  for _ in range(10000):  # Prevent infinite loops
    # Move in current direction
    dx, dy = inv_dir_4[d]
    vx += dx
    vy += dy
    chain.append(d)
    path.append((vx, vy))

    # Check if back to start
    if (vx, vy) == (start_x, start_y) and len(chain) > 0:
      break

    # Turn left (counter-clockwise)
    d = (d + 3) % 4
    found = False
    for _ in range(4):
      # Get pixel coordinates adjacent to current edge
      dx, dy = inv_dir_4[d]
      if d == 0:  # Right
        px, py = vx, vy
      elif d == 1:  # Down
        px, py = vx - 1, vy
      elif d == 2:  # Left
        px, py = vx - 1, vy - 1
      else:  # Up
        px, py = vx, vy - 1

      # Check pixel in padded image
      if padded[py, px] == 255:
        found = True
        break
      # Turn right if background
      d = (d + 1) % 4

    if not found:
      break

  return chain, path


def procesar_imagen_freeman(image_path, umbral=127) -> list:
  """
  Procesa una imagen para generar su código de cadena Freeman de 4 direcciones.

  Args:
      imagen: Ruta o URL de la imagen a procesar
      umbral: Valor de umbral para la binarización (0-255)

  Returns:
      Lista con el código de cadena Freeman
  """
  # Cargar y preprocesar imagen
  try:
    image = PIL.Image.open(image_path)
    img = image.convert('L')  # 'L' para escala de grises
    img_array = np.array(img)
  except Exception as e:
    print(f"Error al cargar la imagen <img_to_4f>: {e}")
    return []

  # Binarizar con NumPy
  binary = np.zeros_like(img_array)
  binary[img_array < umbral] = 255  # Invertir como THRESH_BINARY_INV

  # Obtener código de cadena F4 y ruta de vértices
  chain_code_4, vertex_path = trace_boundary(binary)

  # Variable para almacenar la imagen reconstruida
  reconstructed = None

  # Reconstruir forma a partir del código de cadena
  if chain_code_4:
    xs, ys = zip(*vertex_path)
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    width = max_x - min_x + 1
    height = max_y - min_y + 1

    # Crear imagen vacía
    reconstructed = np.zeros((height, width), dtype=np.uint8)
    for x, y in vertex_path:
      # Ajustar coordenadas para que encajen en la imagen
      adj_x = x - min_x
      adj_y = y - min_y
      if 0 <= adj_y < height and 0 <= adj_x < width:
        reconstructed[adj_y, adj_x] = 255

  # Simplemente devolver el código de cadena
  return chain_code_4


# Ejemplo de uso
if __name__ == "__main__":
  # Procesar una imagen y obtener el código de cadena
  # Cambia esto a la ruta de tu imagen
  ruta_imagen = './assets/WhatsApp Image 2025-06-09 at 14.26.32.jpeg'
  codigo_freeman = procesar_imagen_freeman(ruta_imagen)

  if codigo_freeman:
    print(f"Código de cadena Freeman: {codigo_freeman}")
    print(f"Longitud: {len(codigo_freeman)}")
    print(f"Entropía: {calcular_entropia(codigo_freeman):.4f}")
