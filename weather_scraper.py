from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import chromedriver_autoinstaller
import csv
import os
import time

# Auto-install ChromeDriver to user-writable path
custom_path = os.path.expanduser("~/.cache/chromedriver")
chromedriver_autoinstaller.install(path=custom_path)

# Setup headless Chrome for Jenkins
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 15)

def safe_get(url, retries=3, delay=10):
    for attempt in range(retries):
        try:
            driver.get(url)
            return True
        except Exception as e:
            print(f"[{datetime.now().isoformat()}] Attempt {attempt+1} failed for {url}: {e}")
            time.sleep(delay)
    return False

def get_text(xpath, label):
    try:
        value = wait.until(EC.presence_of_element_located((By.XPATH, xpath))).text.strip()
        print(f"{label}: {value}")
        return value
    except Exception as e:
        print(f"{label} error:", e)
        return "ERROR"

def scrape_weather():
    print("Scraping weather.gov.mn...")
    if not safe_get("https://weather.gov.mn"):
        return ["ERROR"] * 4
    updated     = get_text("/html/body/div[1]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/p", "Updated")
    temperature = get_text("/html/body/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div[2]", "Temperature")
    wind_speed  = get_text("/html/body/div[1]/div[2]/div/div[2]/div/div[1]/div/div[3]/div[1]/p[2]", "Wind Speed (m/s)")
    humidity    = get_text("/html/body/div[1]/div[2]/div/div[2]/div/div[1]/div/div[3]/div[3]/p[2]", "Humidity")
    return updated, temperature, wind_speed, humidity

def scrape_pm25(url, label):
    print(f"Scraping {label} PM2.5...")
    if not safe_get(url):
        return "ERROR"
    xpath = '//*[@id="main-content"]/div[3]/div[2]/div[1]/div[2]/div[2]/div/div[1]/div[3]/p'
    return get_text(xpath, f"{label} PM2.5 (µg/m³)")

# Scrape all data
updated, temperature, wind_speed, humidity = scrape_weather()
pm25_french  = scrape_pm25("https://www.iqair.com/mongolia/ulaanbaatar/ulaanbaatar/french-embassy-peace-avenue", "French Embassy")
pm25_eu      = scrape_pm25("https://www.iqair.com/mongolia/ulaanbaatar/ulaanbaatar/european-union-delegation", "EU Delegation")
pm25_czech   = scrape_pm25("https://www.iqair.com/mongolia/ulaanbaatar/ulaanbaatar/czech-embassy", "Czech Embassy")
pm25_yarmag  = scrape_pm25("https://www.iqair.com/mongolia/ulaanbaatar/ulaanbaatar/yarmag-garden-city", "Yarmag Garden City")

driver.quit()

# Define output path
output_path = os.path.join(os.getcwd(), "weather_log.csv")

# Write header if file is empty
if not os.path.exists(output_path) or os.stat(output_path).st_size == 0:
    with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp", "updated", "temperature", "wind_speed", "humidity",
            "pm25_french", "pm25_eu", "pm25_czech", "pm25_yarmag"
        ])

# Append latest data
with open(output_path, "a", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        datetime.now().isoformat(),
        updated,
        temperature,
        wind_speed,
        humidity,
        pm25_french,
        pm25_eu,
        pm25_czech,
        pm25_yarmag
    ])
