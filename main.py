from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

driver.get("https://example.com")

time.sleep(2)

input_field = driver.find_element(By.NAME, "username")
input_field.send_keys("MeinName")

time.sleep(2)
driver.quit()
