import requests
from bs4 import BeautifulSoup
import manager as man
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

aptoide_API_endpoint = config['DOWNLOAD']['aptoideAPIEndpoint']
dir = config['DOWNLOAD']['apkDownloadDir']

DEFAULT_URL = "https://en.aptoide.com/group/applications"

print("Starting web scrapping of Aptoide web site.... :-)")
print("... getting stuff from ->" + DEFAULT_URL)
response = requests.get(DEFAULT_URL)
html = BeautifulSoup(response.text, 'html.parser')

print("Extracting categories...")
categories = html.find_all(class_="aptweb-button aptweb-button--see-more")

for category in categories:
    category_location = category.find("a")['href']
    print("Entering -> " + category_location)

    category_page_response = requests.get(category_location)
    category_page_html = BeautifulSoup(category_page_response.text, 'html.parser')

    # bundle = category_page_html.find_all(class_="bundle")
    cat_button_more_location = category_page_html.find_all(class_="bundle")[2].find(class_="aptweb-button aptweb-button--see-more").find("a")['href']
    print("Now getting -> " + cat_button_more_location)

    apps_page_response = requests.get(cat_button_more_location)
    apps_page_html = BeautifulSoup(apps_page_response.text, 'html.parser')

    apps_html = apps_page_html.find_all(class_="bundle-item__info__span bundle-item__info__span--big")

    for app in apps_html:
        if app.find("a") != "None":
            app_location = app.find("a")['href']

            # print("Entering App Page -> " + app_location)

            app_page_response = requests.get(app_location)
            if app_page_response:
                app_page_html = BeautifulSoup(app_page_response.text, 'html.parser')

                info_table = app_page_html.find_all(class_="app-info__row")
                print("[" + info_table[0].find_all("td")[1].get_text() + " : " + info_table[8].find_all("td")[1].get_text() + "]")
                id_app = info_table[8].find_all("td")[1].get_text()

                # download the APK to local temp dir
                data = man.get_json_data(id_app)
                appPath = data["nodes"]["meta"]["data"]["file"]["path"]
                man.download_apk(appPath)
