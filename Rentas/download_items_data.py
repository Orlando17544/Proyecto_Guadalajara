from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
import time

driver = webdriver.Firefox()

items = [
        "382408304169965",
        "445827793360101",
        "1205149113482662",
        "1414506836127455",
        "1228192601239634",
        "1125143605514871",
        "593443075795498",
        "295501920070604",
        "243824651641806",
        "233528629698895",
        "156359653897197",
        "698597268684106",
        "2697120183762431",
        "361977886390629",
        "284788314427415",
        "722942239340368",
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
        "268538105727906",
        "817803782768764",
        "370241748775982",
        "1776650172786000",
        "856944246142507",
        "340216515277539",
        "660754966152456",
        "1380621809498086",
        "1547191799444501",
        "891454978989783",
        "611264634248046",
        "3455955834718732",
        "825680272638092",
        "3585747618356542",
        "1380621732539614",
        "318421950895289",
        "725554562520858",
        "7517657608264827",
        "3372612109551926",
        "360782396692461",
        "713189510458526",
        "211966131913051",
        "746485800665132",
        "1015732202694269",
        "662116599420314",
        "366328192526167",
        "654675559167459",
        "902835734751118",
        "1135977604479792"
        ]

with open("Rentas.csv", "w") as file:
    file.write("Latitude,Longitude,Rented,Price,Link,Google Maps link,Description\n")

for item in items:

    link = 'https://www.facebook.com/marketplace/item/' + item

    driver.get(link)

    page = driver.page_source

    match = re.search('"latitude":([^,]+),"longitude":([^,]+)', page)

    latitude = match.group(1)
    longitude = match.group(2)

    main_feed = driver.find_element(By.XPATH, '//div[@data-pagelet="MainFeed"]')

    post_data = main_feed.find_element(By.XPATH, './/div[contains(@style,"display") and contains(@style,"inline")]')

    try:
        WebDriverWait(post_data, 60).until(EC.element_to_be_clickable((By.XPATH, './/span[text()="Ver más"]'))).click()
    except TimeoutException:
        print("There was a TimeException when trying to click the button")

    post_text = post_data.text

    match = re.search('Alquilado', post_text)

    if match == None:
        rented = 'No'
    else:
        rented = 'Yes'

    match = re.search('\$([^/]+)/mes', post_text)

    price = match.group(1)

    price = price.replace('.', '')

    google_maps_link = '"https://www.google.com/maps/search/?api=1&query=' + latitude + ',' + longitude + '"'

    description = post_text.replace('\n', '\t')

    description = '"' + description + '"'

    with open("Rentas.csv", "a") as file:
        file.write(latitude + "," + longitude + "," + rented + "," + price + "," + link + "," + google_maps_link + "," + description + "\n")

    time.sleep(5)
