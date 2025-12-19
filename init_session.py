import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def init_session():
    directory_path = os.getcwd()
    userdata_path = os.path.join(directory_path, 'chrome', 'userdata')
    os.makedirs(userdata_path, exist_ok=True)

    options = Options()
    options.add_argument("user-data-dir=" + userdata_path)
    options.add_argument("--disable-blink-features=AutomationControlled")
    # We want a real browser window that the user can interact with
    # options.add_argument("--headless") # NO HEADLESS

    print("🚀 Iniciando Chrome para sesión de WhatsApp...")
    try:
        service = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service, options=options)
        browser.maximize_window()
        
        print("🌍 Navegando a WhatsApp Web...")
        browser.get('https://web.whatsapp.com/')
        
        print("\n🆔 ESPERANDO ESCANEO DE QR...")
        print("Por favor, abre WhatsApp en tu teléfono y escanea el código en la ventana que se abrió.")
        
        # Wait for the main app to load (indicates successful login)
        wait = WebDriverWait(browser, 600) # 10 minutes timeout
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[role="application"]')))
        
        print("\n✅ SESIÓN INICIADA CORRECTAMENTE!")
        print("Mantendré el navegador abierto 30 segundos más para verificación.")
        time.sleep(30)
        
    except Exception as e:
        print(f"❌ Error durante la inicialización: {e}")
    finally:
        try:
            browser.quit()
            print("👋 Navegador cerrado. Los datos de sesión se guardaron en ./chrome/userdata")
        except:
            pass

if __name__ == "__main__":
    init_session()
