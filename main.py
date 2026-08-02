#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HTTP Request Builder - Herramienta CLI para probar APIs REST.
Autor: Falconmx1
Licencia: MIT
"""

import sys
import json
import os
from datetime import datetime

# Añadir el directorio actual al path para importaciones
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.request import HTTPRequest
from core.response import HTTPResponse
from cli.parser import create_parser, parse_headers
from utils.file_manager import FileManager
from core.report_generator import ReportGenerator
from ci.cicd_integration import CICDIntegration

def main():
    """Función principal del programa."""
    parser = create_parser()
    args = parser.parse_args()

    # Si no hay argumentos, mostrar ayuda
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    # Modo CI/CD: ejecutar pruebas desde archivo de configuración
    if args.ci_config:
        results = CICDIntegration.run_tests_from_config(
            args.ci_config,
            args.report
        )
        exit_code = CICDIntegration.exit_code(results.get('results', []))
        sys.exit(exit_code)

    # Detectar entorno CI/CD
    env = CICDIntegration.detect_environment()
    if args.ci:
        print(f"🔧 Entorno CI/CD detectado: {env}")

    # Cargar configuración si se especifica
    config = {}
    if args.config:
        config = FileManager.load_config(args.config)

    # Si no hay URL, mostrar ayuda
    if not args.url:
        parser.print_help()
        sys.exit(1)

    # Preparar los datos si existen
    data = None
    if args.data:
        try:
            data = json.loads(args.data)
        except json.JSONDecodeError:
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

    # Preparar resultado para reportes
    result_data = {
        'method': args.method.upper(),
        'url': args.url,
        'status_code': response.status_code,
        'success': response.success,
        'elapsed_time': response.elapsed_time,
        'error': response.error_message if response.error_type else None,
        'body_preview': (response.body[:200] + '...') if response.body and len(response.body) > 200 else response.body,
        'timestamp': datetime.now().isoformat()
    }

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

    # Generar reporte HTML si se solicita
    if args.report:
        generator = ReportGenerator()
        report_file = generator.generate_report([result_data], args.report)
        print(f"📊 Reporte HTML generado: {report_file}")

    # Salir con código apropiado
    if response.success:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
