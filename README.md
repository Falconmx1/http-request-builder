# HTTP Request Builder

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Herramienta CLI para probar, depurar y monitorear APIs REST desde la línea de comandos. Ideal para desarrollo, testing e integración de servicios web.

## 🚀 Características

*   **Pruebas de APIs**: Realiza peticiones HTTP (GET, POST, PUT, DELETE, etc.) y valida respuestas.
*   **Depuración**: Visualiza cabeceras, códigos de estado y tiempos de respuesta.
*   **Automatización**: Ideal para scripting y pipelines de integración continua.
*   **Monitoreo**: Verifica la disponibilidad y salud de tus servicios.
*   **Análisis**: Filtra y analiza respuestas JSON/HTML.
*   **Línea de comandos**: Simple y potente, sin dependencias pesadas.

## 📦 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/Falconmx1/http-request-builder.git
cd http-request-builder

# (Opcional) Crear un entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

🛠️ Uso Básico
# Realizar una petición GET
python main.py --method GET --url https://api.github.com/users/octocat

# Enviar datos JSON con POST
python main.py --method POST --url https://httpbin.org/post --data '{"nombre": "Ejemplo"}'

# Ver ayuda completa
python main.py --help

📋 Ejemplos de Comandos
Comando                                                                                     Descripción
python main.py -m GET -u https://api.example.com/users                                      Obtener lista de usuarios.
python main.py -m POST -u https://api.example.com/users -d '{"name":"John"}'                Crear un nuevo usuario.
python main.py -m PUT -u https://api.example.com/users/1 -d '{"name":"Jane"}'               Actualizar usuario.
python main.py -m DELETE -u https://api.example.com/users/1                                 Eliminar usuario.

🤝 Contribuciones
¡Las contribuciones son bienvenidas! Por favor, lee CONTRIBUTING.md para más detalles.

📄 Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más información.
