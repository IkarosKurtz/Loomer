import cv2
import numpy as np
from collections import Counter
import math

# Freeman 8-direction lookup
directions_8 = {
  (0, 1): 0,     # derecha
  (1, 1): 1,     # abajo-derecha
  (1, 0): 2,     # abajo
  (1, -1): 3,    # abajo-izquierda
  (0, -1): 4,    # izquierda
  (-1, -1): 5,   # arriba-izquierda
  (-1, 0): 6,    # arriba
  (-1, 1): 7     # arriba-derecha
}
inv_dir_8 = {v: k for k, v in directions_8.items()}


def calcular_entropia(cadena):
  total = len(cadena)
  conteo = Counter(cadena)
  entropia = -sum((f / total) * math.log2(f / total) for f in conteo.values())
  return entropia


def rotate_contour_to_start(contour):
  """Rotate and reverse contour to start at top-leftmost and go clockwise"""
  if contour.size == 0:
    return contour
  points = contour.reshape(-1, 2)
  start_idx = min(range(len(points)), key=lambda i: (points[i][1], points[i][0]))
  rotated = np.concatenate((points[start_idx:], points[:start_idx]), axis=0)
  rotated = rotated[::-1]  # Reverse to make it clockwise
  return rotated.reshape((-1, 1, 2)).astype(contour.dtype)


def procesar_imagen_freeman_8(ruta_imagen, umbral=127):
  """
  Procesa una imagen y genera su código de cadena Freeman de 8 direcciones.

  Args:
      ruta_imagen: Ruta a la imagen a procesar
      umbral: Valor de umbral para la binarización (0-255)

  Returns:
      Lista con el código de cadena Freeman de 8 direcciones
  """
  try:
    # Cargar y preprocesar imagen
    img = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
    if img is None:
      print(f"Error: No se pudo cargar la imagen en {ruta_imagen}")
      return []

    # Binarizar la imagen
    _, binary = cv2.threshold(img, umbral, 255, cv2.THRESH_BINARY_INV)

    # Encontrar contornos
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not contours:
      print("No se encontraron contornos en la imagen")
      return []

    # Seleccionar el contorno más grande
    cnt = max(contours, key=cv2.contourArea)

    # Rotar y reordenar el contorno
    cnt = rotate_contour_to_start(cnt)

    # Calcular el código de cadena Freeman de 8 direcciones
    chain_code_8 = []
    for i in range(len(cnt)):
      curr = cnt[i][0]
      nxt = cnt[(i + 1) % len(cnt)][0]  # Envolver al primer punto
      dy = nxt[1] - curr[1]
      dx = nxt[0] - curr[0]
      if (dy, dx) in directions_8:
        chain_code_8.append(directions_8[(dy, dx)])

    # Ajustar el código de cadena
    if chain_code_8:
      chain_code_8 = chain_code_8[-1:] + chain_code_8[:-1]

    return chain_code_8

  except Exception as e:
    print(f"Error al procesar la imagen: {e}")
    return []


# Ejemplo de uso
if __name__ == "__main__":
  # Ejemplo 1: Obtener sólo el código de cadena
  ruta_imagen = './assets/WhatsApp Image 2025-06-09 at 14.26.33(3).jpeg'
  codigo_freeman = procesar_imagen_freeman_8(ruta_imagen)
  print(f"Código de cadena Freeman 8F: {codigo_freeman}")
  print(f"Longitud: {len(codigo_freeman)}")
  print(f"Entropía: {calcular_entropia(codigo_freeman):.4f}")
