# -*- coding: utf-8 -*-

"""
Tests básicos para verificar la instalación.
"""

import unittest
import sys
import os

class TestInstallation(unittest.TestCase):
    """Pruebas básicas de instalación."""

    def test_imports(self):
        """Verificar que todos los módulos se importan correctamente."""
        try:
            import core
            import cli
            import utils
            import ci
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Error de importación: {e}")

    def test_requests_installed(self):
        """Verificar que requests está instalado."""
        try:
            import requests
            self.assertTrue(True)
        except ImportError:
            self.fail("Requests no está instalado")

    def test_python_version(self):
        """Verificar versión de Python."""
        version = sys.version_info
        self.assertGreaterEqual(version.major, 3)
        self.assertGreaterEqual(version.minor, 6)

if __name__ == '__main__':
    unittest.main()
