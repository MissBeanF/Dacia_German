import csv
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys 

if __name__ == "__main__":
    driver = webdriver.Chrome('chromedriver.exe')
    start_url = 'https://www.ford.de/haendlersuche#/search/'
    
    zip_codes = []
    with open("zip_german.csv", 'r', encoding='utf-8-sig') as fr:
        reader = csv.reader(fr)
        for row in reader:
            zip_codes.append(row[0])

    for zip in zip_codes:
        driver.get(start_url + zip)
        time.sleep(5)
        titles = []
        title_links = []
        addresses = []
        states = []
        phones = []
        websites = []
        
        result = driver.find_elements_by_css_selector('row result ng-scope')

        titles_elements = driver.find_elements_by_css_selector('h3.dl-dealer-name.dl-dealer-name-details.ng-scope>a')
        for i in range(0, len(titles_elements)):
            titles.append(titles_elements[i].text)
            title_links.append(titles_elements[i].get_attribute('href'))

        address_elements = driver.find_elements_by_css_selector('p.dl-address-line.ng-binding')
        for i in range(0, len(address_elements)):
            if i%2 == 0:
                addresses.append(address_elements[i].text)
            else:
                states.append(address_elements[i].text)
        
        phone_elements = driver.find_elements_by_css_selector('p.dl-telephone.ng-binding')
        for i in range(0, len(phone_elements)):
            phones.append(phone_elements[i].text)

        website_elements = driver.find_elements_by_css_selector('a.ext-link.dealerWebsiteLink.ng-scope')
        for i in range(0, len(website_elements)):
            websites.append(website_elements[i].get_attribute('href'))

        with open("result_german_all_2.csv", 'a', encoding='utf-8-sig', newline='') as fw:
            print(zip, ":", len(titles), len(addresses), len(states), len(phones), len(websites))
            writer = csv.writer(fw, lineterminator='\n')
            temp = []
            for i in range(0, len(titles)):
                temp.append(titles[i])
                temp.append(title_links[i])
                temp.append(addresses[i])
                temp.append(states[i])
                temp.append(phones[i])
                temp.append(websites[i])
                writer.writerow(temp)
                temp[:] = []