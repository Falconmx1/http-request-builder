# Guía para Contribuidores

¡Gracias por tu interés en contribuir a **HTTP Request Builder**! Toda ayuda es bienvenida.

## 🐛 Reportar Problemas
*   Asegúrate de que el problema no haya sido reportado antes.
*   Usa el [issue tracker](https://github.com/Falconmx1/http-request-builder/issues) para reportar bugs.
*   Incluye pasos detallados para reproducir el problema y la versión de Python que usas.

## 💡 Sugerir Mejoras
*   Abre un issue describiendo la nueva funcionalidad y por qué sería útil.
*   Espera feedback antes de empezar a codificar para alinear expectativas.

## 🔧 Pull Requests
1.  Haz un fork del repositorio.
2.  Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`).
3.  Haz tus cambios y asegúrate de que el código siga el estilo (PEP 8).
4.  Añade o actualiza tests si es necesario.
5.  Haz commit de tus cambios (`git commit -m 'Añade nueva funcionalidad X'`).
6.  Haz push a la rama (`git push origin feature/nueva-funcionalidad`).
7.  Abre un Pull Request contra la rama `main`.

## 📖 Estilo de Código
*   Sigue [PEP 8](https://pep8.org/) para Python.
*   Usa nombres de variables y funciones descriptivos en inglés.
*   Añade docstrings a las funciones y clases nuevas.

## 🧪 Pruebas
Si añades código nuevo, intenta incluir pruebas para él. Puedes ejecutar las pruebas existentes con:
```bash
python -m unittest discover tests
