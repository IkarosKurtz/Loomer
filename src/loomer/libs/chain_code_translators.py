# Traductor de cadenas de códigos de figuras


directions_F8 = [
    (1, 0),    # 0
    (1, -1),   # 1
    (0, -1),   # 2
    (-1, -1),  # 3
    (-1, 0),   # 4
    (-1, 1),   # 5
    (0, 1),    # 6
    (1, 1)     # 7
]

directions_F4 = [
    (1, 0),    # 0
    (0, -1),   # 1
    (-1, 0),   # 2
    (0, 1)     # 3
]

_F8toF4 = {
    (0, 0): (0,), (0, 1): (0, 1, 0), (0, 2): (0, 1), (0, 3): (0, 1, 2, 1), (0, 7): (0, 3),
    (1, 0): None, (1, 1): (1, 0), (1, 2): (1,), (1, 3): (1, 2, 1), (1, 4): (1, 2), (1, 7): (3,),  # Changed [3] to (3,)
    # Changed [1] to (1,), [1,2,1] to (1,2,1), etc.
    (2, 1): (1, 0), (2, 2): (1,), (2, 3): (1, 2, 1), (2, 4): (1, 2), (2, 5): (1, 2, 3, 2),
    (3, 1): (0,), (3, 2): None, (3, 3): (2, 1), (3, 4): (2,), (3, 5): (2, 3, 2), (3, 6): (2, 3),
    (4, 3): (2, 1), (4, 4): (2,), (4, 5): (2, 3, 2), (4, 6): (2, 3), (4, 7): (2, 3, 0, 3),
    (5, 0): (3, 0), (5, 3): (1,), (5, 4): None, (5, 5): (3, 2), (5, 6): (3,), (5, 7): (3, 0, 3),
    (6, 0): (3, 0), (6, 1): (2, 0, 1, 0), (6, 5): (3, 2), (6, 6): (3,), (6, 7): (3, 0, 3),
    (7, 0): (0,), (7, 1): (0, 1, 0), (7, 2): (0, 1), (7, 5): (2,), (7, 6): None, (7, 7): (0, 3), }

_F4toVCC = {
    (0, 0): 0,
    (0, 1): 1,
    (0, 3): 2,
    (1, 0): 2,
    (1, 1): 0,
    (1, 2): 1,
    (2, 1): 2,
    (2, 2): 0,
    (2, 3): 1,
    (3, 0): 1,
    (3, 2): 2,
    (3, 3): 0
}

_VCCtoF4 = {
    (0, 0): 0,
    (0, 1): 1,
    (0, 2): 3,
    (1, 0): 1,
    (1, 1): 2,
    (1, 2): 0,
    (2, 0): 2,
    (2, 1): 3,
    (2, 2): 1,
    (3, 0): 3,
    (3, 1): 0,
    (3, 2): 2
}

_F4toF8 = {
    (0, 0): 0,
    (0, 1): None,
    (0, 3): 7,
    (1, 0): 1,
    (1, 1): 2,
    (1, 2): None,
    (2, 1): 3,
    (2, 2): 4,
    (2, 3): None,
    (3, 0): None,
    (3, 2): 5,
    (3, 3): 6
}

_F8toAF8 = {
    (0, 0): 0,
    (0, 1): 1,
    (0, 2): 2,
    (0, 3): 3,
    (0, 4): 4,
    (0, 5): 5,
    (0, 6): 6,
    (0, 7): 7,
    (1, 0): 7,
    (1, 1): 0,
    (1, 2): 1,
    (1, 3): 2,
    (1, 4): 3,
    (1, 5): 4,
    (1, 6): 5,
    (1, 7): 6,
    (2, 0): 6,
    (2, 1): 7,
    (2, 2): 0,
    (2, 3): 1,
    (2, 4): 2,
    (2, 5): 3,
    (2, 6): 4,
    (2, 7): 5,
    (3, 0): 5,
    (3, 1): 6,
    (3, 2): 7,
    (3, 3): 0,
    (3, 4): 1,
    (3, 5): 2,
    (3, 6): 3,
    (3, 7): 4,
    (4, 0): 4,
    (4, 1): 5,
    (4, 2): 6,
    (4, 3): 7,
    (4, 4): 0,
    (4, 5): 1,
    (4, 6): 2,
    (4, 7): 3,
    (5, 0): 3,
    (5, 1): 4,
    (5, 2): 5,
    (5, 3): 6,
    (5, 4): 7,
    (5, 5): 0,
    (5, 6): 1,
    (5, 7): 2,
    (6, 0): 2,
    (6, 1): 3,
    (6, 2): 4,
    (6, 3): 5,
    (6, 4): 6,
    (6, 5): 7,
    (6, 6): 0,
    (6, 7): 1,
    (7, 0): 1,
    (7, 1): 2,
    (7, 2): 3,
    (7, 3): 4,
    (7, 4): 5,
    (7, 5): 6,
    (7, 6): 7,
    (7, 7): 0
}

# Funciones de conversión entre códigos de cadena


def convertirF8toF4(cadena):
  cadena_convertida = [0,]

  for i in range(len(cadena)):
    if i == 0:
      if (cadena[i] == 1):
        cadena_convertida.extend([1, 0])
      continue
    if (_F8toF4[(cadena[i - 1], cadena[i])] == None):
      continue
    cadena_convertida.extend(_F8toF4[(cadena[i - 1], cadena[i])])

  # Add this to process the last-to-first pair (close the chain)
  if (_F8toF4.get((cadena[-1], cadena[0])) is not None):
    if (cadena[-1] == 7):
      pass
    elif (cadena[-1] == 6):
      cadena_convertida.append(cadena_convertida[-1])
    else:
      cadena_convertida.extend(_F8toF4[(cadena[-1], cadena[0])])
      cadena_convertida.pop()

  return cadena_convertida


def convertirF4toF8(cadena):
  cadena_convertida = []
  for i in range(len(cadena) - 1):
    par = (cadena[i], cadena[i + 1])
    if par in _F4toF8:
      val = _F4toF8[par]
      if val is not None:
        cadena_convertida.append(val)
      if i == len(cadena) - 2:
        par_final = (cadena[i + 1], cadena[0])
        if par_final in _F4toF8:
          val_final = _F4toF8[par_final]
          if val_final is not None:
            cadena_convertida.append(val_final)
    else:
      raise ValueError(f"Par {par} no reconocido en el mapeo _F4toF8.")

  return cadena_convertida


def convertirF4toVCC(cadena):
  cadena_convertida = []
  for i in range(len(cadena) - 1):
    if (cadena[i], cadena[i + 1]) in _F4toVCC:
      cadena_convertida.append(_F4toVCC[(cadena[i], cadena[i + 1])])
    if i == len(cadena) - 2:
      # AUN NO SE SI SE COMPARA EL PRIMERO Y EL ULTIMO O SE AGREGA UN UNO DIRECTAMENTE
      cadena_convertida.insert(0, 1)

  return cadena_convertida


def convertirVCCtoF4(cadena):
  cadena_convertida = [0]
  for i in range(len(cadena) - 1):
    cadena_convertida.append(_VCCtoF4[(cadena_convertida[i], cadena[i + 1])])

  return cadena_convertida


def convertirF4to3OT(f4_code):
  n = len(f4_code)
  if n < 2:
    raise ValueError("El código F4 debe tener al menos 2 elementos.")

  c3ot = []

  ref = f4_code[0]
  support = f4_code[0]
  primer_cambio_detectado = False

  for i in range(1, n):
    change = f4_code[i]

    if change == support:
      c3ot.append(0)
    else:
      # Detectamos el primer cambio real
      if not primer_cambio_detectado:
        c3ot.append(2)
        primer_cambio_detectado = True
      elif change == ref:
        c3ot.append(1)
        ref = support
      elif (change - ref) % 4 == 2:
        c3ot.append(2)
        ref = support
      else:
        c3ot.append(1)
        ref = support

    support = change

  # Agregamos la última transición circular (con respecto al primero)
  change = f4_code[0]
  if change == support:
    c3ot.append(0)
  elif not primer_cambio_detectado:
    c3ot.append(2)
  elif change == ref:
    c3ot.append(1)
  elif (change - ref) % 4 == 2:
    c3ot.append(2)
  else:
    c3ot.append(1)

  return c3ot


def convertir3OTtoF4(code_3ot):
  if not code_3ot or len(code_3ot) < 1:
    raise ValueError("El código 3OT no puede estar vacío.")

  # Convención de referencia: ref = 3, support = 0 (no incluimos ref en el resultado final)
  f4_code = []  # solo el soporte real
  ref = 3
  support = 0

  for symbol in code_3ot:  # Empezamos en el segundo símbolo
    if symbol == 0:
      change = support
    elif symbol == 1:
      change = ref
      ref = support
    elif symbol == 2:
      change = (ref + 2) % 4
      ref = support
    else:
      raise ValueError(f"Símbolo inválido en código 3OT: {symbol}")

    support = change
    f4_code.append(change)

  f4_code = [f4_code[-1]] + f4_code[:-1]

  return f4_code


def convertirF8toAF8(cadena):
  new_chain_code = []
  for i in range(len(cadena) - 1):
    if (cadena[i], cadena[i + 1]) in _F8toAF8:
      new_chain_code.append(_F8toAF8[(cadena[i], cadena[i + 1])])
    if i == len(cadena) - 2:
      new_chain_code.insert(0, _F8toAF8[(cadena[i + 1], cadena[0])])

  return new_chain_code


def convertirAF8toF8(cadena):
  # CREEMOS QUE SIEMPRE SE LE PONE UN 0 AL PRINCIPIO
  new_chain_code = [0]
  for i in range(len(cadena) - 1):
    new_chain_code.append((cadena[i + 1] + new_chain_code[i]) % 8)

  return new_chain_code


# cadena = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 2, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 2, 1, 1, 7, 0, 7, 0, 7, 6, 6, 0, 7, 7, 0, 0, 7, 0, 0, 0, 0, 0, 0, 7, 1, 1, 7, 1, 7, 0, 1, 0, 1, 7, 1, 0, 0, 7, 0, 0, 7, 0, 7, 0, 0, 7, 7, 0, 0, 0, 0, 7, 0, 0, 0, 7, 0, 0, 7, 7, 0, 7, 0, 0, 0, 7, 1, 0, 0, 1, 7, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 7, 1, 0, 7, 1, 0, 0, 2, 1, 7, 1, 0, 0, 1, 0, 2, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 2, 1, 1, 0, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 2, 1, 0, 2, 2, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 0, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 2, 1, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 3, 2, 3, 4, 3, 2, 2, 2, 1, 2, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 4, 4, 5, 4, 4, 4, 4, 4, 4, 3, 2, 3, 3, 5, 3, 3, 4, 4, 4, 4, 3, 3, 1, 0, 1, 1, 1, 0, 2, 1, 0, 1, 3, 2, 2, 2, 3, 2, 1, 2, 3, 1, 2, 3, 2, 2, 3, 2, 4, 3, 2, 3, 3, 3, 2, 5, 3, 3, 2, 5, 4, 3, 4, 5, 3, 3, 5, 3, 2, 2, 4, 3, 5, 5, 6, 6, 5, 3, 4, 3, 2, 2, 4, 3, 6, 5, 4, 5, 3, 4, 5, 4, 6, 6, 5, 5, 5, 4, 7, 5, 6, 7, 6, 6, 7, 6, 6, 7, 6, 0, 7, 7, 6, 7, 0, 7, 6, 7, 5, 6, 5, 5, 7, 5, 4, 5, 6, 5, 4, 4, 5, 5, 3, 5, 4, 4, 5, 4, 5, 3, 2, 5, 4, 4, 4, 5, 3, 4, 5, 4, 5, 3, 5, 3, 5, 4, 3, 5, 4, 4, 4, 5, 3, 5, 5, 3, 2, 5, 4, 4, 5, 3, 4, 5, 4, 5, 3, 4, 5, 4, 4, 3, 5, 4, 4, 5, 4, 4, 4, 5, 4, 5, 3, 5, 4, 5, 5, 3, 6, 5, 3, 4, 5, 4, 4, 5, 4, 4, 5, 4, 4, 5, 5, 3, 6, 5, 3, 4, 5, 4, 4, 4, 5, 5, 5, 5, 4, 6, 5, 4, 5, 4, 5, 3, 5, 4, 4, 5, 5, 5, 5, 4, 5, 3, 2, 2, 3, 2, 2, 3, 1, 4, 3, 1, 3, 3, 3, 2, 3, 4, 3, 2, 5, 4, 4, 4, 3, 3, 4, 6, 5, 4, 5, 3, 4, 4, 4, 4, 3, 4, 3, 4, 3, 4, 4, 4, 4, 5, 5, 5, 4, 5, 5, 6, 6, 7, 5, 7, 6, 7, 6, 5, 6, 7, 6, 6, 0, 7, 6, 7, 0, 7, 6, 7, 7, 0, 0, 1, 0, 1, 7, 6, 6, 7, 5, 7, 6, 6, 7, 7, 6, 6, 6, 5, 7, 7, 6, 7, 6, 6, 7, 5, 4, 6, 5, 6, 6, 5, 4, 6, 6, 5, 4, 6, 5, 4, 6, 6, 5, 6, 6, 6, 6, 6, 5, 6, 6, 5, 6, 6, 5, 5, 5, 5, 4, 6, 5, 3, 5, 4, 6, 5, 4, 5, 5, 5, 5, 4, 6, 5, 4, 4, 4, 5, 5, 5, 5, 5, 5, 3, 5, 5, 7, 5, 4, 4, 5, 4, 5, 5, 5, 6, 5, 4, 4, 4, 4, 4, 6, 6, 6, 5, 5, 4, 5, 4, 4, 5, 4, 4, 5, 4, 5, 4, 5, 5, 6, 6, 6, 6, 6, 6, 6, 7, 6, 6, 7, 6, 5, 6, 6, 6, 6, 6, 7, 0, 0, 7, 0, 7, 0, 7]
# cadena = [0, 0, 0, 0, 1, 1, 2, 1, 2, 2, 2, 2, 3, 3, 0, 3]

# cadena = [0,0,0,0,1,1,2,1,2,2,2,2,3,3,0,3]
cadena = [1, 2, 4, 6, 6]

print(convertirF8toF4(cadena))
# res = convertirF4toF8(cadena)
# print(res, obtener_datos_de_cadena(res))
# print("".join([str(i) for i in cadena]) ==
# "".join([str(i) for i in convertir3OTtoF4(convertirF4to3OT(cadena))])
# )


# print(convertirF8toAF8(cadena))

# cadena2 = [1, 0, 0, 2, 1, 1, 0, 0, 2, 1]

# print(convertirAF8toF8(cadena2))
