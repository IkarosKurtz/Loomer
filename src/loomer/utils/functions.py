from collections import Counter, defaultdict
import math


def calcular_entropia(cadena):
  total = len(cadena)
  conteo = Counter(cadena)
  entropia = -sum((f / total) * math.log2(f / total) for f in conteo.values())
  return entropia


def obtener_datos_de_cadena(cadena):
  contador = defaultdict(int)
  for valor in cadena:
    contador[str(valor)] += 1

  return dict(sorted(contador.items(), key=lambda x: x[0], reverse=False))
