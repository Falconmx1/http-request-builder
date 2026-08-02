# -*- coding: utf-8 -*-

"""
Tests básicos para verificar la funcionalidad.
"""

import unittest
import sys
import os

# Añadir el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestBasicFunctionality(unittest.TestCase):
    """Pruebas básicas de funcionalidad."""

    def test_imports(self):
        """Verificar importaciones."""
        import core
        import cli
        import utils
        self.assertTrue(True)

    def test_http_request_import(self):
        """Verificar importación de HTTPRequest."""
        from core.request import HTTPRequest
        self.assertIsNotNone(HTTPRequest)

    def test_http_response_import(self):
        """Verificar importación de HTTPResponse."""
        from core.response import HTTPResponse
        self.assertIsNotNone(HTTPResponse)

if __name__ == '__main__':
    unittest.main()
