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

credentials = credentials.split(";")

user_email = credentials[0]

user_password = credentials[1]

email = driver.find_element(By.XPATH, '//input[@id="email"]')
ActionChains(driver).send_keys_to_element(email, user_email).perform()

time.sleep(3)

password = driver.find_element(By.XPATH, '//input[@id="pass"]')
ActionChains(driver).send_keys_to_element(password, user_password).perform()

time.sleep(3)

driver.find_element(By.XPATH, '//button[@name="login"]').click()


items = [
        "363722842979931",
        "985468302749889",
        "505498638052943",
        "1377173996229849",
        "1052162136096061",
        "592321686029830",
        "370532622063157",
        "2581137655400170",
        "1804132706706124",
        "382408304169965",
        "445827793360101",
        "1414506836127455",
        "1125143605514871",
        "593443075795498",
        "295501920070604",
        "243824651641806",
        "233528629698895",
        "156359653897197",
        "361977886390629",
        "284788314427415",
        #"722942239340368",
        "1017592886241991",
        "1024811001972809",
        "3347797385441005",
        "7305948029423902",
        "371086558618674",
        "472159955125956",
        "2413105738877398",
        "297747459390740",
        "1069142150889896",
        "905744247610767",
        "836101287428331",
        "395787207903581",
        "370241748775982",
        "1776650172786000",
        "856944246142507",
        "340216515277539",
        "660754966152456",
        "1380621809498086",
        "1547191799444501",
        "891454978989783",
        "3455955834718732",
        "825680272638092",
        "3585747618356542",
        "318421950895289",
        "725554562520858",
        "7517657608264827",
        "713189510458526",
        "211966131913051",
        "662116599420314",
        "366328192526167",
        "654675559167459",
        "902835734751118",
        "1135977604479792",
        ]

#with open("Rentas.csv", "w") as file:
#    file.write("Latitude,Longitude,Rented,Price,Link,Google Maps link,Description\n")

for item in items:

    link = 'https://www.facebook.com/marketplace/item/' + item

    driver.get(link)

    page = driver.page_source

    match = re.search(r'"latitude":([^,]+),"longitude":([^}]+)\},"is_shipping_offered"', page)

    if match == None:
        match = re.search(r'"latitude":([^,]+),"longitude":([^,]+),"reverse_geocode_detailed"', page)
        if match != None:
            latitude = match.group(1)
            longitude = match.group(2)
        else:
            latitude = ""
            longitude = ""
    else:
        latitude = match.group(1)
        longitude = match.group(2)

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

    with open("Rentas.csv", "a") as file:
        file.write(latitude + "," + longitude + "," + rented + "," + price + "," + link + "," + google_maps_link + "," + description + "\n")

    time.sleep(5)
