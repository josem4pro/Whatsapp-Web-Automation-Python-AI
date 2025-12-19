import time
import os
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def send_whatsapp_message(contact_name, message_text):
    # Intentar cerrar procesos previos para liberar el perfil
    print("🧹 Limpiando procesos de Chrome previos...")
    subprocess.run(["pkill", "-f", "chrome"], capture_output=True)
    time.sleep(2)

    directory_path = os.getcwd()
    userdata_path = os.path.join(directory_path, 'chrome', 'userdata')
    os.makedirs(userdata_path, exist_ok=True)

    options = Options()
    options.add_argument("user-data-dir=" + userdata_path)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("detach", True)
    # Evitar el mensaje de "Chrome está siendo controlado..."
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    print(f"🚀 Iniciando Chrome para enviar mensaje a: {contact_name}...")
    try:
        service = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service, options=options)
        browser.maximize_window()
        
        browser.get('https://web.whatsapp.com/')
        
        wait = WebDriverWait(browser, 100)
        
        # Esperar a que cargue la lista de chats o el buscador
        print("⏳ Esperando a que WhatsApp Web cargue por completo...")
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="side"]')))
        print("✓ WhatsApp Web cargado.")

        # Buscar el contacto
        print(f"🔍 Buscando contacto '{contact_name}'...")
        try:
            # Intentar clickear directamente si está visible
            contact_element = browser.find_element(By.XPATH, f'//span[@title="{contact_name}"]')
            contact_element.click()
        except:
            # Si no está visible, usar el buscador
            search_box = wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            search_box.clear()
            search_box.send_keys(contact_name)
            time.sleep(2)
            search_box.send_keys(Keys.ENTER)
        
        # Esperar a que el cuadro de mensaje esté presente
        print("⌨️ Escribiendo mensaje...")
        message_box_xpath = '//div[@contenteditable="true"][@data-tab="10"]'
        message_box = wait.until(EC.presence_of_element_located((By.XPATH, message_box_xpath)))
        
        message_box.send_keys(message_text)
        time.sleep(1)
        message_box.send_keys(Keys.ENTER)
        
        print(f"✅ MENSAJE ENVIADO: '{message_text}' a {contact_name}")
        print("📌 Navegador ABIERTO y sesión ACTIVA.")
        
        # Mantener el script vivo para que el proceso no se cierre bruscamente
        while True:
            time.sleep(100)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    send_whatsapp_message("Argentina", "Hola Argentina")
