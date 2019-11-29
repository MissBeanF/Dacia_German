import csv
from selenium import webdriver
import time
import re

if __name__ == "__main__":
    with open('man-mn_result_Schweiz29.csv', 'r', encoding="utf-8-sig") as fr:
        reader = csv.reader(fr)
        for row in reader:
            first_row = []
            other_rows = []
            blank_rows = [[],[],[],[],[]]
            for j in range(0, 32):
                first_row.append(row[j])
            for j in range(32, len(row), 3):
                new_row = []
                new_row.append(row[j])
                new_row.append(row[j+1])
                for k in row[j+2].split(","):
                    new_row.append(k)
                other_rows.append(new_row)
            with open('man-mn_result_Schweiz29_modify.csv', 'a', encoding="utf-8-sig", newline='') as fw:
                writer = csv.writer(fw, lineterminator='\n')
                writer.writerow(first_row)
                writer.writerows(other_rows)
                writer.writerows(blank_rows)
                