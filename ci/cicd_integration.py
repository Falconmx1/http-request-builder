# -*- coding: utf-8 -*-

"""
Módulo para integración con sistemas de CI/CD.
"""

import json
import os
import sys
from typing import Dict, List, Any
from pathlib import Path

class CICDIntegration:
    """Clase para manejar integración con sistemas CI/CD."""

    @staticmethod
    def detect_environment() -> str:
        """Detecta el entorno de CI/CD actual."""
        if os.getenv('GITHUB_ACTIONS') == 'true':
            return 'github_actions'
        if os.getenv('JENKINS_HOME'):
            return 'jenkins'
        if os.getenv('GITLAB_CI') == 'true':
            return 'gitlab_ci'
        return 'local'

    @staticmethod
    def run_tests_from_config(config_file: str, report_path: str = None) -> Dict[str, Any]:
        """
        Ejecuta pruebas desde un archivo de configuración.

        Args:
            config_file (str): Ruta al archivo de configuración.
            report_path (str, optional): Ruta para guardar el reporte.

        Returns:
            dict: Resultados de las pruebas.
        """
        try:
            # Asegurar que existe el archivo
            if not os.path.exists(config_file):
                print(f"❌ Archivo de configuración no encontrado: {config_file}")
                return {'results': [], 'total': 0}

            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            requests_config = config.get('requests', [])
            results = []

            # Intentar importar core
            try:
                from core.request import HTTPRequest
                from core.report_generator import ReportGenerator
            except ImportError as e:
                print(f"❌ Error de importación: {e}")
                return {'results': [], 'total': 0}

            for req_config in requests_config:
                try:
                    request = HTTPRequest(
                        method=req_config.get('method', 'GET'),
                        url=req_config.get('url', ''),
                        headers=req_config.get('headers', {}),
                        data=req_config.get('data'),
                        timeout=req_config.get('timeout', 10),
                        verify_ssl=not req_config.get('no_verify', False)
                    )

                    response = request.send()
                    results.append({
                        'method': req_config.get('method', 'GET'),
                        'url': req_config.get('url', ''),
                        'status_code': response.status_code,
                        'success': response.success,
                        'elapsed_time': response.elapsed_time,
                        'error': response.error_message if response.error_type else None,
                        'body_preview': (response.body[:200] + '...') if response.body and len(response.body) > 200 else response.body,
                        'timestamp': __import__('datetime').datetime.now().isoformat()
                    })
                except Exception as e:
                    results.append({
                        'method': req_config.get('method', 'GET'),
                        'url': req_config.get('url', ''),
                        'status_code': None,
                        'success': False,
                        'elapsed_time': 0,
                        'error': str(e),
                        'body_preview': '',
                        'timestamp': __import__('datetime').datetime.now().isoformat()
                    })

            # Generar reporte HTML
            if report_path:
                try:
                    generator = ReportGenerator()
                    report_file = generator.generate_report(results, report_path)
                    print(f"📊 Reporte generado: {report_file}")
                except Exception as e:
                    print(f"⚠️ Error al generar reporte: {e}")

            return {'results': results, 'total': len(results)}

        except Exception as e:
            print(f"❌ Error al ejecutar pruebas: {e}")
            return {'results': [], 'total': 0}

    @staticmethod
    def exit_code(results: List[Dict[str, Any]]) -> int:
        """
        Determina el código de salida basado en los resultados.
        """
        for result in results:
            if not result.get('success', False):
                return 1
        return 0
