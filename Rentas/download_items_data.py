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

# Put items to get its data
items = [
        "363722842979931",
        "985468302749889"
        ]

if not os.path.isfile('./Rentas_items.csv'):
    with open("Rentas_items.csv", "w") as file:
        file.write("Latitude,Longitude,Rented,Price,Link,Google Maps link,Description\n")

for item in items:

    link = 'https://www.facebook.com/marketplace/item/' + item

    driver.get(link)

    page = driver.page_source

    location = re.search(r'"latitude":([^,]+),"longitude":([^}]+)\},"is_shipping_offered"', page)

    if location == None:
        location = re.search(r'"latitude":([^,]+),"longitude":([^,]+),"reverse_geocode_detailed"', page)
        if location != None:
            latitude = location.group(1)
            longitude = location.group(2)
        else:
            latitude = ""
            longitude = ""
    else:
        latitude = location.group(1)
        longitude = location.group(2)

    main_feed = driver.find_element(By.XPATH, '//div[@data-pagelet="MainFeed"]')

    post_data = main_feed.find_element(By.XPATH, './/div[contains(@style,"display") and contains(@style,"inline")]')

    try:
        WebDriverWait(post_data, 15).until(EC.element_to_be_clickable((By.XPATH, './/span[text()="Ver más"]'))).click()
    except TimeoutException:
        print("There was a TimeException when trying to click the button")

    post_text = post_data.text

    match = re.search(r'Alquilado', post_text)

    if match == None:
        rented = 'No'
    else:
        rented = 'Yes'

    match = re.search(r'\$([^/]+)/mes', post_text)

    price = match.group(1)

    price = price.replace('.', '')

    google_maps_link = '"https://www.google.com/maps/search/?api=1&query=' + latitude + ',' + longitude + '"'

    description = post_text.replace('\n', '\t')

    description = '"' + description + '"'

    with open("Rentas_items.csv", "a") as file:
        file.write(latitude + "," + longitude + "," + rented + "," + price + "," + link + "," + google_maps_link + "," + description + "\n")

    time.sleep(5)