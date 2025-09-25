from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://weather.gov.mn")

try:
    # Wait for the element to appear
    target_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div[2]"))
    )
    print(target_element.text.strip())
except Exception as e:
    print("Error:", e)

driver.quit()