# src/loomer/ui/tabs/code_details_tab.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.loomer.utils.validators import check_numeric_content

from ...utils.functions import calcular_entropia, obtener_datos_de_cadena
from ..styles import AppStyles


class CodeDetailsTab:
  def __init__(self, parent):
    self.parent = parent
    self.styles = AppStyles
    self.tab = ttk.Frame(parent)
    self.setup_ui()

  def setup_ui(self):
    # Frame izquierdo para ingresar el código
    left_frame = tk.Frame(self.tab, bg=self.styles.COLOR_FONDO)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Etiqueta para el código de cadena
    code_label = tk.Label(left_frame, text="Código de cadena a analizar:",
                    fg=self.styles.COLOR_TEXTO, bg=self.styles.COLOR_FONDO)
    code_label.pack(anchor=tk.W, pady=(0, 5))

    # Área para ingresar el código
    self.code_text = tk.Text(left_frame, bg=self.styles.COLOR_PRIMARIO, height=15,
                        width=30)
    self.code_text.pack(fill=tk.BOTH, expand=True)
    self.code_text.bind("<KeyRelease>", self.on_key_release)    # Dropdown y texto

    self.code_text.insert(tk.END, "")  # Valor por defecto

    # Botón de análisis
    analyze_button = tk.Button(left_frame, text="Analizar Código",
                        bg=self.styles.COLOR_SECUNDARIO, fg="white",
                        command=self.analyze_code)
    analyze_button.pack(anchor=tk.W, pady=(10, 0))

    # Frame derecho para mostrar detalles
    right_frame = tk.Frame(self.tab, bg=self.styles.COLOR_FONDO)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10,
                     pady=10)    # Frame para mostrar estadísticas de texto
    stats_frame = tk.Frame(right_frame, bg=self.styles.COLOR_FONDO)
    stats_frame.pack(side=tk.TOP, fill=tk.X, expand=False, pady=(0, 10))

    # Etiqueta para la entropía
    self.entropy_label = tk.Label(stats_frame, text="Entropía: N/A",
                        fg=self.styles.COLOR_TEXTO, bg=self.styles.COLOR_FONDO,
                        font=("Arial", 12, "bold"))
    self.entropy_label.pack(anchor=tk.W, pady=(0, 2))

    # Etiqueta para el índice i de la fórmula
    self.entropy_i_label = tk.Label(stats_frame, text="",
                        fg=self.styles.COLOR_TEXTO, bg=self.styles.COLOR_FONDO,
                        font=("Arial", 12, "bold"))
    self.entropy_i_label.pack(anchor=tk.W, pady=(0, 5))

    # Etiqueta para la longitud
    self.length_label = tk.Label(stats_frame, text="Longitud: N/A",
                        fg=self.styles.COLOR_TEXTO, bg=self.styles.COLOR_FONDO,
                        font=("Arial", 12))
    self.length_label.pack(anchor=tk.W, pady=(0, 5))

    # Etiqueta para caracteres únicos
    self.unique_chars_label = tk.Label(stats_frame, text="Caracteres únicos: N/A",
                        fg=self.styles.COLOR_TEXTO, bg=self.styles.COLOR_FONDO,
                        font=("Arial", 12))
    self.unique_chars_label.pack(anchor=tk.W, pady=(0, 5))

    # Frame para la visualización de distribución
    self.viz_frame = tk.Frame(right_frame, bg=self.styles.COLOR_FONDO)
    self.viz_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    # Crear figura de matplotlib para la visualización
    self.figure = plt.Figure(figsize=(5, 4), dpi=100)
    self.plot = self.figure.add_subplot(111)
    self.canvas = FigureCanvasTkAgg(self.figure, self.viz_frame)
    self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

  def on_key_release(self, event):
    check_numeric_content(self.code_text)

  def analyze_code(self):
    """Analiza el código de cadena ingresado y actualiza la visualización"""
    # Obtener el código ingresado por el usuario
    code = self.code_text.get("1.0", tk.END).strip()

    if not code:
      messagebox.showwarning("Advertencia", "Por favor ingrese un código de cadena para analizar.")
      return

    try:
      # Calcular la entropía
      entropy = calcular_entropia(code)

      # Obtener datos de la cadena
      data = obtener_datos_de_cadena(code)      # Actualizar las etiquetas de estadísticas
      total_len = len(code)
      # Mejorar la representación de la fórmula para que coincida con la imagen
      entropy_formula = f"Entropía = -sum((P_i / total) * log2(P_i / total)) = {entropy:.4f}"
      entropy_i = f"i = 1, 2, ..., {len(data)}"

      # Configurar las etiquetas por separado para asegurar la alineación izquierda
      self.entropy_label.config(text=entropy_formula)
      self.entropy_i_label.config(text=entropy_i)
      self.length_label.config(text=f"Longitud: {total_len}")
      self.unique_chars_label.config(text=f"Caracteres únicos: {len(data)}")

      # Crear visualización de distribución
      self.update_visualization(data, total_len)

    except Exception as e:
      messagebox.showerror("Error", f"Error al analizar el código: {str(e)}")

  def update_visualization(self, data, total_len):
    """Actualiza la visualización de la distribución de caracteres"""
    try:
      # Limpiar el gráfico anterior
      self.plot.clear()

      # Convertir los datos a formato para graficar
      chars = list(data.keys())
      counts = list(data.values())
      probabilities = [count / total_len for count in counts]

      # Crear gráfico de barras
      bars = self.plot.bar(chars, counts, color=self.styles.COLOR_SECUNDARIO)

      # Añadir etiquetas
      self.plot.set_xlabel('Caracteres')
      self.plot.set_ylabel('Frecuencia')
      self.plot.set_title('Distribución de Caracteres')

      # Ajustar el límite y para que no se corten los valores
      max_count = max(counts) if counts else 0
      # Añadir 15% más de espacio arriba    # Añadir valores y probabilidades sobre las barras (en porcentaje)
      self.plot.set_ylim(0, max_count * 1.15)
      for i, bar in enumerate(bars):
        height = bar.get_height()
        prob_percent = probabilities[i] * 100  # Convertir a porcentaje
        prob_text = f"{prob_percent:.1f}%"
        self.plot.text(bar.get_x() + bar.get_width() / 2., height,
                f"{height}\n({prob_text})", ha='center', va='bottom')

      # Refrescar el canvas
      self.figure.tight_layout()
      self.canvas.draw()
    except Exception as e:
      messagebox.showerror("Error", f"Error al generar la visualización: {str(e)}")
