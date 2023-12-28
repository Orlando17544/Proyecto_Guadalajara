from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Keys, ActionChains
import re
import time

driver = webdriver.Firefox()

driver.get("https://www.facebook.com/")

with open("credentials.txt", "r") as file:
    credentials = file.read()

credentials = credentials.split(",")

user_email = credentials[0]

user_password = credentials[1]

email = driver.find_element(By.XPATH, '//input[@id="email"]')
ActionChains(driver).send_keys_to_element(email, user_email).perform()

password = driver.find_element(By.XPATH, '//input[@id="pass"]')
ActionChains(driver).send_keys_to_element(password, user_password).perform()

driver.find_element(By.XPATH, '//button[@name="login"]').click()

commerce_ids = [
        "912535197129006",
        "1962905910748787",
        ]

with open("Rentas_commerce_ids.csv", "w") as file:
    file.write("Latitude,Longitude,Price,Link,Google Maps link,Description\n")

for commerce_id in commerce_ids:

    link = 'https://www.facebook.com/commerce/listing/' + commerce_id

    driver.get(link)

    page = driver.page_source

    match = re.search(r'"latitude":([^,]+),"longitude":([^}]+)\},"is_shipping_offered"', page)

    if match == None:
        match = re.search(r'"latitude":([^,]+),"longitude":([^}]+)\},"is_multi_variant_listing"', page)
        if match != None:
            latitude = match.group(1)
            longitude = match.group(2)
        else:
            latitude = ""
            longitude = ""
    else:
        latitude = match.group(1)
        longitude = match.group(2)

    commerce_data = driver.find_element(By.XPATH, '//div[contains(@style,"display") and contains(@style,"inline")]')

    commerce_text = commerce_data.text

    match = re.search(r'MX\$(.+)', commerce_text)

    price = match.group(1)

    price = price.replace('.', '')

    google_maps_link = '"https://www.google.com/maps/search/?api=1&query=' + latitude + ',' + longitude + '"'

    description = commerce_text.replace('\n', '\t')

    description = '"' + description + '"'

    with open("Rentas_commerce_ids.csv", "a") as file:
        file.write(latitude + "," + longitude + "," + price + "," + link + "," + google_maps_link + "," + description + "\n")

    time.sleep(5)
