import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome import options
from apscheduler.schedulers.background import BackgroundScheduler

chrome_options = options.Options()
chrome_options.add_experimental_option("detach", True)
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://orteil.dashnet.org/cookieclicker/")


cookie_button = driver.find_element(By.CSS_SELECTOR, "#cookieAnchor #bigCookie")


def buy_upgrades(chrome_driver):
    # Find the most expensive available upgrade
    upgrade_prices = []
    max_price = 0
    unlocked_upgrades = chrome_driver.find_elements(By.CSS_SELECTOR, ".product.unlocked.enabled > .content > .price")
    for upgrade_price in unlocked_upgrades:
        upgrade_prices.append(upgrade_price.text)

    # Click on the most expensive upgrade
    button = chrome_driver.find_element(By.ID, f"product{len(upgrade_prices) - 1}")
    button.click()


def get_cookie_stats(chrome_driver):
    total_cookies = driver.find_element(By.ID, "cookies")[0]
    per_second = driver.find_element(By.ID, "cookies")[1].split(':')[1]
    return f"Total Cookies:{total_cookies}\n{per_second} cookies/second"


# Wait a bit before to give page chance to load

time.sleep(8)
attempts = 0
while attempts < 10:
    try:
        cookie_button.click()
    except selenium.common.exceptions.StaleElementReferenceException:
        cookie_button = driver.find_element(By.CSS_SELECTOR, "#cookieAnchor #bigCookie")
    finally:
        attempts += 1


# Check the prices for available upgrades every 5 seconds
scheduler = BackgroundScheduler()
scheduler.add_job(buy_upgrades, "interval", [driver], seconds=8)
scheduler.start()

start_time = time.time()
end_time = time.time() + (1 * 60)

still_playing = True
while still_playing:
    cookie_button.click()
    time_now = time.time()
    if time_now >= end_time:
        still_playing = False
        cookie_stats = get_cookie_stats(driver)
        time_finished = time.time()
        print(cookie_stats)













