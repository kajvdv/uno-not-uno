from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
driver.get("http://localhost")

elem = driver.find_element(By.ID, "username")
elem.clear()
elem.send_keys("admin")

elem = driver.find_element(By.ID, "password")
elem.clear()
elem.send_keys("admin")

elem.send_keys(Keys.RETURN)

wait = WebDriverWait(driver, 2)
elem = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="lobby" and h1[text()="admin\'s game"]]/button[text()="Join"]')))

elem.click()


sleep(2)
driver.close()