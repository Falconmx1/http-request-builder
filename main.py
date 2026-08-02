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
from cli.parser import create_parser

def main():
    """Función principal del programa."""
    parser = create_parser()
    args = parser.parse_args()

    # Si no hay argumentos, mostrar ayuda
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    # Preparar los datos si existen
    data = None
    if args.data:
        try:
            # Intentar parsear como JSON
            data = json.loads(args.data)
        except json.JSONDecodeError:
            # Si falla, usarlo como texto plano
            data = args.data

    # Crear y ejecutar la petición
    request = HTTPRequest(
        method=args.method.upper(),
        url=args.url,
        headers=args.headers,
        data=data,
        timeout=args.timeout,
        verify_ssl=not args.no_verify
    )

    response = request.send()

    # Mostrar resultados
    response.display(
        show_headers=args.show_headers,
        show_body=args.show_body,
        verbose=args.verbose
    )

    # Salir con código de estado apropiado para scripting
    if 200 <= response.status_code < 300:
        sys.exit(0)  # Éxito
    else:
        sys.exit(1)  # Error

if __name__ == "__main__":
    main()
