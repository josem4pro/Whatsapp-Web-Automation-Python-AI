#!/usr/bin/env python3
"""Debug script para explorar estructura de WhatsApp Web"""

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

directory_path = os.getcwd()
userdata_path = os.path.join(directory_path, 'chrome', 'userdata')
os.makedirs(userdata_path, exist_ok=True)

options = Options()
options.add_argument("user-data-dir=" + userdata_path)
options.add_argument("--disable-blink-features=AutomationControlled")

print("🚀 Abriendo Chrome...")
service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)
browser.maximize_window()

try:
    browser.get('https://web.whatsapp.com/')
    print("⏳ Esperando 10 segundos para que cargue...")
    time.sleep(10)

    print("\n🔍 EXPLORANDO ESTRUCTURA HTML\n")

    # Ver title
    print(f"Title: {browser.title}")
    print(f"URL: {browser.current_url}")
    print()

    # Buscar diferentes elementos clave
    print("📊 Elementos encontrados:")

    # 1. Elemento main/app
    mains = browser.find_elements(By.TAG_NAME, 'main')
    print(f"  - <main>: {len(mains)}")

    # 2. Divs con role
    app_divs = browser.find_elements(By.CSS_SELECTOR, 'div[role="application"]')
    print(f"  - div[role='application']: {len(app_divs)}")

    # 3. Cualquier div grande
    all_divs = browser.find_elements(By.TAG_NAME, 'div')
    print(f"  - Total <div>: {len(all_divs)}")

    # 4. Spans con title (contactos)
    spans = browser.find_elements(By.CSS_SELECTOR, 'span[title]')
    print(f"  - span[title]: {len(spans)}")
    if spans:
        print("\n    Primeros 5:")
        for i, span in enumerate(spans[:5]):
            title = span.get_attribute('title')
            if title:
                print(f"      {i+1}. {title}")

    # 5. Elementos de chat
    chat_items = browser.find_elements(By.CSS_SELECTOR, '[data-testid="chat-list-item"]')
    print(f"\n  - [data-testid='chat-list-item']: {len(chat_items)}")

    # 6. Mensajes
    messages = browser.find_elements(By.CSS_SELECTOR, '[data-testid="msg-container"]')
    print(f"  - [data-testid='msg-container']: {len(messages)}")

    # Imprimir estructura básica del body
    print("\n📄 Primeros 2000 caracteres del HTML:")
    print(browser.page_source[:2000])

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    browser.quit()
