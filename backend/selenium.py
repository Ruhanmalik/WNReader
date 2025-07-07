from backend.selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


URL = input("Enter the URL you want to scrape")

service = Service(executable_path="/Users/ruhanmalik/Desktop/Workplace/Python/WebScraping/chromedriver")
driver = webdriver.Chrome(service=service)

driver.get(URL)

element = driver.find_element(By.CLASS_NAME, "chr-c")

print(element.text)

driver.quit()