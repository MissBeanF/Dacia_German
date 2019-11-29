import csv
from selenium import webdriver
import time
import re

if __name__ == "__main__":
    driver = webdriver.Chrome('chromedriver.exe')
    start_url = 'https://ws-public.man-mn.com/siit/mansettlementwebapp/public/client/index.html?lang=de&truck=on&filterByCountry='
    end_url = '&adressField='

    countries = []
    filename = []

    with open('countries.csv', 'r', encoding="utf-8-sig") as fr:
        reader = csv.reader(fr)
        for row in reader:
            countries.append(row[0])
            filename.append(row[1] + ".csv")

    for con in range(48, 150):
        if con == 26 or con == 98 or con == 114:
            continue
        url = start_url + countries[con] + end_url
        print(url)
        driver.get(url)
        time.sleep(5)

        # write result header
        with open(filename[con], 'a', encoding="utf-8-sig", newline='') as fwrite:
            writer = csv.writer(fwrite, lineterminator='\n')
            header = ['Company Name', 'Service Partner', 'Address','Phone Number', 'Fax', 'Email', 'Website', 
                    'LKW-Service', 'Bus-Service', 'MAN Van-Service', 'Schiffsmotoren-Service', 'Industriemotoren-Service',
                    'LKW-Verkauf', 'Bus-Verkauf', 'MAN Van-Verkauf', 'Schiffsmotoren-Verkauf', 'Industriemotoren-Verkauf',
                    'LKW-MAN_TopUsed', 'Bus-MAN_TopUsed', 'MAN Van-MAN_TopUsed', 'Schiffsmotoren-MAN_TopUsed', 'Industriemotoren-MAN_TopUsed',
                    'LKW-BusTopService', 'Bus-BusTopService', 'MAN Van-BusTopService', 'Schiffsmotoren-BusTopService', 'Industriemotoren-BusTopService',
                    'LKW-eMobility', 'Bus-eMobility', 'MAN Van-eMobility', 'Schiffsmotoren-eMobility', 'Industriemotoren-eMobility']
            writer.writerow(header)

        # get detail information url
        detail_url_list = []
        detail_urls = driver.find_elements_by_css_selector("h4>a.js_detail")
        for ii in detail_urls:
            detail_url_list.append(ii.get_attribute('href'))
        print(len(detail_url_list))
        # get detail information
        index = 0
        for i in detail_url_list:
            index += 1
            # if index < 35:
            #     continue
            print(index, ":", i)
            driver.get(i)
            time.sleep(5)
            name = driver.find_element_by_css_selector('div#basics>h1.h2').text
            try:
                service_partner = (re.sub(re.compile('<.*?>'), '', driver.find_element_by_css_selector('div#basics>p.h4').get_attribute('innerHTML'))).replace('"', '-').replace("\n", " ").replace('&amp;', "&").strip()
            except:
                service_partner = ""
            try:
                address = driver.find_elements_by_css_selector('div#basics>div.row>div.col-sm-4.spacer-xs')[0].text.split("+")[0].replace('\n', ", ")
                print(address)
            except:
                address = ""
            try:
                phone = driver.find_element_by_css_selector('ul>li>a.icon.icon-phone').text.replace('\n', "")
            except:
                phone = ""
            try:
                fax = driver.find_element_by_css_selector('ul>li>a.icon.icon-fax').text.replace('\n', "")
            except:
                fax = ""
            try:
                email = driver.find_element_by_css_selector('ul>li>a.icon.icon-mail').text.replace('\n', "")
            except:
                email = ""
            try:
                website = driver.find_element_by_css_selector('ul>li>a.icon.icon-globe').text.replace('\n', "")
            except:
                website = ""

            # check list
            check_list_all = []
            leistungen_table = driver.find_elements_by_css_selector('#tab_offerings>tbody>tr')
            for j in range(0,5):
                td_list = leistungen_table[j].get_attribute('innerHTML').split("<td")
                check_list = []
                for k in range(1, len(td_list)):
                    td_one = td_list[k].split('</td>')[0]
                    if "inactive" in td_one:
                        check = "no"
                    elif "checkmark" in td_one:
                        check = "yes"
                    else:
                        check = ""
                    check_list.append(check)
                check_list_all.append(check_list)

            # employees
            employees_list_all = []
            employee_table_name = driver.find_elements_by_css_selector('#scrollemployees>table>tbody>tr>th')
            employee_table_position = driver.find_elements_by_css_selector('#scrollemployees>table>tbody>tr>td:nth-child(2)')
            employee_table_contact = driver.find_elements_by_css_selector('#scrollemployees>table>tbody>tr>td:nth-child(3)')
            for j in range(0,len(employee_table_name)):
                e_name = re.sub(re.compile('<.*?>'), '', employee_table_name[j].get_attribute('innerHTML'))
                e_position = re.sub(re.compile('<.*?>'), '', employee_table_position[j].get_attribute('innerHTML'))
                e_contact = re.sub(re.compile('<.*?>'), '', employee_table_contact[j].get_attribute('innerHTML'))     
                employee_list = []
                employee_list.append(e_name)
                employee_list.append(e_position)
                employee_list.append(e_contact)
                employees_list_all.append(employee_list)
            # print(employees_list_all)

            # write the result as csv file
            with open(filename[con], 'a', encoding="utf-8-sig", newline='') as fw:
                writer = csv.writer(fw, lineterminator='\n')
                temp = []
                temp.append(name)
                temp.append(service_partner)
                temp.append(address)
                temp.append(phone)
                temp.append(fax)
                temp.append(email)
                temp.append(website)
                for m in range(0, 5):
                    temp.append(check_list_all[m][0])
                    temp.append(check_list_all[m][1])
                    temp.append(check_list_all[m][2])
                    if len(check_list_all[1]) == 3:
                        temp.append("")
                        temp.append("")
                    else:
                        temp.append(check_list_all[m][3])
                        temp.append(check_list_all[m][4])
                writer.writerow(temp)
                next_row = []
                for m in range(0, len(employees_list_all)):
                    next_row.append(employees_list_all[m][0])
                    next_row.append(employees_list_all[m][1])
                    for p in employees_list_all[m][2].split("\n"):
                        next_row.append(p)
                    writer.writerow(next_row)
                    next_row[:] = []
                blank_rows = [[],[],[],[],[]]
                writer.writerows(blank_rows)
        # time.sleep(5)
        # driver.close()