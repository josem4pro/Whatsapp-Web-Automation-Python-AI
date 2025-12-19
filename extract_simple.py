#!/usr/bin/env python3
"""
Script simplificado para extraer mensajes de WhatsApp Web
Asume que ya está autenticado (sesión persistente en chrome/userdata)
"""

import time
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Setup
directory_path = os.getcwd()
userdata_path = os.path.join(directory_path, 'chrome', 'userdata')
os.makedirs(userdata_path, exist_ok=True)

options = Options()
options.add_argument("user-data-dir=" + userdata_path)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--remote-debugging-port=9222")

print("🚀 Abriendo Chrome...")
service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)
browser.maximize_window()

try:
    print("📱 Navegando a WhatsApp Web...")
    browser.get('https://web.whatsapp.com/')

    # Esperar a que cargue - simplemente esperar
    print("⏳ Esperando a que WhatsApp Web cargue...")
    wait = WebDriverWait(browser, 120)
    # Esperar a que aparezcan los spans (que siempre están)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[title]')))

    print("✅ WhatsApp Web cargado\n")

    time.sleep(2)

    # Buscar todos los spans con title (nombres de contactos)
    print("🔍 Buscando contactos...")
    all_spans = browser.find_elements(By.CSS_SELECTOR, 'span[title]')

    contacts = {}
    for span in all_spans:
        title = span.get_attribute('title')
        # Buscar números telefónicos
        if title and ('+54' in title or title.startswith('+')):
            if title not in contacts:
                contacts[title] = span
                print(f"  ✓ Encontrado: {title}")

    if not contacts:
        print("❌ No se encontraron contactos")
    else:
        # Usar el primer contacto
        target = list(contacts.keys())[0]
        print(f"\n📲 Abriendo chat con: {target}")

        # Scroll al elemento si es necesario
        browser.execute_script("arguments[0].scrollIntoView(true);", contacts[target])
        time.sleep(1)

        # Click en el contacto
        contacts[target].click()

        print("⏳ Esperando a que carguen los mensajes...")
        time.sleep(5)

        # Extraer mensajes - buscar spans con clase copyable-text
        print("\n💬 Extrayendo mensajes...\n")

        messages = []

        # Buscar todos los elementos que contienen mensajes
        msg_elements = browser.find_elements(By.CSS_SELECTOR, 'span.copyable-text')

        for msg_elem in msg_elements:
            try:
                msg_text = msg_elem.text.strip()
                if msg_text:  # Solo si tiene texto
                    # Determinar dirección (In/Out) mirando clases ancestros
                    parent = msg_elem
                    msg_dir = 'Unknown'
                    for _ in range(10):  # Subir hasta 10 niveles
                        parent = parent.find_element(By.XPATH, '..')
                        classes = parent.get_attribute('class') or ''
                        if 'message-in' in classes:
                            msg_dir = 'In'
                            break
                        elif 'message-out' in classes:
                            msg_dir = 'Out'
                            break

                    msg_data = {
                        'text': msg_text,
                        'direction': msg_dir,
                        'contact': target
                    }
                    messages.append(msg_data)
                    print(f"  [{msg_dir}] {msg_text}")
            except:
                pass

        # Guardar
        if messages:
            with open('messages.json', 'w', encoding='utf-8') as f:
                json.dump(messages, f, ensure_ascii=False, indent=2)

            print(f"\n✅ {len(messages)} mensajes extraídos")
            print(f"💾 Guardados en: messages.json")
        else:
            print("\n⚠️  No se extrajeron mensajes")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

finally:
    print("\n✅ Completado")
    browser.quit()
