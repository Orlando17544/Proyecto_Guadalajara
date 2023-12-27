from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
import time
import os

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

# group con commerce_ids: 926692934070184
# group con posts: 949521149345732

groups = [
        "1504083032972281",
        "723834411098468",
        "1200120893397632",
        "850414421695243",
        "358194791226175",
        "250866605349037",
        "rentasentlajo",
        "1205678469611086",
        "418378306327844",
        "123691638322648",
        "1180084502186534",
        "2365380587055100",
        ]

if not os.path.isfile('./commerce_ids.csv'):
    with open("commerce_ids.csv", "w") as file:
        file.write("Id,Group\n")

if not os.path.isfile('./Posts.csv'):
    with open("Posts.csv", "w") as file:
        file.write("Description,Photos,Group\n") 

if not os.path.isfile('./rejected.txt'):
    with open("rejected.txt", "w") as file:
        file.write("Description\n") 


for group in groups:

    print("Group: " + group)

    link = 'https://www.facebook.com/groups/' + group + '?sorting_setting=CHRONOLOGICAL'

    driver.get(link)

    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//div[@role="feed"]')))
        feed = driver.find_element(By.XPATH, '//div[@role="feed"]')
    except TimeoutException:
        print("There was a TimeException when trying to find the feed")

    start_position = 0

    for i in range(15):
        posts = feed.find_elements(By.XPATH, "*")

        empty_posts = 0

        print("Inicio")

        for post in posts[start_position:]:

            try:
                post_text = post.text
                post_code = post.get_attribute('outerHTML')
            except:
                continue

            if post_text == "":
                print('""')
            else:
                print(post_text.replace('\n', '\t')[:50])

            if post_text == "":
                empty_posts += 1
                if empty_posts >= 8:
                    start_position += empty_posts
                continue
            else:
                empty_posts = 0

            description = post_text.replace('\n', '\t')

            description = '"' + description + '"'

            positive = re.search(r'\b(rent[ao]|departamento|depto\.|dpto\.|casa|fraccionamiento|coto|recamaras?|cuartos?|habitaci[óo]n(es)?|baños?)\b', post_text, re.IGNORECASE)

            negative = re.search(r'\b(busc[oa]|venta|vende|vendo|preventa|urge|fovissste|infonavit|banjercito|cr[ée]ditos?)\b', post_text, re.IGNORECASE)

            if positive != None:
                if negative == None:
                    commerce_id = re.search(r'(?<=/commerce/listing/)\d+', post_code)

                    # It is a post
                    if commerce_id == None:
                        
                        photos = re.findall(r'https://www.facebook.com/photo/\?fbid=[^"]+', post_code)

                        photos = ",".join(photos)

                        photos = '"' + photos + '"'

                        with open("Posts.csv", "a") as file:
                            file.write(description + "," + photos + "," + group + "\n")

                    # It is a commerce/listing
                    else:
                        with open("commerce_ids.csv", "a") as file:
                            file.write(commerce_id.group(0) + "," + group + "\n")
                        
                else:
                    with open("rejected.txt", "a") as file:
                        file.write(description + "\n")
            else:
                with open("rejected.txt", "a") as file:
                    file.write(description + "\n")

        driver.execute_script("window.scrollBy(0,3000)")
        
        time.sleep(5)
