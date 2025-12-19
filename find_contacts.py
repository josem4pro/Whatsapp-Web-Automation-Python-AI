#!/usr/bin/env python3
"""
Script para listar y explorar contactos disponibles en WhatsApp Web
"""

import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os

# Configuración
directory_path = os.getcwd()
userdata_path = os.path.join(directory_path, 'chrome', 'userdata')
os.makedirs(userdata_path, exist_ok=True)

# Opciones Chrome
options = Options()
options.add_argument("user-data-dir=" + userdata_path)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--remote-debugging-port=9222")

# Iniciar navegador
print("🚀 Abriendo Chrome...")
service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)
browser.maximize_window()

try:
    # Navegar a WhatsApp Web
    browser.get('https://web.whatsapp.com/')
    print("⏳ Esperando a WhatsApp Web...")
    
    # Esperar a que esté listo
    wait = WebDriverWait(browser, 600)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]')))
    
    print("✅ WhatsApp Web cargado")
    print("")
    print("=" * 60)
    print("BUSCANDO CONTACTOS...")
    print("=" * 60)
    
    # Esperar a que los chats se carguen
    time.sleep(3)
    
    # Intentar múltiples selectores para encontrar chats
    selectors = [
        '[data-testid="chat-list-item"]',
        'div[role="button"][data-testid*="chat"]',
        'div.x10l6tqk',  # Selector alternativo
        'div[aria-label*="chat"]'
    ]

    chat_items = []
    print("\n🔍 Buscando chats con múltiples selectores...\n")

    for selector in selectors:
        items = browser.find_elements(By.CSS_SELECTOR, selector)
        if items:
            print(f"✓ Selector '{selector}' encontró {len(items)} elementos")
            chat_items = items
            break

    print(f"\n✓ Encontrados {len(chat_items)} chats\n")

    # Si no encontró nada, intentar buscar por span con title
    if len(chat_items) == 0:
        print("⚠️  No se encontraron chats con selectores estándar")
        print("Buscando por nombres directos...\n")
        all_spans = browser.find_elements(By.CSS_SELECTOR, 'span[title]')
        print(f"Encontrados {len(all_spans)} elementos span con title:")
        for span in all_spans[:15]:
            title = span.get_attribute('title')
            if title:
                print(f"  - {title}")
    
    contacts = []
    
    # Extraer información de cada chat
    for i, item in enumerate(chat_items[:10], 1):  # Primeros 10
        try:
            # Obtener nombre
            name_elem = item.find_element(By.CSS_SELECTOR, 'span[title]')
            name = name_elem.get_attribute('title')
            
            # Obtener último mensaje (vista previa)
            try:
                preview_elem = item.find_element(By.CSS_SELECTOR, 'span.ggj6brxn')
                preview = preview_elem.text[:50]
            except:
                preview = "(Sin mensajes)"
            
            # Obtener tiempo
            try:
                time_elem = item.find_element(By.CSS_SELECTOR, 'span.x1rg5ohu')
                last_time = time_elem.text
            except:
                last_time = "N/A"
            
            contact = {
                'nombre': name,
                'preview': preview,
                'tiempo': last_time,
                'index': i
            }
            contacts.append(contact)
            
            print(f"{i}. {name}")
            print(f"   Preview: {preview}")
            print(f"   Último: {last_time}")
            print()
            
        except Exception as e:
            print(f"⚠️  Error procesando chat {i}: {e}")
    
    if contacts:
        print("=" * 60)
        print(f"✅ Total de contactos encontrados: {len(contacts)}")
        print("=" * 60)
        print()
        
        # Guardar lista de contactos
        with open('contactos_disponibles.json', 'w', encoding='utf-8') as f:
            json.dump(contacts, f, ensure_ascii=False, indent=2)
        
        print("💾 Contactos guardados en: contactos_disponibles.json")
        print()
        print("PRÓXIMO PASO:")
        print(f"Para extraer mensajes de cualquier contacto, edita main.py:")
        print(f'  CHAT_NAME = "{contacts[0]["nombre"]}"')
        print()
        print("Luego ejecuta: python main.py")
    else:
        print("❌ No se encontraron contactos")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

finally:
    print("\n⏳ Presiona Ctrl+C para cerrar Chrome cuando termines...")
    try:
        input()
    except:
        pass
    browser.quit()

