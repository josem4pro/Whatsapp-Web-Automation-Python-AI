import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def verify_contact(contact_name):
    directory_path = os.getcwd()
    userdata_path = os.path.join(directory_path, 'chrome', 'userdata')

    options = Options()
    options.add_argument("user-data-dir=" + userdata_path)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless=new") # Run headless for verification

    print(f"🔍 Buscando contacto: {contact_name}...")
    try:
        service = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service, options=options)
        
        browser.get('https://web.whatsapp.com/')
        
        # Wait for the main app to load
        wait = WebDriverWait(browser, 60)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[role="application"]')))
        print("✓ WhatsApp Web cargado.")

        # Search box
        search_box = wait.until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
        )
        search_box.clear()
        search_box.send_keys(contact_name)
        time.sleep(3) # Wait for search results
        
        # Look for the contact in the results
        try:
            contact = browser.find_element(By.XPATH, f'//span[@title="{contact_name}"]')
            print(f"✅ CONTACTO ENCONTRADO: {contact_name}")
            return True
        except:
            print(f"❌ Contacto '{contact_name}' no encontrado en los resultados inmediatos.")
            
            # Alternative: list visible contacts
            print("\n📋 Contactos visibles en la lista:")
            spans = browser.find_elements(By.CSS_SELECTOR, 'span[title]')
            for span in spans:
                print(f"  - {span.get_attribute('title')}")
            
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        browser.quit()

if __name__ == "__main__":
    verify_contact("Argentina")
