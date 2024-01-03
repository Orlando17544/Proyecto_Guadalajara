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

password = driver.find_element(By.XPATH, '//input[@id="pass"]')
ActionChains(driver).send_keys_to_element(password, user_password).perform()

driver.find_element(By.XPATH, '//button[@name="login"]').click()

commerce_ids = [
        "953766546295334",
        "910715274004243",
        "902780230891456",
        "902730884899325",
        "886790766325317",
        "882843676894895",
        "879406990259209",
        "874704794238266",
        "873407167570234",
        "859396265656944",
        "823702099527658",
        "815052450386367",
        "789769609220934",
        "789336472958771",
        "773549401480349",
        "765057695450510",
        "7536451206373284",
        "743456957675063",
        "741354051233678",
        "733313398373021",
        "730795525611639",
        "729649749194416",
        "727918158779575",
        "7113778172020998",
        "7087544404644689",
        "707768077670661",
        "706461798260283",
        "7044690178899372",
        "676995154625642",
        "672215845024458",
        "654777080156465",
        "653173440351595",
        "650230943990982",
        "638268018497608",
        "636045968731301",
        "630986789025601",
        "613026390876510",
        "568376228812658",
        "563095145980259",
        "403986578624260",
        "381875474236596",
        "380788501050781",
        "379459021190921",
        "377655661444501",
        "375893928429381",
        "374374084934223",
        "373179018537881",
        "373052368434388",
        "372903188602700",
        "3712829962265305",
        "3634894800094800",
        "3623549407923279",
        "3610223975958152",
        "360546026554507",
        "3589492284664833",
        "357228690046297",
        "355576350413973",
        "347797581333378",
        "344015481562890",
        "341671335383310",
        "340919935222495",
        "337556315871136",
        "325237510285356",
        "322882333804653",
        "322388733953751",
        "3223721867763278",
        "318702127583668",
        "3184835028315183",
        "318450801082822",
        "317833294367016",
        "298608736483432",
        "298562716494545",
        "2740906479391378",
        "270674106026559",
        "269701182766286",
        "264145559982246",
        "260746630342385",
        "2585881361562720",
        "25196998666565673",
        "24496795919935163",
        "24393910550255467",
        "232432176472441",
        "223477094109192",
        "2091914074504357",
        "2059251897786550",
        "201934776292110",
        "182059388253148",
        "179887791801029",
        "1785487301970889",
        "1748624305621151",
        "1744355206050786",
        "1741940959618246",
        "168079993016793",
        "1643884089472359",
        "1622059315232339",
        "1605538363608489",
        "1565819580888052",
        "1561858827895676",
        "1534102287346870",
        "1527002904766080",
        "1508124413313253",
        "1501225350704175",
        "1450195428881159",
        "1446364719615877",
        "1436242770571989",
        "1409734226615202",
        "1377023439577263",
        "1356918995196633",
        "1354822665122063",
        "1340908463227740",
        "1331690394405364",
        "1298734500825806",
        "1288268711881670",
        "1276913726330262",
        "119199141225773",
        "1142204313444985",
        "1126919625340658",
        "1115842363128607",
        "1107016630666835",
        "1097897134579217",
        "1096266941818468",
        "1094571275056457",
        "1092738688825134",
        "1086754792515952",
        "1084994435861629",
        "1082893929413721",
        "1082607306257646",
        "1080042536355549",
        "1077219250129034",
        "1066744067993890",
        "1060402331941213",
        "1053262622579102",
        "1050682606250246",
        "1047312683184142",
        "1045340390079678",
        "1036378290980174",
        "1033415091051818",
        "1022804422165990",
        "1021410969135182",
        "1012629546487297",
        "1003024424102516"
        ]

#with open("Rentas_commerce_ids.csv", "w") as file:
#    file.write("Latitude,Longitude,Price,Link,Google Maps link,Description\n")

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

    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@style,"display") and contains(@style,"inline")]')))
    commerce_data = driver.find_element(By.XPATH, '//div[contains(@style,"display") and contains(@style,"inline")]')

    commerce_text = commerce_data.text

    match = re.search(r'\nMX\$(.+)', commerce_text)

    if match == None:
        match = re.search(r'\n\$(.+)', commerce_text)
        
    price = match.group(1)

    price = price.replace('.', '')

    google_maps_link = '"https://www.google.com/maps/search/?api=1&query=' + latitude + ',' + longitude + '"'

    description = commerce_text.replace('\n', '\t')

    description = '"' + description + '"'

    with open("Rentas_commerce_ids.csv", "a") as file:
        file.write(latitude + "," + longitude + "," + price + "," + link + "," + google_maps_link + "," + description + "\n")

    time.sleep(5)
