import cv2
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import math

# Freeman 8-direction lookup
directions_8 = {
    (0, 1): 0,     # right
    (1, 1): 1,     # down-right
    (1, 0): 2,     # down
    (1, -1): 3,    # down-left
    (0, -1): 4,    # left
    (-1, -1): 5,   # up-left
    (-1, 0): 6,    # up
    (-1, 1): 7     # up-right
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


# Load and preprocess image
img = cv2.imread('img/img5.jpg', cv2.IMREAD_GRAYSCALE)
if img is None:
  raise FileNotFoundError("Image not found at 'img/img3.jpg'")

_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

# Find contours
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cnt = max(contours, key=cv2.contourArea)

# Rotate and reorder contour
cnt = rotate_contour_to_start(cnt)

# print(cnt)

# Compute Freeman 8-direction chain code with explicit closing
chain_code_8 = []
for i in range(len(cnt)):
  curr = cnt[i][0]
  nxt = cnt[(i + 1) % len(cnt)][0]  # Wrap around to the first point
  dy = nxt[1] - curr[1]
  dx = nxt[0] - curr[0]
  if (dy, dx) in directions_8:
    chain_code_8.append(directions_8[(dy, dx)])

chain_code_8 = chain_code_8[-1:] + chain_code_8[:-1]

# Simulate path for reconstruction
y, x = 0, 0
ys = [y]
xs = [x]
for code in chain_code_8:
  dy, dx = inv_dir_8[code]
  y += dy
  x += dx
  ys.append(y)
  xs.append(x)

# Determine reconstructed image size
min_y, max_y = min(ys), max(ys)
min_x, max_x = min(xs), max(xs)
height = max_y - min_y + 10
width = max_x - min_x + 10

# Reconstruct shape from chain code
reconstructed = np.zeros((height, width), dtype=np.uint8)
y, x = -min_y + 5, -min_x + 5
reconstructed[y, x] = 255
for code in chain_code_8:
  dy, dx = inv_dir_8[code]
  y += dy
  x += dx
  reconstructed[y, x] = 255

# Mostrar resultados
plt.figure(figsize=(10, 4))
plt.subplot(1, 3, 1)
plt.title('Original')
plt.imshow(img, cmap='gray')

plt.subplot(1, 3, 2)
plt.title('Binaria')
plt.imshow(binary, cmap='gray')

plt.subplot(1, 3, 3)
plt.title(f'Reconstruida desde 8F')
plt.imshow(reconstructed, cmap='gray')
plt.show()


# Output chain code data
print("Cadena de códigos Freeman 8F:", chain_code_8)
print(f"Longitud de la cadena de códigos 8F: {len(chain_code_8)}")
print(f"Entropía de la cadena de códigos 8F: {calcular_entropia(chain_code_8)}")
