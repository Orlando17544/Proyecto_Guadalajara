# To delete repeated Ids in commerce_ids.csv use: 

# sort -u -t, -k1,1 commerce_ids.csv

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
ids_and_groups = [
        ["732974355709657", "926692934070184"],
        ["7333767776658598", "926692934070184"],
        ["734045232222085", "cuartosyroomieszmg"],
        ["7360799107320699", "966904140057606"],
        ["738156011521498", "926692934070184"],
        ["7410179795742263", "1447650615560237"],
        ["743698881079963", "966904140057606"],
        ["743824241067078", "926692934070184"],
        ["749129923707169", "926692934070184"],
        ["751052463376326", "124943894894711"],
        ["751431686947529", "124943894894711"],
        ["752396397109822", "1447650615560237"],
        ["7547980781930300", "926692934070184"],
        ["755289016753419", "cuartosyroomieszmg"],
        ["7566265866764790", "926692934070184"],
        ["756934316527183", "926692934070184"],
        ["7572661566089797", "309130319570465"],
        ["7588307541235899", "926692934070184"],
        ["7592334427501048", "966904140057606"],
        ["760301656250537", "2982751505128088"],
        ["763465618647835", "309130319570465"],
        ["764263292336143", "1447650615560237"],
        ["7676232739065716", "2982751505128088"],
        ["770639721722986", "529603630566325"],
        ["7743093082402788", "926692934070184"],
        ["780092967517943", "309130319570465"],
        ["785216523056134", "309130319570465"],
        ["789226739443149", "101428536996053"],
        ["795778255944937", "926692934070184"],
        ["797157775233113", "966904140057606"],
        ["798718348987105", "cuartosyroomieszmg"],
        ["799418338754169", "926692934070184"],
        ["800020371562328", "926692934070184"],
        ["800980744823070", "CasasInmueblesVentaRentaenTonala"],
        ["8020523837976029", "1212797438805604"],
        ["802189728025101", "850414421695243"],
        ["806872797921129", "400768320908843"],
        ["808918861141058", "101428536996053"],
        ["816291313681754", "6151546404957659"],
        ["818036456803092", "6151546404957659"],
        ["819492933348416", "309130319570465"],
        ["850803370133842", "309130319570465"],
        ["875435244385715", "926692934070184"],
        ["886493779915567", "353648613594897"],
        ["892312859249130", "cuartosyroomieszmg"],
        ["907279774451276", "309130319570465"],
        ["917859066492299", "309130319570465"],
        ["921769749738237", "309130319570465"],
        ["922216336281883", "309130319570465"],
        ["930570865736947", "6151546404957659"],
        ["937628864569082", "cuartosyroomieszmg"],
        ["939468701232503", "1447650615560237"],
        ["941014587673504", "1447650615560237"],
        ["944020260530982", "CasasInmueblesVentaRentaenTonala"],
        ["945390623796516", "cuartosyroomieszmg"],
        ["945519457234991", "cuartosyroomieszmg"],
        ["946946004101451", "328174782800379"],
        ["947930836994777", "309130319570465"],
        ["948074657320077", "cuartosyroomieszmg"],
        ["949070023438300", "6151546404957659"],
        ["951867836320669", "926692934070184"],
        ["954241346290473", "1447650615560237"],
        ["954915295878988", "2982751505128088"],
        ["957485149416704", "288521261823808"],
        ["960249199057756", "328174782800379"],
        ["963120082202501", "926692934070184"],
        ["969694718123624", "529603630566325"],
        ["974557880956431", "288521261823808"],
        ["977552557321182", "529603630566325"],
        ["986724503021796", "CasasInmueblesVentaRentaenTonala"],
        ["987724415978430", "443342110118758"],
        ["988186246025151", "cuartosyroomieszmg"],
        ["992873818919010", "cuartosyroomieszmg"]
        ]

if not os.path.isfile('./Rentas_commerce_ids.csv'):
    with open("Rentas_commerce_ids.csv", "w") as file:
        file.write("Latitude,Longitude,Rented,Price,Link,Google Maps link,Description,Id,Group\n")

for id_and_group in ids_and_groups:
    commerce_id = id_and_group[0]
    group = id_and_group[1]

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

    # To avoid: AttributeError: 'NoneType' object has no attribute 'group'
    if match == None and commerce_text == "" and latitude == "" and longitude == "":
        print("This commerce id is empty: " + commerce_id)
        continue
        
    price = match.group(1)

    price = price.replace('.', '')

    google_maps_link = '"https://www.google.com/maps/search/?api=1&query=' + latitude + ',' + longitude + '"'

    description = commerce_text.replace('\n', '\t')

    description = '"' + description + '"'

    with open("Rentas_commerce_ids.csv", "a") as file:
        file.write(latitude + "," + longitude + "," + rented + "," + price + "," + link + "," + google_maps_link + "," + description + "," + commerce_id + "," + group + "\n")

    time.sleep(10)
