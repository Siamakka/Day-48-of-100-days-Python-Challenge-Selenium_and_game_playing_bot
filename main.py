from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

driver.get("https://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(By.XPATH, '//*[@id="cookie"]')
# money = driver.find_element(By.ID, "money").text
# cursor = driver.find_element(By.CSS_SELECTOR, "#buyCursor b").text.split("- ")[1]
# grandma = driver.find_element(By.CSS_SELECTOR, "#buyGrandma b").text.split("- ")[1]
# factory = driver.find_element(By.CSS_SELECTOR, "#buyFactory b").text.split("- ")[1]
# mine = driver.find_element(By.CSS_SELECTOR, "#buyMine b").text.split("- ")[1]
# shipment = driver.find_element(By.CSS_SELECTOR, "#buyShipment b").text.split("- ")[1]
# alchemy_lab = driver.find_element(By.XPATH, '//*[@id="buyAlchemy lab"]/b').text.split("- ")[1]
# portal = driver.find_element(By.CSS_SELECTOR, "#buyPortal b").text.split("- ")[1]
# time_machine = driver.find_element(By.XPATH, '//*[@id="buyTime machine"]/b').text.split("- ")[1]

cursor_rate = 0.2
grandma_rate = 1
factory_rate = 4
mine_rate = 10
shipment_rate = 20

items = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_ids = [item.get_attribute("id") for item in items]

timeout = time.time() + 150
five_min = time.time() + 60 * 30  # 5minutes

while True:
    cookie.click()

    # Every 5 seconds:
    if time.time() > timeout:

        # Get all upgrade <b> tags
        all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
        item_prices = []

        # Convert <b> text into an integer price.
        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)

        # Create dictionary of store items and prices
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_ids[n]

        # Get current cookie count
        money_element = driver.find_element(By.ID, "money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        # Find upgrades that we can currently afford
        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id

        # Purchase the most expensive affordable upgrade
        highest_price_affordable_upgrade = max(affordable_upgrades)
        print(highest_price_affordable_upgrade)
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]

        driver.find_element(By.ID, to_purchase_id).click()

        # Add another 5 seconds until the next check
        timeout = time.time() + 20

    # After 5 minutes stop the bot and check the cookies per second count.
    if time.time() > five_min:
        cookie_per_s = driver.find_element(By.ID, "cps").text
        print(cookie_per_s)
        break
