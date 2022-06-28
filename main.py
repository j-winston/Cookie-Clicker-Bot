import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("https://www.amazon.com/Instant-Pot-Air-Fryer-One-Touch/dp/B07VT23JDM/ref=sr_1_5?crid=3DJC57ABWN8W6&keywords=instapot&qid=1656421581&sprefix=instapot%2Caps%2C103&sr=8-5&th=1")

price = driver.find_elements_by_class_name("a-price-whole")
print(price)
