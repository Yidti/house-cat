import csv
from os.path import exists
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import os
import time
from house_property import HouseProperty


def _url_response(url):
    try:
        response = requests.get(url)
        if response.status_code == 404:
            print("error url")
            return False
        else:
            return True
    except Exception as e:
        print("error" + str(e))
        return False


class HouseFun:

    def __init__(self):
        self.total_page = None
        self.total_properties: list[HouseProperty] = []
        self.city = "台中市"
        self.district = "豐原區"
        self.url_house_fun = "https://buy.housefun.com.tw/region/"
        self.header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
        }
        self.url_district = ""
        self._check_url()
        self.get_properties_num()
        self.get_all_data()

    def _check_url(self):
        file_exists = exists("sample/district_url.txt")
        if not file_exists:
            with open("sample/district_url.txt", "w") as file:
                self._get_district_url()
                file.write(self.url_district)
        else:
            with open("sample/district_url.txt", "r") as file:
                url_file = file.readline()
                link_if_ok = _url_response(url_file)
                if link_if_ok:
                    self.url_district = url_file
                    print(f"{self.city}/{self.district}: {self.url_district}")
                else:
                    ans = input("Do you want to get url again?(y/n): ")
                    if ans == "y":
                        self._get_district_url()

    def _get_district_url(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(self.url_house_fun)
        time.sleep(2)
        # click select city
        driver.find_element(By.CLASS_NAME, "m-icon-chevron-down").click()
        # choose Taichung city and Fengyuan district (台中市/豐原區)
        driver.find_element(By.LINK_TEXT, self.city).click()
        driver.find_element(By.LINK_TEXT, self.district).click()
        driver.find_element(By.LINK_TEXT, "找房子").click()
        time.sleep(1)
        # get current url for a district
        self.url_district = driver.current_url
        # save url to district_url.txt
        self.save_url()
        driver.close()

    def save_url(self):
        file_exists = exists("sample/district_url.txt")
        if file_exists:
            os.remove("sample/district_url.txt")
        with open("sample/district_url.txt", "w") as file:
            file.write(self.url_district)

    def page_url_exist(self, page):
        response = requests.get(self.url_district + f"?pg={page}")
        if response.status_code == 403:
            print("403")
            return False
        else:
            return True

    def get_properties_num(self):
        response = requests.get(self.url_district, headers=self.header)
        data = response.text
        soup = BeautifulSoup(data, "html.parser")
        # how many rental properties
        properties = soup.findAll("i", {"class": "count"})[0].string.strip("(").strip(")")
        print(f"Properties: {properties}")

    def get_all_data(self):
        # get all data in every page (try page 1 to page 100)
        for index in range(100):
            page = index + 1
            if self.page_url_exist(page):
                self.get_data_page(page)
            else:
                self.total_page = page
                break

    def get_data_page(self, page_num: int):
        response = requests.get(self.url_district + f"?pg={page_num}")
        data = response.text
        soup = BeautifulSoup(data, "html.parser")
        # 1. get name of properties
        # 2. get url link of properties
        all_case_elements = soup.select(".casename a")
        print(f"Properties number:{len(all_case_elements)} at page {page_num}")
        all_names = []
        all_urls = []
        for case in all_case_elements:
            href = case["href"]
            name = case.string
            all_urls.append(f"http://buy.housefun.com.tw{href}")
            all_names.append(name)
        # 3. get address of properties
        all_address_elements = soup.select(".address-map address")
        all_addresses = [address.get_text() for address in all_address_elements]
        # 4. get price of properties
        all_price_elements = soup.select(".discount-price .number")
        all_prices = [price.get_text() for price in all_price_elements]
        # 5. get unit-price of properties
        all_unit_price_elements = soup.select(".Unit-price .wording")
        all_unit_prices = [unit_price.get_text().split("，")[0] for unit_price in all_unit_price_elements]
        # 6. get ping number of properties
        all_ping_elements = soup.select(".ping-number .number")
        all_pings = [area.get_text() for area in all_ping_elements]
        # 7. get patterns of properties
        all_pattern_elements = soup.select(".ping-pattern .pattern")
        all_patterns = [pattern.get_text() for pattern in all_pattern_elements]
        # 8. get floors of properties
        all_floor_elements = soup.select(".ping-pattern .floor")
        all_floors = [floor.get_text().strip() for floor in all_floor_elements]

        for i in range(len(all_case_elements)):
            rent_property = HouseProperty(all_names[i], all_urls[i], all_addresses[i], all_prices[i],
                                          all_unit_prices[i],
                                          all_pings[i], all_patterns[i], all_floors[i])
            self.total_properties.append(rent_property)

    def save_to_csv(self):
        filename = "sample/house_properties.csv"
        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                for index, rent in enumerate(self.total_properties):
                    writer.writerow(
                        [index, rent.name, rent.address, rent.price, rent.unit_price, rent.ping, rent.patterns,
                         rent.floors, rent.url])
        except OSError as e:
            print("OSError:", filename)
        else:
            print("Data has been saved successfully!")
