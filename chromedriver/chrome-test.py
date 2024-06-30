import undetected_chromedriver as uc
import time
import random

def simulate_human_interaction():
    time.sleep(random.uniform(2, 5))

def test_chrome_driver(chromedriver_path, chrome_binary_path):
    try:
        options = uc.ChromeOptions()
        if chrome_binary_path:
            options.binary_location = chrome_binary_path
        
        driver = uc.Chrome(driver_executable_path=chromedriver_path, options=options)
        driver.get("https://www.google.com")
        print("ChromeDriver successfully started and opened Google.")
        
        # Simulieren Sie eine Verzögerung wie bei einem menschlichen Benutzer
        simulate_human_interaction()
        
        # Akzeptieren Sie alle Cookies, falls ein Popup erscheint
        try:
            accept_cookies_button = driver.find_element_by_xpath("//button[contains(text(), 'Ich stimme zu')]")
            accept_cookies_button.click()
            print("Cookies accepted.")
        except Exception as e:
            print("No cookies popup found or an error occurred:", e)

        # Halten Sie den Browser für 30 Sekunden offen
        time.sleep(30)
        
        driver.quit()
    except Exception as e:
        print(f"An error occurred:\n{e}")

if __name__ == "__main__":
    chromedriver_path = '/mnt/c/tmp/chromedriver-linux64/chromedriver'
    chrome_binary_path = '/mnt/c/tmp/chrome-linux64/chrome'  # Pfad zur Chrome-Binärdatei
    
    print("Überprüfe Pfade...")
    import os
    if not os.path.exists(chromedriver_path):
        print(f"ChromeDriver Pfad existiert nicht: {chromedriver_path}")
    if not os.path.exists(chrome_binary_path):
        print(f"Google Chrome Pfad existiert nicht: {chrome_binary_path}")
    
    test_chrome_driver(chromedriver_path, chrome_binary_path)