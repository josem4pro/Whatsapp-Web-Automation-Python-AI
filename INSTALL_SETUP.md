# 📦 WhatsApp Web Automation - Guía de Instalación

**Estado**: ✅ Instalación completada y probada

## 🎯 Qué hace este proyecto

Automatiza la extracción de mensajes de WhatsApp Web usando Python y Selenium:
- Extrae mensajes de un chat específico
- Clasifica mensajes por tipo (texto, imagen, video, audio, archivo)
- Guarda los datos en formato JSON
- Permite seguimiento incremental (solo nuevos mensajes)
- Compatible con integración futura de OpenAI para respuestas automáticas

**⚠️ Importante**: WhatsApp prohíbe sistemas automatizados. Úsalo responsablemente y solo para propósitos personales/educativos.

---

## ✅ Instalación (YA COMPLETADA)

Se realizaron los siguientes pasos:

### 1. Python y Dependencias
- ✅ Python 3.12.3 detectado
- ✅ Entorno virtual (`venv`) creado
- ✅ Todas las dependencias instaladas:
  - `selenium==4.21.0` - Automatización web
  - `webdriver-manager==4.0.2` - Descarga automática de ChromeDriver
  - `openai==0.27.0` - Integración con ChatGPT
  - `mysql-connector-python==8.0.33` - Base de datos MySQL (opcional)
  - `pydub==0.25.1` - Procesamiento de audio (opcional)

### 2. Chrome y ChromeDriver
- ✅ Chrome 142.0.7444.175 instalado
- ✅ ChromeDriver 142 descargado automáticamente por webdriver-manager
- ✅ Ubicación: `/home/jose/.wdm/drivers/chromedriver/linux64/142.0.7444.175/`

### 3. Mejoras Realizadas
- ✅ `main.py` actualizado para usar `webdriver-manager`
- ✅ Ya no necesitas descargar manualmente ChromeDriver
- ✅ La carpeta `./chrome/userdata` se crea automáticamente
- ✅ Mejor manejo de errores al iniciar el navegador
- ✅ Script de prueba (`test_setup.py`) para validar la instalación

---

## 🚀 Cómo Usar

### Paso 1: Activar el Entorno Virtual

```bash
cd /home/jose/Repositorios/Whatsapp-Web-Automation-Python-AI
source venv/bin/activate
```

### Paso 2: Configurar el Script (main.py)

Abre `main.py` y edita estas líneas (al inicio del archivo):

```python
CHAT_NAME = "Mario Rossi"          # Cambia al nombre del contacto deseado
LANGUAGE = 'italian'                # O 'english' si prefieres inglés
DEFAULT_MONTHS_TO_EXTRACT = 1       # Meses hacia atrás a extraer
WAIT_TIME = 30                      # Segundos a esperar por elementos
```

**Ejemplo**: Si quieres extraer mensajes de "Juan Pérez":
```python
CHAT_NAME = "Juan Pérez"
LANGUAGE = 'italian'  # Mantén el idioma configurado en tu WhatsApp Web
```

### Paso 3: Ejecutar el Script

```bash
python main.py
```

**Lo que sucede**:
1. Se abre Chrome automáticamente
2. Se navega a https://web.whatsapp.com/
3. Verás un código QR (código de escaneo)
4. **Abre WhatsApp en tu celular** → Configuración → Dispositivos conectados → Escanea el código QR
5. Una vez autenticado, el script comienza a extraer mensajes
6. Los mensajes se guardan en `messages.json`

### Paso 4: Ver los Mensajes Extraídos

Los mensajes se guardan en `messages.json` con esta estructura:

```json
[
    {
        "id": "hash_único_del_mensaje",
        "type": "Text",
        "message_dir": "In",
        "date": "15/12/2024",
        "time": "14:30",
        "datetime": "15/12/2024 14:30",
        "text": "Contenido del mensaje"
    },
    {
        "id": "...",
        "type": "Image",
        "message_dir": "Out",
        "date": "15/12/2024",
        "time": "14:35",
        "datetime": "15/12/2024 14:35",
        "image_src": "url_de_la_imagen"
    }
]
```

**Tipos de mensajes detectados**:
- `Text` - Texto simple
- `Image` - Imagen
- `Image and text together` - Imagen con texto
- `Video` - Video
- `Video and text together` - Video con texto
- `Voice` - Nota de voz
- `File` - Archivo
- `Referred Text` - Respuesta a un mensaje
- `Deleted` - Mensaje eliminado

---

## 🧪 Prueba de Instalación

Para verificar que todo está correctamente configurado:

```bash
python test_setup.py
```

Este script verifica:
- Python 3.8+
- Todos los paquetes instalados
- Chrome instalado
- ChromeDriver descargado
- Conexión Chrome + Selenium

---

## 📋 Cambios que Hice

### 1. **Automatización de ChromeDriver**
```python
# ANTES: Necesitabas descargar manualmente
driver_location = os.path.join(directory_path, 'chrome', 'chromedriver')
service = webdriver.chrome.service.Service(driver_location)

# AHORA: webdriver-manager lo descarga automáticamente
from webdriver_manager.chrome import ChromeDriverManager
service = Service(ChromeDriverManager().install())
```

### 2. **Mejor Manejo de Errores**
```python
try:
    browser = webdriver.Chrome(service=service, options=options)
    print("Chrome browser started successfully")
except Exception as e:
    print(f"Error starting Chrome browser: {e}")
    raise
```

### 3. **Creación Automática de Carpetas**
```python
os.makedirs(userdata_path, exist_ok=True)  # Sin errores si ya existe
```

### 4. **Script de Prueba**
Nuevo archivo `test_setup.py` que valida toda la instalación.

---

## 🔧 Troubleshooting

### Error: "Chrome not found"
```bash
# En Ubuntu/Debian
sudo apt-get install google-chrome-stable

# En macOS
brew install google-chrome

# En Fedora
sudo dnf install google-chrome-stable
```

### Error: "chromedriver permission denied"
```bash
# webdriver-manager lo maneja automáticamente
# Pero si lo hiciste manualmente:
chmod +x /ruta/a/chromedriver
```

### Error: "Element not found" o XPath inválido
- WhatsApp Web cambia sus XPath ocasionalmente
- Necesitarás actualizar los XPath en `main.py`
- Usa Chrome DevTools (F12) para inspeccionar elementos

### Chrome abre pero no conecta
- Asegúrate de escanear el código QR
- Espera a que la sesión se cargue completamente
- Aumenta `WAIT_TIME` en main.py si es necesario

### Mensajes no se guardan
- Verifica que `messages.json` sea creado en la carpeta del proyecto
- Asegúrate de que el chat tiene mensajes visibles
- Revisa los logs en la consola para errores

---

## 📁 Estructura del Proyecto

```
Whatsapp-Web-Automation-Python-AI/
├── main.py                    # Script principal
├── misc.py                    # Código experimental (OpenAI, MySQL, audio)
├── requirements.txt           # Dependencias Python
├── test_setup.py             # Script de prueba
├── INSTALL_SETUP.md          # Esta guía
├── README.md                 # Documentación original
├── messages.json             # Mensajes extraídos (se genera)
├── chrome/
│   └── userdata/             # Sesión de Chrome (se crea automáticamente)
└── LICENSE
```

---

## 🚀 Próximos Pasos

Una vez instalado, puedes:

### 1. **Extraer Mensajes Regularmente**
```bash
# Agregar a cron para ejecutar cada hora
0 * * * * cd /home/jose/Repositorios/Whatsapp-Web-Automation-Python-AI && source venv/bin/activate && python main.py
```

### 2. **Procesar Datos**
Los datos en `messages.json` pueden procesarse con:
- Pandas para análisis
- SQLite/MySQL para almacenamiento
- Machine Learning para clasificación

### 3. **Integrar con OpenAI**
El proyecto tiene código en `misc.py` para:
- Generar respuestas automáticas con ChatGPT
- Procesar notas de voz
- Almacenar en base de datos MySQL

---

## ⚖️ Aclaraciones Legales

- Este es un proyecto **experimental y educativo**
- No usa la API oficial de WhatsApp (porque no existe para usuarios personales)
- **No está permitido** para:
  - Spam o envío masivo
  - Robo de datos
  - Acceso no autorizado
  - Fines comerciales sin permiso
- **Úsalo responsablemente** solo para automatización personal

---

## 📞 Soporte

Si encuentras problemas:

1. Ejecuta `python test_setup.py` para diagnóstico
2. Revisa los logs en la consola
3. Consulta el repositorio original: https://github.com/Jersk/Whatsapp-Web-Automation-Python-AI
4. Inspecciona los XPath con Chrome DevTools (F12)

---

**Instalación completada**: ✅ 2024-12-18
**Versión**: main.py mejorado con webdriver-manager
**Estado**: Listo para usar
