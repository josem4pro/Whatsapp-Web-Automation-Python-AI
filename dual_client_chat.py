#!/usr/bin/env python3
"""
Script para manejar dos clientes de WhatsApp Web simultáneamente
Cliente 1: MarDelPlata (cuenta principal)
Cliente 2: Death Number (segunda cuenta)

Objetivo: Enviar mensaje de uno a otro y capturar la conversación
"""

import time
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def create_browser(profile_name):
    """Crea una nueva instancia de Chrome con un perfil separado"""
    profile_path = os.path.join(os.getcwd(), 'chrome', f'userdata_{profile_name}')
    os.makedirs(profile_path, exist_ok=True)

    options = Options()
    options.add_argument(f"user-data-dir={profile_path}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--remote-debugging-port=0")  # Puerto dinámico para evitar conflictos

    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)
    browser.maximize_window()

    return browser

def wait_for_whatsapp(browser, timeout=120):
    """Espera a que WhatsApp Web cargue"""
    wait = WebDriverWait(browser, timeout)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[title]')))
    time.sleep(2)

def get_contacts(browser):
    """Obtiene lista de contactos del navegador"""
    all_spans = browser.find_elements(By.CSS_SELECTOR, 'span[title]')
    contacts = {}

    for span in all_spans:
        title = span.get_attribute('title')
        if title and ('+' in title or any(c.isalpha() for c in title)):
            if title not in contacts:
                contacts[title] = span

    return contacts

def open_chat(browser, contact_name):
    """Abre un chat con un contacto"""
    contacts = get_contacts(browser)

    if contact_name not in contacts:
        print(f"❌ Contacto '{contact_name}' no encontrado")
        return False

    print(f"📲 Abriendo chat con: {contact_name}")
    browser.execute_script("arguments[0].scrollIntoView(true);", contacts[contact_name])
    time.sleep(1)
    contacts[contact_name].click()

    print("⏳ Esperando a que carguen los mensajes...")
    time.sleep(3)

    return True

def send_message(browser, message_text):
    """Envía un mensaje en el chat abierto"""
    try:
        # Buscar el área de texto para escribir
        input_elements = browser.find_elements(By.CSS_SELECTOR, '[contenteditable="true"]')

        if not input_elements:
            print("❌ No se encontró el área de texto")
            return False

        # Usar el último elemento contenteditable (usualmente es el input de mensajes)
        message_input = input_elements[-1]

        print(f"📝 Escribiendo mensaje: {message_text}")
        message_input.click()
        message_input.send_keys(message_text)

        # Enviar con Enter
        time.sleep(0.5)
        message_input.send_keys(Keys.RETURN)

        print("✅ Mensaje enviado")
        time.sleep(2)

        return True
    except Exception as e:
        print(f"❌ Error al enviar mensaje: {e}")
        return False

def get_latest_messages(browser, count=5):
    """Obtiene los últimos N mensajes del chat"""
    messages = []

    try:
        msg_elements = browser.find_elements(By.CSS_SELECTOR, 'span.copyable-text')

        # Tomar los últimos 'count' elementos
        for msg_elem in msg_elements[-count:]:
            try:
                msg_text = msg_elem.text.strip()
                if msg_text:
                    # Determinar dirección
                    parent = msg_elem
                    msg_dir = 'Unknown'
                    for _ in range(10):
                        parent = parent.find_element(By.XPATH, '..')
                        classes = parent.get_attribute('class') or ''
                        if 'message-in' in classes:
                            msg_dir = 'In'
                            break
                        elif 'message-out' in classes:
                            msg_dir = 'Out'
                            break

                    messages.append({
                        'text': msg_text,
                        'direction': msg_dir
                    })
            except:
                pass
    except Exception as e:
        print(f"⚠️  Error extrayendo mensajes: {e}")

    return messages

# ==================== MAIN ====================

print("=" * 60)
print("🚀 SISTEMA DUAL DE CLIENTES WHATSAPP")
print("=" * 60)
print()

# Clientes y configuración
clients = {
    'client1': {
        'name': 'MarDelPlata',
        'partner': 'Death Number',
        'browser': None
    },
    'client2': {
        'name': 'Death Number',
        'partner': 'MarDelPlata',
        'browser': None
    }
}

try:
    # Abrir navegadores
    print("📱 Abriendo Cliente 1 (MarDelPlata)...")
    clients['client1']['browser'] = create_browser('mardel')
    clients['client1']['browser'].get('https://web.whatsapp.com/')
    wait_for_whatsapp(clients['client1']['browser'])
    print("✅ Cliente 1 listo\n")

    print("📱 Abriendo Cliente 2 (Death Number)...")
    clients['client2']['browser'] = create_browser('death')
    clients['client2']['browser'].get('https://web.whatsapp.com/')
    wait_for_whatsapp(clients['client2']['browser'])
    print("✅ Cliente 2 listo\n")

    print("=" * 60)
    print("💬 INICIANDO CONVERSACIÓN")
    print("=" * 60)
    print()

    # Cliente 1: Enviar mensaje a Cliente 2
    print("👤 CLIENTE 1 (MarDelPlata)")
    print("-" * 60)
    if open_chat(clients['client1']['browser'], clients['client1']['partner']):
        time.sleep(1)
        message1 = "Hola Death Number! Soy Claude automatizando desde MarDelPlata 🤖"
        if send_message(clients['client1']['browser'], message1):
            print()

    # Esperar a que el mensaje llegue
    print("⏳ Esperando a que el mensaje llegue a Cliente 2...")
    time.sleep(5)

    # Cliente 2: Ver mensaje y responder
    print()
    print("👤 CLIENTE 2 (Death Number)")
    print("-" * 60)
    if open_chat(clients['client2']['browser'], clients['client2']['partner']):
        time.sleep(1)

        # Ver último mensaje recibido
        latest = get_latest_messages(clients['client2']['browser'], 2)
        if latest:
            print("📨 Últimos mensajes recibidos:")
            for msg in latest:
                print(f"  [{msg['direction']}] {msg['text']}")
            print()

        # Responder
        message2 = "¡Hola MarDelPlata! Recibí tu mensaje. Esto es automatización bidireccional 💬"
        if send_message(clients['client2']['browser'], message2):
            print()

    # Esperar respuesta
    print("⏳ Esperando respuesta...")
    time.sleep(5)

    # Cliente 1: Ver conversación completa
    print()
    print("=" * 60)
    print("📋 CONVERSACIÓN COMPLETA")
    print("=" * 60)
    print()

    print("👤 CLIENTE 1 (MarDelPlata)")
    print("-" * 60)
    messages_c1 = get_latest_messages(clients['client1']['browser'], 10)
    if messages_c1:
        for i, msg in enumerate(messages_c1, 1):
            print(f"{i}. [{msg['direction']}] {msg['text']}")
    else:
        print("Sin mensajes")

    print()
    print("👤 CLIENTE 2 (Death Number)")
    print("-" * 60)
    messages_c2 = get_latest_messages(clients['client2']['browser'], 10)
    if messages_c2:
        for i, msg in enumerate(messages_c2, 1):
            print(f"{i}. [{msg['direction']}] {msg['text']}")
    else:
        print("Sin mensajes")

    # Guardar conversación completa
    print()
    print("=" * 60)
    conversation = {
        'client1': {
            'name': 'MarDelPlata',
            'messages': messages_c1
        },
        'client2': {
            'name': 'Death Number',
            'messages': messages_c2
        },
        'status': 'success'
    }

    with open('dual_conversation.json', 'w', encoding='utf-8') as f:
        json.dump(conversation, f, ensure_ascii=False, indent=2)

    print("✅ Conversación guardada en: dual_conversation.json")
    print("=" * 60)

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

finally:
    print()
    print("⏳ Cerrando navegadores en 30 segundos...")
    time.sleep(30)

    for key, client in clients.items():
        if client['browser']:
            try:
                client['browser'].quit()
                print(f"✓ {key} cerrado")
            except:
                pass

    print("\n✅ Completado")
