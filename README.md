# BrailleOCR API - Sistema de Traducción PDF a Braille
Este proyecto proporciona una API para convertir documentos PDF a texto mediante OCR y luego traducirlos a Braille, con funcionalidades de autenticación y gestión de usuarios. Esto servirá para enviar esta traducción a un dispositivo externo (en este caso un ESP32).

## Características principales

- Extracción de texto de PDFs mediante OCR (Tesseract)
- Traducción de texto a Braille
- Sistema de autenticación JWT
- Gestión de sesiones de lectura
- Progreso guardado por usuario
- API RESTful organizada en blueprints

## Tecnologías utilizadas

- **Backend Framework:** Flask (Python)
- **OCR:** Tesseract
- **Base de datos:** SQLite
- **Autenticación:** JWT (Flask-JWT-Extended)
- **Procesamiento PDF:** PyPDF2

## Prerrequisitos

- Python 3.11 o superior
- Tesseract OCR
- pip (gestor de paquetes de Python)

## Instalación

### Paso 1: Clonar el repositorio
```bash
git clone https://github.com/Fabo2303/pdf-to-braille-flask.git
cd pdf-to-braille-flask
```

### Paso 2: Crear entorno virtual
```bash
python -m venv venv
```

### Paso 3: Activar entorno virtual
```bash
source venv/bin/activate  # En Linux/Mac
venv\Scripts\activate  # En Windows
```

### Paso 4: Instalar las dependencias:
```bash
pip install -r requirements.txt
```

### Paso 5: Crear un archivo .env y reemplazar los valores por los de tu entorno
```bash
SECRET_KEY=supersecretkey
JWT_SECRET_KEY=superjwtsecret
UPLOAD_FOLDER=uploads
DATABASE_URL=sqlite:///braille.db
FLASK_ENV=development
```

### Paso 6: Instalar Tesseract OCR
- Descargar Tesseract OCR: https://github.com/tesseract-ocr/tesseract.git
- Asegurarse de que Tesseract esté en el PATH de tu sistema.

### Paso 7: Iniciar la aplicación
```bash
python run.py
```

### Paso 8: Acceder a la API
- La API estará disponible en `http://localhost:5000`.

## Endpoints de la API

### POST /api/auth/register
Registra un nuevo usuario.

**Parámetros:**
```json
{
    "username": "nombre_usuario",
    "password": "contraseña_segura"
}
```

**Respuesta:**
```json
{
    "message": "User registered successfully"
}
```

### POST /api/auth/login
Inicia sesión de un usuario.

**Parámetros:**
```json
{
    "username": "nombre_usuario",
    "password": "contraseña_segura"
}
```

**Respuesta:**
```json
{
    "access_token": "token_de_acceso"
}
```

### POST /api/pdf/upload
Sube un archivo PDF para su procesamiento.

**Parámetros:**
```json
{
    "file": "ruta_del_archivo.pdf"
}
```

**Respuesta:**
```json
{
    "message": "File uploaded successfully"
}
```

### GET /api/braille/files
Lista los archivos disponibles en la carpeta uploads/braille.

**Respuesta:**
```json
{
    "files": ["archivo1.txt", "archivo2.txt"]
}
```

### GET /api/braille/read
Lee un archivo braille.

**Parámetros:**
```json
{
    "title": "nombre_archivo",
    "chunk_size": 3
}
```

**Respuesta:**
```json
{
  "title": "nombre_archivo.txt",
  "start": 0,
  "end": 3,
  "chunk": ["000011", "101101", "100111"],
  "done": false
}
```

### Estructura del proyecto

```
pdf-to-braille-flask/
├── 📁 app/
│   ├── 📁 controllers/
│   │   ├── 🐍 auth_controller.py
│   │   ├── 🐍 file_controller.py
│   │   ├── 🐍 main_controller.py
│   │   └── 🐍 pdf_controller.py
│   ├── 📁 models/
│   │   ├── 🐍 user_session.py
│   │   └── 🐍 user.py
│   ├── 📁 routes/
│   │   ├── 🐍 auth_routes.py
│   │   ├── 🐍 file_routes.py
│   │   ├── 🐍 main_routes.py
│   │   └── 🐍 pdf_routes.py
│   ├── 📁 services/
│   │   ├── 🐍 braille_converter.py
│   │   ├── 🐍 file_utils.py
│   │   └── 🐍 pdf_reader.py
│   ├── 📁 templates/
│   │   ├── 🌐 brailletest.html
│   │   └── 🌐 index.html
│   ├── 🐍 __init__.py
│   └── 🐍 extensions.py
├── 📁 instance/
│   └── 🗄️ braille.db
├── 📁 uploads/
│   ├── 📁 braille/
│   │   └── 📝 braille_output.txt
│   ├── 📁 pdf/
│   │   └── 📄 prueba.pdf
│   └── 📁 text/
│   │   └── 📝 texto_extraido.txt
├── ⚙️ .env
├── 🚀 create_db.py
├── 📝 README.md
├── 📦 requirements.txt
└── 🚀 run.py
```

## Consideraciones

### 1. Limitaciones Técnicas
- **Calidad de OCR** depende de:
  - Resolución del PDF (mínimo 300 DPI recomendado)
  - Calidad del escaneo (mejor resultado con texto digital)
  - Idiomas soportados (español/inglés con mejor rendimiento)

- **Tamaño de archivos**:
  - Límite de 10MB por PDF
  - Procesamiento puede ser lento en archivos >5MB