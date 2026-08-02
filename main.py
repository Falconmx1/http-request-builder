#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HTTP Request Builder - Herramienta CLI para probar APIs REST.
Autor: Falconmx1
Licencia: MIT
"""

import sys
import json
from core.request import HTTPRequest
from core.response import HTTPResponse
from cli.parser import create_parser, parse_headers
from utils.file_manager import FileManager

def main():
    """Función principal del programa."""
    parser = create_parser()
    args = parser.parse_args()

    # Si no hay argumentos, mostrar ayuda
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    # Cargar configuración si se especifica
    config = {}
    if args.config:
        config = FileManager.load_config(args.config)

    # Preparar los datos si existen
    data = None
    if args.data:
        try:
            # Intentar parsear como JSON
            data = json.loads(args.data)
        except json.JSONDecodeError:
            # Si falla, usarlo como texto plano
            data = args.data

    # Parsear cabeceras
    headers = parse_headers(args.headers)
    if args.config and 'headers' in config:
        headers.update(config['headers'])

    # Crear y ejecutar la petición
    request = HTTPRequest(
        method=args.method.upper(),
        url=args.url,
        headers=headers,
        data=data,
        timeout=args.timeout,
        verify_ssl=not args.no_verify
    )

    response = request.send()

    # Mostrar resultados
    response.display(
        show_headers=args.show_headers,
        show_body=not args.no_body,
        verbose=args.verbose
    )

    # Guardar resultados si se solicita
    if args.output:
        output_data = {
            'url': args.url,
            'method': args.method,
            'status_code': response.status_code,
            'headers': response.headers,
            'body': response.body,
            'elapsed_time': response.elapsed_time,
            'success': response.success,
            'error': response.error_message if response.error_type else None
        }
        saved_path = FileManager.save_response(
            output_data,
            filename=args.output,
            format=args.output_format
        )
        print(f"💾 Resultados guardados en: {saved_path}")

    # Salir con código de estado apropiado para scripting
    if response.success:
        sys.exit(0)  # Éxito
    else:
        sys.exit(1)  # Error

if __name__ == "__main__":
    main()
