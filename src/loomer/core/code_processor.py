# src/loomer/core/code_processor.py

from src.loomer.utils.pipe import Methods, Pipe
from rich.console import Console

console = Console()


class CodeProcessor:
  @staticmethod
  def translate_code(source_code, source_format: Methods = "3OT", target_format: Methods = "3OT"):
    """
    Translate a chain code from one format to another

    Args:
        source_code: Source chain code string
        source_format: Format of the source code
        target_format: Format to translate to

    Returns:
        Translated chain code string
    """
    # En una implementación real, aquí estaría la lógica para traducir
    # entre diferentes formatos de código de cadena

    try:
      source_code = [int(c) for c in source_code if c.isdigit()]
      chain_code = ''

      if source_format == target_format:
        return {
          'result': source_code,
          'logs': []
        }

      # Diccionario de rutas de conversión
      conversion_routes = {
        '3OT': {
          'F4': ['3OT', 'F4'],
          'F8': ['3OT', 'F4', 'F8'],
          'AF8': ['3OT', 'F4', 'F8', 'AF8'],
          'VCC': ['3OT', 'F4', 'VCC']
        },
        'AF8': {
          'F4': ['AF8', 'F8', 'F4'],
          '3OT': ['AF8', 'F8', 'F4', '3OT'],
          'F8': ['AF8', 'F8'],
          'VCC': ['AF8', 'F8', 'F4', 'VCC']
        },
        'F8': {
          'F4': ['F8', 'F4'],
          '3OT': ['F8', 'F4', '3OT'],
          'AF8': ['F8', 'AF8'],
          'VCC': ['F8', 'F4', 'VCC']
        },
        'VCC': {
          'F4': ['VCC', 'F4'],
          '3OT': ['VCC', 'F4', '3OT'],
          'AF8': ['VCC', 'F4', 'F8', 'AF8'],
          'F8': ['VCC', 'F4', 'F8']
        },
        'F4': {
          '3OT': ['F4', '3OT'],
          'F8': ['F4', 'F8'],
          'AF8': ['F4', 'F8', 'AF8'],
          'VCC': ['F4', 'VCC']
        }
      }

      try:
        # Obtener la ruta de conversión
        route = conversion_routes.get(source_format, {}).get(target_format)
        if not route:
          raise ValueError(f"Conversión no soportada: {source_format} -> {target_format}")

        # Crear el objeto Pipe con la ruta de conversión
        calculate = Pipe(*route)
      except KeyError:
        raise ValueError(f"Conversión no soportada: {source_format} -> {target_format}")

      # Aplicar la conversión
      chain_code, log = calculate(source_code)

      return {
        'result': chain_code,
        'log': log
      }
    except Exception as e:
      console.print_exception()
      return {
        'error': e
      }
