from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from datetime import datetime
import os

# Configure Chrome for headless Jenkins execution
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Explicitly use installed chromedriver
service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to weather site
driver.get("https://weather.gov.mn")

try:
    # Wait for target element to load
    target_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div[2]"))
    )
    temperature = target_element.text.strip()
    print(temperature)

    # Log to CSV in Jenkins workspace
    output_path = os.path.join(os.getcwd(), "weather_log.csv")
    with open(output_path, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(), temperature])

except Exception as e:
    print("Error:", e)

finally:
    driver.quit()
