# -*- coding: utf-8 -*-

"""
Módulo para manejar archivos (guardar resultados, cargar configuraciones).
"""

import json
import os
from datetime import datetime
from pathlib import Path

class FileManager:
    """Clase para manejar operaciones con archivos."""

    @staticmethod
    def save_response(data, filename=None, format='json'):
        """
        Guarda una respuesta HTTP en un archivo.

        Args:
            data (dict): Datos a guardar.
            filename (str, optional): Nombre del archivo. Si es None, se genera automáticamente.
            format (str): Formato de salida ('json', 'txt', 'html').

        Returns:
            str: Ruta del archivo guardado.
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"response_{timestamp}.{format}"

        # Crear directorio de salida si no existe
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        filepath = output_dir / filename

        if format == 'json':
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        elif format == 'txt':
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(data))
        else:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(data))

        return str(filepath)

    @staticmethod
    def load_config(filepath):
        """
        Carga una configuración desde un archivo JSON.

        Args:
            filepath (str): Ruta al archivo de configuración.

        Returns:
            dict: Configuración cargada.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            print(f"❌ Error: El archivo {filepath} no tiene un formato JSON válido.")
            return {}

    @staticmethod
    def save_config(config, filepath):
        """
        Guarda una configuración en un archivo JSON.

        Args:
            config (dict): Configuración a guardar.
            filepath (str): Ruta donde guardar.

        Returns:
            bool: True si se guardó correctamente.
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error al guardar configuración: {e}")
            return False
