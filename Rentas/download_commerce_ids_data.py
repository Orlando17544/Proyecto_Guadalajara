from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Keys, ActionChains
import re
import time
import os

driver = webdriver.Firefox()

# Login
driver.get("https://www.facebook.com/")

with open("credentials.txt", "r") as file:
    credentials = file.read()

credentials = re.search(r'^([^,]+),(.+)', credentials)


user_email = credentials.group(1)

user_password = credentials.group(2)

email = driver.find_element(By.XPATH, '//input[@id="email"]')
ActionChains(driver).send_keys_to_element(email, user_email).perform()

time.sleep(2)

password = driver.find_element(By.XPATH, '//input[@id="pass"]')
ActionChains(driver).send_keys_to_element(password, user_password).perform()

time.sleep(2)

driver.find_element(By.XPATH, '//button[@name="login"]').click()

# Put commerce ids to get its data
commerce_ids = [
        "953766546295334",
        "910715274004243"
        ]

if not os.path.isfile('./Rentas_commerce_ids.csv'):
    with open("Rentas_commerce_ids.csv", "w") as file:
        file.write("Latitude,Longitude,Rented,Price,Link,Google Maps link,Description\n")

for commerce_id in commerce_ids:

    link = 'https://www.facebook.com/commerce/listing/' + commerce_id

    driver.get(link)

    page = driver.page_source

    location = re.search(r'"latitude":([^,]+),"longitude":([^}]+)\},"is_shipping_offered"', page)

    if location == None:
        location = re.search(r'"latitude":([^,]+),"longitude":([^}]+)\},"is_multi_variant_listing"', page)
        if location != None:
            latitude = location.group(1)
            longitude = location.group(2)
        else:
            latitude = ""
            longitude = ""
    else:
        latitude = location.group(1)
        longitude = location.group(2)

    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@style,"display") and contains(@style,"inline")]')))
    commerce_data = driver.find_element(By.XPATH, '//div[contains(@style,"display") and contains(@style,"inline")]')

    commerce_text = commerce_data.text

    match = re.search(r'Alquilado', commerce_text)

    if match == None:
        match = re.search(r'Vendido', commerce_text)
        if match != None:
            rented = 'Yes'
        else:
            rented = 'No'
    else:
        rented = 'Yes'

    match = re.search(r'\nMX\$(.+)', commerce_text)

    if match == None:
        match = re.search(r'\n\$(.+)', commerce_text)
        
    price = match.group(1)

    price = price.replace('.', '')

    google_maps_link = '"https://www.google.com/maps/search/?api=1&query=' + latitude + ',' + longitude + '"'

    description = commerce_text.replace('\n', '\t')

    description = '"' + description + '"'

    with open("Rentas_commerce_ids.csv", "a") as file:
        file.write(latitude + "," + longitude + "," + rented + "," + price + "," + link + "," + google_maps_link + "," + description + "\n")

    time.sleep(5)
