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

def respond_from_argentina(contact_name, message_text):
    directory_path = os.getcwd()
    # USAMOS EL PERFIL DE ARGENTINA
    userdata_path = os.path.join(directory_path, 'chrome', 'client_argentina')
    os.makedirs(userdata_path, exist_ok=True)

    options = Options()
    options.add_argument("user-data-dir=" + userdata_path)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    print(f"🚀 Iniciando sesión de ARGENTINA para responder a: {contact_name}...")
    try:
        service = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service, options=options)
        browser.maximize_window()
        
        browser.get('https://web.whatsapp.com/')
        
        wait = WebDriverWait(browser, 100)
        
        print("⏳ Esperando a que WhatsApp Web (Argentina) cargue...")
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="side"]')))
        print("✓ WhatsApp Web Argentina cargado.")

        # Buscar el contacto "Mexico"
        print(f"🔍 Buscando contacto '{contact_name}'...")
        try:
            # Intentar clickear directamente si está visible (probablemente sea el primero por el saludo reciente)
            contact_element = wait.until(EC.element_to_be_clickable((By.XPATH, f'//span[@title="{contact_name}"]')))
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
        
        # Escribir la respuesta
        print("⌨️ Escribiendo respuesta desde Argentina...")
        message_box_xpath = '//div[@contenteditable="true"][@data-tab="10"]'
        message_box = wait.until(EC.presence_of_element_located((By.XPATH, message_box_xpath)))
        
        message_box.send_keys(message_text)
        time.sleep(1)
        # message_box.send_keys(Keys.ENTER) # Descomentar para enviar realmente
        
        # El usuario pidió responder el saludo, así que enviamos
        message_box.send_keys(Keys.ENTER)
        
        print(f"✅ RESPUESTA ENVIADA DESDE ARGENTINA: '{message_text}' a {contact_name}")
        print("📌 Navegador de Argentina ABIERTO.")
        
        while True:
            time.sleep(100)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Contact Name as set in Argentina's phone: "Mexico"
    respond_from_argentina("Mexico", "Hola México! Saludos desde Argentina, recibí tu mensaje perfectamente.")
