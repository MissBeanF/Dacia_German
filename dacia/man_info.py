import csv
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys 

if __name__ == "__main__":
    driver = webdriver.Chrome('chromedriver.exe')
    start_url = 'https://de.dacia.ch/haendler-suchen.html'
    driver.get(start_url)
    time.sleep(5)

    zip_codes = []
    with open("zip_code_swi_all.csv", 'r', encoding='utf-8-sig') as fr:
        reader = csv.reader(fr)
        for row in reader:
            zip_codes.append(row[0])

    for zip in zip_codes:
        driver.find_element_by_css_selector('.places-search-box').clear()
        driver.find_element_by_css_selector('.places-search-box').send_keys(zip)
        time.sleep(15)
        try:
            driver.find_element_by_css_selector('.pac-item.first-result-item').click()
        except:
            time.sleep(3)
        time.sleep(10)
        # driver.find_element_by_css_selector('.search-cta').click()
        # time.sleep(3)
        try:
            points = driver.find_elements_by_css_selector('div.inactive-label-beta')
        except:
            time.sleep(5)
        print(len(points))
        for i in points:
            position_title = i.get_attribute("innerText")
            if position_title == "":
                position_title = i.get_attribute("title")
            if len(position_title) < 3:
                continue
            with open("titles_swi.csv", 'a', encoding='utf-8-sig', newline='') as fw:
                writer = csv.writer(fw, lineterminator='\n')
                temp = []
                temp.append(position_title)
                writer.writerow(temp)
            print(position_title)
