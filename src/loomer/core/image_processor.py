# src/loomer/core/image_processor.py

from src.loomer.libs.f8_f4_to_img import f4_to_image
from src.loomer.utils.pipe import Methods, Pipe
from src.loomer.libs.img_to_4f import procesar_imagen_freeman


class ImageProcessor:
  @staticmethod
  def generate_code_from_image(image, code_format="3OT"):
    """
    Generate a chain code from an image

    Args:
        image: ruta a la imagen
        code_format: Format of the chain code to generate (e.g., "3OT", "F4", etc.)

    Returns:
        A chain code string
    """
    # Simulación: En una aplicación real, aquí se procesaría la imagen
    # para generar el código de cadena según el formato especificado

    # Por ahora, devolvemos un código de ejemplo, pero en una implementación real
    # tendríamos lógica específica para cada formato
    if code_format == "F4":
      code = "".join([str(i) for i in procesar_imagen_freeman(image)])
    elif code_format == "F8":
      code = procesar_imagen_freeman(image)
      calculate = Pipe('F4', 'F8')
      code, _ = calculate(code)

      code = "".join([str(i) for i in code])
    elif code_format == "AF8":
      chain_code = procesar_imagen_freeman(image)
      calculate = Pipe('F4', 'F8', 'AF8')
      code, _ = calculate(chain_code)

      code = "".join([str(i) for i in code])
    elif code_format == "VCC":
      chain_code = procesar_imagen_freeman(image)
      calculate = Pipe('F4', 'VCC')
      code, _ = calculate(chain_code)

      code = "".join([str(i) for i in code])
    else:  # 3OT por defecto
      chain_code = procesar_imagen_freeman(image)
      calculate = Pipe('F4', '3OT')
      code, _ = calculate(chain_code)

      code = "".join([str(i) for i in code])

    return code

  @staticmethod
  def generate_image_from_code(code, code_format: Methods = "3OT", size=(300, 300)):
    """
    Generate an image from a chain code

    Args:
        code: Chain code string
        code_format: Format of the chain code (e.g., "3OT", "F4", etc.)
        size: Tuple with the desired size for the image (width, height)

    Returns:
        PIL Image object
    """
    code = [int(c) for c in code if c.isdigit()]
    if code_format == "F8":
      calculate = Pipe('F8', 'F4')
      code, _ = calculate(code)
    elif code_format == "F4":
      pass
    elif code_format == "AF8":
      calculate = Pipe('AF8', 'F8', 'F4')
      code, _ = calculate(code)
    elif code_format == "VCC":
      calculate = Pipe('VCC', 'F4')
      code, _ = calculate(code)
    elif code_format == "3OT":
      calculate = Pipe('3OT', 'F4')
      code, _ = calculate(code)
    else:
      raise ValueError(f"Formato de código no reconocido: {code_format}")
    image = f4_to_image(code, padding=15, scale=60)

    return image
