# -*- coding: utf-8 -*-

"""
Módulo para manejar respuestas HTTP.
"""

import json
import sys
from datetime import datetime

class HTTPResponse:
    """Clase para encapsular y mostrar una respuesta HTTP."""

    def __init__(self, response=None, elapsed_time=0.0, error_type=None, error_message=None):
        """
        Inicializa una respuesta, ya sea desde una petición exitosa o un error.

        Args:
            response (requests.Response, optional): Objeto de respuesta de requests.
            elapsed_time (float): Tiempo que tardó la petición.
            error_type (str, optional): Tipo de error si ocurrió.
            error_message (str, optional): Mensaje de error.
        """
        self.status_code = getattr(response, 'status_code', None) if response else None
        self.headers = dict(getattr(response, 'headers', {})) if response else {}
        self.body = getattr(response, 'text', None) if response else None
        self.elapsed_time = elapsed_time
        self.error_type = error_type
        self.error_message = error_message
        self.success = error_type is None and response and 200 <= self.status_code < 300

        # Intentar parsear JSON si es aplicable
        self.json_body = None
        if self.body and 'application/json' in self.headers.get('Content-Type', ''):
            try:
                self.json_body = json.loads(self.body)
            except:
                pass

    @classmethod
    def error(cls, error_type, error_message):
        """Crea una respuesta de error."""
        return cls(error_type=error_type, error_message=error_message)

    def display(self, show_headers=False, show_body=True, verbose=False):
        """Muestra la respuesta en consola con colores básicos."""
        # Colores ANSI para terminal
        GREEN = '\033[92m'
        RED = '\033[91m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        RESET = '\033[0m'
        BOLD = '\033[1m'

        # Cabecera de la respuesta
        print("\n" + "=" * 60)
        print(f"{BOLD}RESPUESTA HTTP{RESET}")
        print("=" * 60)

        # Mostrar estado
        if self.error_type:
            print(f"{RED}❌ ERROR: {self.error_type}{RESET}")
            print(f"   {self.error_message}")
        else:
            color = GREEN if self.success else RED
            status_text = "✅ ÉXITO" if self.success else "❌ FALLO"
            print(f"{color}{BOLD}Estado: {self.status_code} - {status_text}{RESET}")
            print(f"{BOLD}Tiempo:{RESET} {self.elapsed_time:.4f} segundos")

        # Mostrar cabeceras
        if show_headers or verbose:
            print(f"\n{BOLD}📋 Cabeceras:{RESET}")
            if self.headers:
                for key, value in self.headers.items():
                    print(f"  {BLUE}{key}{RESET}: {value}")
            else:
                print("  (Sin cabeceras)")

        # Mostrar cuerpo de la respuesta
        if show_body and not self.error_type:
            print(f"\n{BOLD}📦 Cuerpo:{RESET}")
            if self.json_body is not None:
                # Mostrar JSON formateado
                print(json.dumps(self.json_body, indent=2, ensure_ascii=False))
            elif self.body:
                # Truncar si es muy largo
                body_preview = self.body
                if len(body_preview) > 2000 and not verbose:
                    body_preview = body_preview[:2000] + "\n... (truncado, usa --verbose para ver completo)"
                print(body_preview)
            else:
                print("  (Cuerpo vacío)")

        print("\n" + "=" * 60 + "\n")
