import csv
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys 

if __name__ == "__main__":
    titles = []
    with open("titles.csv", 'r', encoding="utf-8-sig") as fr:
        reader = csv.reader(fr)
        for row in reader:
            titles.append(row[0])

    driver = webdriver.Chrome('chromedriver.exe')
    driver.get('https://www.dacia.at/haendlersuche.html')
    time.sleep(10)

    for i in titles:
        driver.find_element_by_css_selector('.places-search-box').clear()
        driver.find_element_by_css_selector('.places-search-box').send_keys(i)
        time.sleep(5)
        try:
            driver.find_element_by_css_selector('.pac-item.first-result-item').click()
            time.sleep(5)
        except:
            time.sleep(5)
        title = driver.find_element_by_css_selector('div.dealer-item>div.dealer-info>h3').text
        address = driver.find_element_by_css_selector('div.dealer-item>div>p.description>a').text.replace("\n", ", ")
        try:
            phone = driver.find_element_by_css_selector('.external-phone.analytics-dealer-interaction').get_attribute('href')
        except:
            phone = ""
        try:
            services = driver.find_elements_by_css_selector('div.dealer-services>ul>li')
            service_list = []
            for j in services:
                service_list.append(j.text)
        except:
            service_list = []
        print(address)
        print(phone)
        print(service_list)


        with open("result_austria2.csv", 'a', encoding='utf-8-sig', newline='') as fw:
            writer = csv.writer(fw, lineterminator='\n')
            temp = []
            temp.append(i)
            temp.append(title)
            temp.append(address)
            temp.append(phone)
            for k in service_list:
                temp.append(k)
            writer.writerow(temp)

