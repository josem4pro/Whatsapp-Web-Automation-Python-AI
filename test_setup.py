#!/usr/bin/env python3
"""
Test setup script to verify all dependencies and configurations are working correctly.
This script does NOT connect to WhatsApp Web, just tests the Selenium + Chrome setup.
"""

import sys
import os

print("=" * 60)
print("Testing WhatsApp Web Automation Setup")
print("=" * 60)

# Test 1: Check Python version
print("\n[1/5] Checking Python version...")
print(f"✓ Python {sys.version.split()[0]}")
if sys.version_info < (3, 8):
    print("✗ Python 3.8+ required")
    sys.exit(1)

# Test 2: Check required packages
print("\n[2/5] Checking Python packages...")
packages = ['selenium', 'webdriver_manager', 'openai', 'mysql', 'pydub']
missing = []
for package in packages:
    try:
        __import__(package)
        print(f"✓ {package}")
    except ImportError:
        print(f"✗ {package} - NOT INSTALLED")
        missing.append(package)

if missing:
    print(f"\nMissing packages: {', '.join(missing)}")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)

# Test 3: Check Chrome installation
print("\n[3/5] Checking Chrome installation...")
import subprocess
try:
    result = subprocess.run(['google-chrome', '--version'],
                          capture_output=True, text=True, timeout=5)
    chrome_version = result.stdout.strip()
    print(f"✓ Chrome found: {chrome_version}")
except Exception as e:
    print(f"✗ Chrome not found or error: {e}")
    sys.exit(1)

# Test 4: Test webdriver-manager
print("\n[4/5] Testing webdriver-manager (downloading ChromeDriver)...")
try:
    from webdriver_manager.chrome import ChromeDriverManager
    driver_path = ChromeDriverManager().install()
    print(f"✓ ChromeDriver downloaded: {driver_path}")
    # Check if the driver is executable
    if not os.access(driver_path, os.X_OK):
        print(f"⚠ Warning: ChromeDriver is not executable")
        os.chmod(driver_path, 0o755)
        print(f"✓ Made ChromeDriver executable")
except Exception as e:
    print(f"✗ Failed to download/find ChromeDriver: {e}")
    sys.exit(1)

# Test 5: Test Selenium with Chrome (headless mode, no UI)
print("\n[5/5] Testing Selenium + Chrome connection (headless)...")
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service

    # Create userdata directory
    userdata_path = os.path.join(os.getcwd(), 'chrome', 'userdata')
    os.makedirs(userdata_path, exist_ok=True)

    # Configure Chrome options
    options = Options()
    options.add_argument("--headless")  # Run in background
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Create Chrome driver
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    # Test basic navigation
    driver.get('https://www.google.com')
    title = driver.title
    print(f"✓ Chrome browser started successfully")
    print(f"✓ Navigation test successful (page title: '{title}')")

    driver.quit()
    print(f"✓ Browser closed successfully")

except Exception as e:
    print(f"✗ Selenium + Chrome test failed: {e}")
    try:
        driver.quit()
    except:
        pass
    sys.exit(1)

# All tests passed
print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED!")
print("=" * 60)
print("\nYou can now run the main script:")
print("  source venv/bin/activate")
print("  python main.py")
print("\nIMPORTANT:")
print("  1. Open WhatsApp Web in your browser first")
print("  2. Scan the QR code when main.py starts the browser")
print("  3. Update CHAT_NAME in main.py with the contact name")
print("\nFor help:")
print("  - Check README.md")
print("  - Review main.py configuration constants")
print("=" * 60)
