from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os, time

# ========== CONFIGURACIÓN CLIENTE ARGENTINA ==========
PROFILE_NAME = "client_argentina"
# =====================================================

userdata = os.path.join(os.getcwd(), 'chrome', PROFILE_NAME)
os.makedirs(userdata, exist_ok=True)

options = Options()
options.add_argument(f"user-data-dir={userdata}")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--no-sandbox")
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

print(f"🚀 Iniciando SEGUNDO navegador para cuenta de ARGENTINA...")
print(f"📁 Perfil: {userdata}")

try:
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)
    browser.maximize_window()
    browser.get('https://web.whatsapp.com/')

    print("\n🆔 ESPERANDO ESCANEO DE QR PARA ARGENTINA...")
    print("Por favor, usa el teléfono de Argentina para escanear el código.")

    # Mantener navegador abierto indefinidamente
    while True:
        time.sleep(100)
except Exception as e:
    print(f"❌ Error: {e}")
