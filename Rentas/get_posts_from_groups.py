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

# Put groups to get posts
groups = [
        "cuartosyroomieszmg"
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
    
    # Put the number of scrolls in the range function
    for i in range(20):
        print("Resting")
        time.sleep(10)
        print("Working")

        posts = feed.find_elements(By.XPATH, "*")

        print("Number of scroll: " + str(i))
        
        for post in posts[-18:]:

            # To avoid "Stale Element Exception"
            try:
                post_text = post.text
                post_code = post.get_attribute('outerHTML')
            except:
                continue

            if post_text == "":
                print('""')
            else:
                print(post_text.replace('\n', '\t')[:50])

            description = post_text.replace('\n', '\t')

            description = '"' + description + '"'
            
            # Find words in a common description of a rent
            positive = re.search(r'\b(rent[ao]|departamentos?|apartamentos?|depto\.|dpto\.|casas?|fraccionamiento|coto|recamaras?|dormitorios?|cuartos?|habitaci[óo]n(es)?|baños?|cocinas?|salas?|comedor)\b', post_text, re.IGNORECASE)

            # Find words in a common description of somebody searching for a rent or somebody selling a house
            negative1 = re.search(r'\b(busc[oóa]|venta|vende|vendo|preventa|urge|urgente|fovissste|infonavit|banjercito|cr[ée]ditos?)\b', post_text, re.IGNORECASE)

            # Find prices high enough for it to be a sale
            negative2 = re.search(r'\$ ?(\d{1,2}[,\'’]\d{3},\d{3}(\.00)?|\d{1,2}[.\'’]\d{3}\.\d{3}(,00)?|\d{3},\d{3}(\.00)?|\d{3}\.\d{3}(,00)?)', post_text, re.IGNORECASE)
            
            if positive != None:
                if negative1 == None and negative2 == None:
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

        driver.execute_script("window.scrollBy(0,8000)")
