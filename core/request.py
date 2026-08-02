# -*- coding: utf-8 -*-

"""
Módulo para manejar peticiones HTTP.
"""

import requests
import time
from core.response import HTTPResponse

class HTTPRequest:
    """Clase para construir y ejecutar peticiones HTTP."""

    def __init__(self, method, url, headers=None, data=None, timeout=10, verify_ssl=True):
        """
        Inicializa una nueva petición.

        Args:
            method (str): Método HTTP (GET, POST, etc.)
            url (str): URL del endpoint.
            headers (dict, optional): Cabeceras HTTP.
            data (dict/str, optional): Cuerpo de la petición.
            timeout (int, optional): Tiempo de espera en segundos.
            verify_ssl (bool, optional): Verificar certificados SSL.
        """
        self.method = method.upper()
        self.url = url
        self.headers = headers or {}
        self.data = data
        self.timeout = timeout
        self.verify_ssl = verify_ssl

    def send(self):
        """
        Envía la petición HTTP.

        Returns:
            HTTPResponse: Objeto con la respuesta del servidor.
        """
        start_time = time.time()

        try:
            # Elegir el método HTTP apropiado
            if self.method == "GET":
                response = requests.get(
                    self.url,
                    headers=self.headers,
                    timeout=self.timeout,
                    verify=self.verify_ssl
                )
            elif self.method == "POST":
                response = requests.post(
                    self.url,
                    headers=self.headers,
                    json=self.data if isinstance(self.data, dict) else None,
                    data=self.data if not isinstance(self.data, dict) else None,
                    timeout=self.timeout,
                    verify=self.verify_ssl
                )
            elif self.method == "PUT":
                response = requests.put(
                    self.url,
                    headers=self.headers,
                    json=self.data if isinstance(self.data, dict) else None,
                    data=self.data if not isinstance(self.data, dict) else None,
                    timeout=self.timeout,
                    verify=self.verify_ssl
                )
            elif self.method == "DELETE":
                response = requests.delete(
                    self.url,
                    headers=self.headers,
                    timeout=self.timeout,
                    verify=self.verify_ssl
                )
            else:
                # Para otros métodos (PATCH, HEAD, etc.)
                response = requests.request(
                    self.method,
                    self.url,
                    headers=self.headers,
                    json=self.data if isinstance(self.data, dict) else None,
                    data=self.data if not isinstance(self.data, dict) else None,
                    timeout=self.timeout,
                    verify=self.verify_ssl
                )

            elapsed_time = time.time() - start_time
            return HTTPResponse(response, elapsed_time)

        except requests.exceptions.Timeout:
            return HTTPResponse.error("Timeout", f"La petición excedió el tiempo límite de {self.timeout}s")
        except requests.exceptions.ConnectionError:
            return HTTPResponse.error("ConnectionError", "No se pudo establecer conexión con el servidor")
        except requests.exceptions.SSLError:
            return HTTPResponse.error("SSLError", "Error de verificación SSL. Usa --no-verify para ignorar.")
        except Exception as e:
            return HTTPResponse.error("Error", str(e))
