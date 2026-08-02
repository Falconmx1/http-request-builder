# -*- coding: utf-8 -*-

"""
Módulo para configurar el parser de argumentos de la CLI.
"""

import argparse

def create_parser():
    """Crea y configura el parser de argumentos."""
    parser = argparse.ArgumentParser(
        prog="http-request-builder",
        description="Herramienta CLI para probar y depurar APIs REST.",
        epilog="Ejemplo: http-request-builder -m GET -u https://api.github.com/users/octocat",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Argumentos principales
    parser.add_argument(
        "-m", "--method",
        choices=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
        default="GET",
        help="Método HTTP a utilizar (default: GET)"
    )

    parser.add_argument(
        "-u", "--url",
        help="URL del endpoint (ej: https://api.example.com/users)"
    )

    parser.add_argument(
        "-d", "--data",
        help="Datos a enviar en el cuerpo (JSON string o texto plano)"
    )

    parser.add_argument(
        "-H", "--headers",
        action="append",
        help="Cabeceras adicionales en formato 'Clave: Valor' (puede repetirse)"
    )

    # Argumentos de configuración
    parser.add_argument(
        "-c", "--config",
        help="Ruta a archivo de configuración JSON con opciones predeterminadas"
    )

    parser.add_argument(
        "-t", "--timeout",
        type=int,
        default=10,
        help="Tiempo de espera máximo en segundos (default: 10)"
    )

    parser.add_argument(
        "--no-verify",
        action="store_true",
        help="Desactivar verificación SSL (útil para entornos de desarrollo)"
    )

    # Argumentos de salida
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Mostrar información detallada (respuestas completas, más datos)"
    )

    parser.add_argument(
        "--show-headers",
        action="store_true",
        help="Mostrar cabeceras de la respuesta"
    )

    parser.add_argument(
        "--no-body",
        action="store_true",
        help="Ocultar el cuerpo de la respuesta"
    )

    parser.add_argument(
        "-o", "--output",
        help="Guardar respuesta en archivo (especificar nombre)"
    )

    parser.add_argument(
        "--output-format",
        choices=["json", "txt", "html"],
        default="json",
        help="Formato del archivo de salida (default: json)"
    )

    # Reportes
    parser.add_argument(
        "-r", "--report",
        help="Generar reporte HTML con los resultados (especificar nombre del archivo)"
    )

    # CI/CD
    parser.add_argument(
        "--ci",
        action="store_true",
        help="Activar modo CI/CD para integración con pipelines"
    )

    parser.add_argument(
        "--ci-config",
        help="Ejecutar pruebas desde archivo de configuración (modo CI/CD)"
    )

    return parser

def parse_headers(headers_list):
    """
    Convierte una lista de strings 'Clave: Valor' a un diccionario.

    Args:
        headers_list (list): Lista de cabeceras en formato string.

    Returns:
        dict: Diccionario de cabeceras.
    """
    if not headers_list:
        return {}

    headers = {}
    for header in headers_list:
        try:
            key, value = header.split(":", 1)
            headers[key.strip()] = value.strip()
        except ValueError:
            print(f"⚠️  Advertencia: Cabecera mal formada: '{header}'. Se ignorará.")

    return headers
