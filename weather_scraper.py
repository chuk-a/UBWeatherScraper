from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from datetime import datetime
import os
import codecs  # ✅ Needed for UTF-8-safe writing

# Setup headless Chrome for Jenkins
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://weather.gov.mn")

wait = WebDriverWait(driver, 10)

def get_text(xpath, label):
    try:
        value = wait.until(EC.presence_of_element_located((By.XPATH, xpath))).text.strip()
        print(f"{label}: {value}")
        return value
    except Exception as e:
        print(f"{label} error:", e)
        return "N/A"

# XPaths for key weather data
updated_xpath     = "/html/body/div[1]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/p"
temperature_xpath = "/html/body/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div[2]"
wind_speed_xpath  = "/html/body/div[1]/div[2]/div/div[2]/div/div[1]/div/div[3]/div[1]/p[2]"
humidity_xpath    = "/html/body/div[1]/div[2]/div/div[2]/div/div[1]/div/div[3]/div[3]/p[2]"

# Scrape values
updated     = get_text(updated_xpath, "Updated")
temperature = get_text(temperature_xpath, "Temperature")
wind_speed  = get_text(wind_speed_xpath, "Wind Speed (m/s)")
humidity    = get_text(humidity_xpath, "Humidity")

driver.quit()

# Write to CSV with UTF-8 encoding
with open(output_path, "a", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        datetime.now().isoformat(),
        updated,
        temperature,
        wind_speed,
        humidity
    ])
