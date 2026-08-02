# -*- coding: utf-8 -*-

"""
Módulo para integración con sistemas de CI/CD.
"""

import json
import os
import sys
from typing import Dict, List, Any, Optional
from pathlib import Path

class CICDIntegration:
    """Clase para manejar integración con sistemas CI/CD."""

    @staticmethod
    def detect_environment() -> str:
        """
        Detecta el entorno de CI/CD actual.

        Returns:
            str: Nombre del entorno ('github_actions', 'jenkins', 'gitlab_ci', 'local')
        """
        # GitHub Actions
        if os.getenv('GITHUB_ACTIONS') == 'true':
            return 'github_actions'
        # Jenkins
        if os.getenv('JENKINS_HOME'):
            return 'jenkins'
        # GitLab CI
        if os.getenv('GITLAB_CI') == 'true':
            return 'gitlab_ci'
        return 'local'

    @staticmethod
    def format_output(results: List[Dict[str, Any]], format_type: str = 'json') -> str:
        """
        Formatea los resultados para diferentes sistemas de CI/CD.

        Args:
            results (list): Lista de resultados.
            format_type (str): Tipo de formato ('json', 'junit', 'github_actions').

        Returns:
            str: Resultados formateados.
        """
        if format_type == 'github_actions':
            return CICDIntegration._format_github_actions(results)
        elif format_type == 'junit':
            return CICDIntegration._format_junit(results)
        else:
            return json.dumps(results, indent=2)

    @staticmethod
    def _format_github_actions(results: List[Dict[str, Any]]) -> str:
        """Formatea resultados para GitHub Actions con anotaciones."""
        output = []
        total = len(results)
        failed = sum(1 for r in results if not r.get('success', False))

        # Resumen
        output.append(f"::notice title=HTTP Test Summary::Total: {total}, Failed: {failed}")

        # Anotaciones por prueba fallida
        for result in results:
            if not result.get('success', False):
                url = result.get('url', 'unknown')
                method = result.get('method', 'GET')
                status = result.get('status_code', 'N/A')
                error = result.get('error', 'Unknown error')
                output.append(f"::error title=Test Failed::{method} {url} - Status: {status} - {error}")

        # Métricas para GitHub Actions
        success_rate = ((total - failed) / total * 100) if total > 0 else 0
        output.append(f"::set-output name=success_rate::{success_rate:.2f}")
        output.append(f"::set-output name=total_tests::{total}")
        output.append(f"::set-output name=failed_tests::{failed}")

        # Guardar resultados en archivo para pasos posteriores
        with open('test_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        output.append("::notice::Resultados guardados en test_results.json")

        return "\n".join(output)

    @staticmethod
    def _format_junit(results: List[Dict[str, Any]]) -> str:
        """Formatea resultados en formato JUnit XML para Jenkins y otras herramientas."""
        import xml.etree.ElementTree as ET
        from datetime import datetime

        testsuite = ET.Element('testsuite')
        testsuite.set('name', 'HTTP Request Builder Tests')
        testsuite.set('timestamp', datetime.now().isoformat())
        testsuite.set('tests', str(len(results)))

        failed = sum(1 for r in results if not r.get('success', False))
        testsuite.set('failures', str(failed))

        for result in results:
            testcase = ET.SubElement(testsuite, 'testcase')
            testcase.set('name', f"{result.get('method', 'GET')} {result.get('url', '')}")
            testcase.set('classname', 'HTTPRequestBuilder')

            if not result.get('success', False):
                failure = ET.SubElement(testcase, 'failure')
                failure.set('type', 'AssertionError')
                failure.text = f"Status: {result.get('status_code', 'N/A')} - {result.get('error', 'Unknown error')}"

            # Añadir tiempo
            elapsed = result.get('elapsed_time', 0)
            testcase.set('time', f"{elapsed:.3f}")

        return ET.tostring(testsuite, encoding='unicode', method='xml')

    @staticmethod
    def exit_code(results: List[Dict[str, Any]]) -> int:
        """
        Determina el código de salida basado en los resultados.

        Args:
            results (list): Lista de resultados.

        Returns:
            int: Código de salida (0 = éxito, 1 = fallo)
        """
        # Si hay algún fallo, devolver 1
        for result in results:
            if not result.get('success', False):
                return 1
        return 0

    @staticmethod
    def run_tests_from_config(config_file: str, report_path: str = None) -> Dict[str, Any]:
        """
        Ejecuta pruebas desde un archivo de configuración y genera reportes.

        Args:
            config_file (str): Ruta al archivo de configuración.
            report_path (str, optional): Ruta para guardar el reporte.

        Returns:
            dict: Resultados de las pruebas.
        """
        from core.request import HTTPRequest
        from core.report_generator import ReportGenerator

        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            requests_config = config.get('requests', [])
            results = []

            for req_config in requests_config:
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

            # Generar reporte HTML
            if report_path:
                generator = ReportGenerator()
                report_file = generator.generate_report(results, report_path)
                print(f"📊 Reporte generado: {report_file}")

            return {'results': results, 'total': len(results)}

        except Exception as e:
            print(f"❌ Error al ejecutar pruebas: {e}")
            return {'results': [], 'total': 0}
