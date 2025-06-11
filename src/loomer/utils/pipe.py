# Clase para encadenar traducciones de códigos de cadena

from typing import Literal

from src.loomer.utils.functions import obtener_datos_de_cadena
from ..libs.chain_code_translators import (
    convertirF8toF4, convertirF4toF8,
    convertirF4toVCC, convertirVCCtoF4,
    convertirF4to3OT, convertir3OTtoF4,
    convertirF8toAF8, convertirAF8toF8
)

Methods = Literal[
  'F4',
  'F8',
  'AF8',
  'VCC',
  '3OT'
]


class Pipe:
  """
  Clase para encadenar conversiones de códigos de cadena.
  Permite definir una secuencia de conversiones y aplicarlas en orden.

  Ejemplo de uso:
      calculate = Pipe('F4', 'F8', 'AF8')
      chain_code = calculate(f4_chain_code)
  """

  def __init__(self, *formats: Methods):
    """
    Inicializa un pipeline de conversiones.

    Args:
        input: El formato del código de cadena de entrada (ej. 'F4', 'F8', 'VCC', '3OT', 'AF8')
        *formats: Secuencia de formatos a los que se debe convertir en orden
    """
    self.input_format = formats[0]
    self.conversion_sequence = list(formats[1:])

    # Mapeo de conversiones disponibles
    self.converters = {
        ('F8', 'F4'): convertirF8toF4,
        ('F4', 'F8'): convertirF4toF8,
        ('F4', 'VCC'): convertirF4toVCC,
        ('VCC', 'F4'): convertirVCCtoF4,
        ('F4', '3OT'): convertirF4to3OT,
        ('3OT', 'F4'): convertir3OTtoF4,
        ('F8', 'AF8'): convertirF8toAF8,
        ('AF8', 'F8'): convertirAF8toF8
    }

    self._allowed_formats = [
      'F4-F8',
      'F8-F4',
      'F4-VCC',
      'F4-3OT',
      'F4-F8-AF8',
      'F8-F4-VCC',
      'F8-F4-3OT',
      'AF8-F8-F4-VCC',
      'AF8-F8-F4-3OT'
    ]

    # Validar la secuencia de conversión
    self._validate_sequence()

    # self._validate_formats()

  def _validate_sequence(self):
    """Valida que la secuencia de conversión sea posible"""
    if not self.input_format or not self.conversion_sequence:
      raise ValueError("Se requiere un formato de entrada y al menos un formato de salida")

    # Verificar que todas las conversiones existan
    current_format = self.input_format
    for next_format in self.conversion_sequence:
      if (current_format, next_format) not in self.converters:
        raise ValueError(f"No existe un convertidor de {current_format} a {next_format}")
      current_format = next_format

  def _validate_formats(self):
    """Valida que el camino de conversiones sea posible"""
    transitions = [self.input_format] + self.conversion_sequence
    transitions_string = '-'.join(transitions)

    if transitions_string not in self._allowed_formats:
      raise ValueError(f"El camino de conversiones {transitions_string} no es posible")

  def __call__(self, chain_code):
    """
    Aplica la secuencia de conversiones al código de cadena.

    Args:
        chain_code: El código de cadena a convertir (lista de enteros)

    Returns:
        El código de cadena convertido según la secuencia especificada (lista de enteros)
    """
    if not isinstance(chain_code, list):
      raise ValueError("El código de cadena debe ser una lista de enteros")

    current_format = self.input_format
    current_chain = chain_code

    # Para seguimiento de las conversiones
    conversion_log = {
        'input': {
            'format': self.input_format,
            'chain_code': chain_code
        },
        'steps': [],
        'output': None
    }

    for next_format in self.conversion_sequence:
      # Obtener el convertidor adecuado
      converter = self.converters[(current_format, next_format)]

      # Aplicar la conversión
      current_chain = converter(current_chain)

      # Registrar este paso de conversión
      conversion_log['steps'].append({
          'from': current_format,
          'to': next_format,
          'result': current_chain
      })

      # Actualizar el formato actual
      current_format = next_format

    # Registrar el resultado final
    conversion_log['output'] = {
        'format': current_format,
        'chain_code': current_chain,
        'frequency': obtener_datos_de_cadena(current_chain)
    }

    return current_chain, conversion_log

  def get_available_formats(self):
    """
    Devuelve los formatos de códigos de cadena disponibles para conversión.

    Returns:
        Conjunto de formatos disponibles
    """
    formats = set()
    for pair in self.converters.keys():
      formats.add(pair[0])
      formats.add(pair[1])
    return formats

  def get_possible_conversions(self):
    """
    Devuelve todas las conversiones posibles.

    Returns:
        Diccionario con los pares de conversión disponibles
    """
    return dict(self.converters)


# Ejemplo de uso
if __name__ == "__main__":
  # Definir una secuencia de conversiones: F4 -> F8 -> AF8
  calculate = Pipe('F4', 'F8', 'AF8')

  # Código de cadena F4 de ejemplo
  f4_chain_code = [0, 1, 0, 1, 0, 1, 2, 2, 2, 3, 3, 3]

  # Aplicar las conversiones
  result = calculate(f4_chain_code)

  print("Código de cadena original (F4):", f4_chain_code)
  print("Código de cadena convertido (AF8):", result)

  # Ejemplo de conversión más compleja: F4 -> F8 -> AF8 -> F8 -> F4
  calculate_roundtrip = Pipe('F4', 'F8', 'AF8', 'F8', 'F4')
  roundtrip_result = calculate_roundtrip(f4_chain_code)

  print("\nConversión de ida y vuelta:")
  print("F4 original:", f4_chain_code)
  print("F4 después de convertir a F8->AF8->F8->F4:", roundtrip_result)
