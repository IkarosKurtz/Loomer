# filepath: d:\Projects\Loomer\main.py
"""
Entry point for Loomer application - a tool for chain code processing
"""
import tkinter as tk
from src.loomer.app import LoomerApp


def main():
  """Initialize and run the Loomer application"""
  root = tk.Tk()
  app = LoomerApp(root)
  root.mainloop()


if __name__ == "__main__":
  main()
