# 🚀 Procedimiento: Abrir Dos Navegadores con Dos Cuentas WhatsApp

**Fecha de creación**: 2025-12-19
**Status**: ✅ VALIDADO Y FUNCIONANDO
**Última actualización**: Sessión dual clients (ambas cuentas autenticadas)

---

## 📋 Requisitos Previos

- ✅ Virtual environment activado: `source venv/bin/activate`
- ✅ Dependencias instaladas: `pip install -r requirements.txt`
- ✅ Chrome/Chromium instalado en el sistema
- ✅ Dos números WhatsApp diferentes disponibles para escanear QR

---

## 🔑 Concepto Principal

El secreto para abrir dos navegadores sin que se interfieran es:

1. **Perfiles Chrome separados**: Cada navegador usa su propio `user-data-dir`
   - Cliente 1: `chrome/userdata_client1/`
   - Cliente 2: `chrome/userdata_client2/`
   - etc.

2. **Proceso Python persiste**: Usa `nohup` con un loop infinito para que el navegador siga abierto después que el script termine

3. **Sin esperas bloqueantes**: El script abre la página y sale inmediatamente, SIN esperar validación del usuario

---

## ✅ PROCEDIMIENTO PASO A PASO

### PASO 1: Preparar el Ambiente

```bash
cd /home/jose/Repositorios/Whatsapp-Web-Automation-Python-AI
source venv/bin/activate
```

---

### PASO 2: Abrir PRIMER Navegador (Cliente 1)

Ejecuta este comando en terminal:

```bash
nohup python3 << 'EOF' > /dev/null 2>&1 &
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os, time

# ========== CONFIGURACIÓN CLIENTE 1 ==========
PROFILE_NAME = "client1"  # ← CAMBIAR PARA CADA CLIENTE
# ===========================================

userdata = os.path.join(os.getcwd(), 'chrome', PROFILE_NAME)
os.makedirs(userdata, exist_ok=True)

options = Options()
options.add_argument(f"user-data-dir={userdata}")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--no-sandbox")

service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)
browser.maximize_window()
browser.get('https://web.whatsapp.com/')

# Mantener navegador abierto indefinidamente
while True:
    time.sleep(1)
EOF
```

**✅ Esperado**: Se abre una ventana Chrome maximizada con WhatsApp Web cargando

---

### PASO 3: Escanear QR en Cliente 1

1. Espera a que cargue WhatsApp Web (~5-10 segundos)
2. Aparecerá un código QR
3. Abre WhatsApp en tu teléfono con la primera cuenta
4. Menu → Dispositivos vinculados → Escanear código QR
5. Escanea el código en la pantalla del navegador
6. **Espera a que termine de cargar la sesión** (~30-60 segundos)

**✅ Confirmación**: Verás la lista de contactos y chats en el navegador

---

### PASO 4: Abrir SEGUNDO Navegador (Cliente 2)

Una vez validado el Cliente 1, ejecuta en una NUEVA terminal:

```bash
nohup python3 << 'EOF' > /dev/null 2>&1 &
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os, time

# ========== CONFIGURACIÓN CLIENTE 2 ==========
PROFILE_NAME = "client2"  # ← CAMBIAR PARA CADA CLIENTE
# ===========================================

userdata = os.path.join(os.getcwd(), 'chrome', PROFILE_NAME)
os.makedirs(userdata, exist_ok=True)

options = Options()
options.add_argument(f"user-data-dir={userdata}")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--no-sandbox")

service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)
browser.maximize_window()
browser.get('https://web.whatsapp.com/')

# Mantener navegador abierto indefinidamente
while True:
    time.sleep(1)
EOF
```

**✅ Esperado**: Se abre OTRA ventana Chrome con WhatsApp Web

---

### PASO 5: Escanear QR en Cliente 2

Repite el mismo proceso que PASO 3 pero con la **segunda cuenta WhatsApp**

---

## 🎯 Estado Final

Cuando ambos navegadores estén listos:

```
✅ Cliente 1 (Puerto Chrome separado)
   └─ +52 221 432 7353 (Mexico)
   └─ chrome/userdata_client1/
   └─ Session persistente

✅ Cliente 2 (Puerto Chrome separado)
   └─ +54 9 223 599-4524 (Argentina)
   └─ chrome/userdata_client2/
   └─ Session persistente
```

---

## 🔄 Próximos Pasos

Una vez ambos navegadores estén autenticados:

1. Usar `dual_client_chat.py` para enviar mensajes bidireccionales
2. Automatizar conversación entre los dos clientes
3. Extraer y guardar logs de conversación en JSON

---

## ⚠️ Troubleshooting

### Problema: Chrome se cierra inmediatamente
**Solución**: Verifica que `nohup` esté redirigiendo output correctamente
```bash
# Alternativa si nohup no funciona:
python3 << 'EOF' &
# ... código ... (sin nohup, pero con & al final)
EOF
```

### Problema: El navegador no carga WhatsApp Web
**Solución**: Espera 10-15 segundos, WhatsApp Web es lento
```bash
# Opcional: Agregar debugging
print("✅ Chrome abierto, esperando a que cargue...")
time.sleep(15)  # Aumentar este valor si es necesario
```

### Problema: Los dos navegadores interfieren entre sí
**Solución**: Verifica que usen `user-data-dir` DIFERENTES
```bash
# Validar:
ls -la chrome/
# Debe mostrar:
# chrome/userdata_client1/
# chrome/userdata_client2/
```

---

## 📚 Referencias

- Archivo principal: `dual_client_chat.py`
- Extracción de mensajes: `extract_simple.py`
- Documentación de instalación: `INSTALL_SETUP.md`

---

## ✅ Checklist para Reutilizar Este Procedimiento

- [ ] Leer este documento completo
- [ ] Activar virtual environment
- [ ] Ejecutar código Cliente 1 (cambiar `PROFILE_NAME` si es necesario)
- [ ] Escanear QR con primera cuenta
- [ ] Ejecutar código Cliente 2 (cambiar `PROFILE_NAME`)
- [ ] Escanear QR con segunda cuenta
- [ ] Verificar que ambos navegadores muestren contactos y chats
- [ ] Proceder con automatización (dual_client_chat.py, bidirectional messaging, etc.)

---

**🎯 Este es el CHECKPOINT. Si necesitas volver a abrir dos navegadores, simplemente sigue estos pasos.**
