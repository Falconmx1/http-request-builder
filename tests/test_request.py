# -*- coding: utf-8 -*-

"""
Tests para el módulo de peticiones HTTP.
"""

import unittest
from unittest.mock import patch, Mock
from core.request import HTTPRequest
from core.response import HTTPResponse

class TestHTTPRequest(unittest.TestCase):
    """Pruebas para la clase HTTPRequest."""

    @patch('core.request.requests.get')
    def test_get_request(self, mock_get):
        """Prueba una petición GET exitosa."""
        # Configurar mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '{"status": "ok"}'
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_get.return_value = mock_response

        # Ejecutar
        request = HTTPRequest('GET', 'https://api.example.com/test')
        response = request.send()

        # Verificar
        self.assertTrue(response.success)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.body, '{"status": "ok"}')
        mock_get.assert_called_once_with(
            'https://api.example.com/test',
            headers={},
            timeout=10,
            verify=True
        )

    @patch('core.request.requests.post')
    def test_post_with_json(self, mock_post):
        """Prueba una petición POST con datos JSON."""
        # Configurar mock
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.text = '{"id": 1}'
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_post.return_value = mock_response

        # Ejecutar
        data = {"name": "Test"}
        request = HTTPRequest('POST', 'https://api.example.com/users', data=data)
        response = request.send()

        # Verificar
        self.assertTrue(response.success)
        self.assertEqual(response.status_code, 201)
        mock_post.assert_called_once_with(
            'https://api.example.com/users',
            headers={},
            json=data,
            data=None,
            timeout=10,
            verify=True
        )

    @patch('core.request.requests.get')
    def test_timeout_error(self, mock_get):
        """Prueba manejo de timeout."""
        # Configurar mock para lanzar timeout
        import requests
        mock_get.side_effect = requests.exceptions.Timeout

        # Ejecutar
        request = HTTPRequest('GET', 'https://api.example.com/slow')
        response = request.send()

        # Verificar
        self.assertFalse(response.success)
        self.assertEqual(response.error_type, 'Timeout')
        self.assertIn('tiempo límite', response.error_message)

if __name__ == '__main__':
    unittest.main()
