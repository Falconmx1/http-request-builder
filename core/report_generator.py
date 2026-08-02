# -*- coding: utf-8 -*-

"""
Módulo para generar reportes HTML de las pruebas realizadas.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class ReportGenerator:
    """Clase para generar reportes HTML de resultados de pruebas."""

    def __init__(self, output_dir="reports"):
        """
        Inicializa el generador de reportes.

        Args:
            output_dir (str): Directorio donde guardar los reportes.
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_report(self, results: List[Dict[str, Any]], filename: str = None) -> str:
        """
        Genera un reporte HTML a partir de los resultados.

        Args:
            results (list): Lista de diccionarios con resultados de pruebas.
            filename (str, optional): Nombre del archivo.

        Returns:
            str: Ruta del reporte generado.
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}.html"

        filepath = self.output_dir / filename

        # Generar estadísticas
        stats = self._calculate_stats(results)

        # Crear HTML
        html_content = self._create_html(results, stats)

        # Guardar
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return str(filepath)

    def _calculate_stats(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calcula estadísticas de los resultados."""
        total = len(results)
        successful = sum(1 for r in results if r.get('success', False))
        failed = total - successful
        success_rate = (successful / total * 100) if total > 0 else 0

        # Tiempos de respuesta
        times = [r.get('elapsed_time', 0) for r in results if r.get('elapsed_time')]
        avg_time = sum(times) / len(times) if times else 0
        max_time = max(times) if times else 0
        min_time = min(times) if times else 0

        return {
            'total': total,
            'successful': successful,
            'failed': failed,
            'success_rate': success_rate,
            'avg_time': avg_time,
            'max_time': max_time,
            'min_time': min_time
        }

    def _create_html(self, results: List[Dict[str, Any]], stats: Dict[str, Any]) -> str:
        """Crea el contenido HTML del reporte."""
        # Estilos CSS embebidos
        css = """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: #f4f6f9;
            padding: 20px;
            color: #333;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
        }
        .header h1 { font-size: 2.5rem; margin-bottom: 10px; }
        .header .subtitle { opacity: 0.9; font-size: 1.1rem; }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            text-align: center;
        }
        .stat-card .number {
            font-size: 2.5rem;
            font-weight: bold;
            color: #667eea;
        }
        .stat-card .label { font-size: 0.9rem; color: #666; margin-top: 5px; }
        .stat-card.success .number { color: #10b981; }
        .stat-card.failed .number { color: #ef4444; }
        .stat-card.rate .number { color: #f59e0b; }
        .stat-card.time .number { color: #3b82f6; }
        .test-table {
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        }
        .test-table table { width: 100%; border-collapse: collapse; }
        .test-table th {
            background: #f8fafc;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            color: #475569;
            border-bottom: 2px solid #e2e8f0;
        }
        .test-table td { padding: 15px; border-bottom: 1px solid #e2e8f0; }
        .test-table tr:hover { background: #f8fafc; }
        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }
        .status-badge.success { background: #d1fae5; color: #065f46; }
        .status-badge.failed { background: #fee2e2; color: #991b1b; }
        .response-details {
            max-width: 300px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            font-size: 0.85rem;
            color: #64748b;
        }
        .timestamp { color: #94a3b8; font-size: 0.85rem; }
        @media (max-width: 768px) {
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
            .header h1 { font-size: 1.8rem; }
            .test-table { overflow-x: auto; }
        }
        """

        # Construir filas de la tabla
        rows = ""
        for result in results:
            status_class = "success" if result.get('success', False) else "failed"
            status_text = "✅ Éxito" if result.get('success', False) else "❌ Fallo"
            status_code = result.get('status_code', 'N/A')
            method = result.get('method', 'GET')
            url = result.get('url', '')
            elapsed = f"{result.get('elapsed_time', 0):.3f}s" if result.get('elapsed_time') else 'N/A'
            timestamp = result.get('timestamp', datetime.now().isoformat())

            rows += f"""
            <tr>
                <td><span class="status-badge {status_class}">{status_text}</span></td>
                <td><strong>{method}</strong></td>
                <td style="max-width: 300px; overflow: hidden; text-overflow: ellipsis;">{url}</td>
                <td>{status_code}</td>
                <td>{elapsed}</td>
                <td class="response-details">{result.get('body_preview', '')[:100]}</td>
                <td class="timestamp">{timestamp[:19]}</td>
            </tr>
            """

        # Construir HTML completo
        html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reporte de Pruebas HTTP</title>
            <style>{css}</style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 HTTP Request Builder</h1>
                    <div class="subtitle">Reporte de Pruebas - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
                </div>

                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="number">{stats['total']}</div>
                        <div class="label">Total Pruebas</div>
                    </div>
                    <div class="stat-card success">
                        <div class="number">{stats['successful']}</div>
                        <div class="label">✅ Exitosas</div>
                    </div>
                    <div class="stat-card failed">
                        <div class="number">{stats['failed']}</div>
                        <div class="label">❌ Fallidas</div>
                    </div>
                    <div class="stat-card rate">
                        <div class="number">{stats['success_rate']:.1f}%</div>
                        <div class="label">Tasa de Éxito</div>
                    </div>
                    <div class="stat-card time">
                        <div class="number">{stats['avg_time']:.3f}s</div>
                        <div class="label">⏱️ Tiempo Promedio</div>
                    </div>
                </div>

                <div class="test-table">
                    <table>
                        <thead>
                            <tr>
                                <th>Estado</th>
                                <th>Método</th>
                                <th>URL</th>
                                <th>Código</th>
                                <th>Tiempo</th>
                                <th>Respuesta</th>
                                <th>Fecha</th>
                            </tr>
                        </thead>
                        <tbody>
                            {rows}
                        </tbody>
                    </table>
                </div>

                <div style="text-align: center; margin-top: 30px; color: #94a3b8; font-size: 0.85rem;">
                    Generado por HTTP Request Builder v0.1.0
                </div>
            </div>
        </body>
        </html>
        """

        return html

    def generate_from_file(self, results_file: str, filename: str = None) -> str:
        """
        Genera un reporte HTML a partir de un archivo JSON de resultados.

        Args:
            results_file (str): Ruta al archivo JSON con resultados.
            filename (str, optional): Nombre del archivo de salida.

        Returns:
            str: Ruta del reporte generado.
        """
        try:
            with open(results_file, 'r', encoding='utf-8') as f:
                results = json.load(f)

            if isinstance(results, dict):
                results = [results]

            return self.generate_report(results, filename)

        except Exception as e:
            print(f"❌ Error al generar reporte desde archivo: {e}")
            return ""
