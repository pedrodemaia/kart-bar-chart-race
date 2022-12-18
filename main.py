'''
This module prints a kart race evolution from mylaptime.com.
'''

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

if __name__ == '__main__':

    race_link = 'http://www.mylaptime.com/laptime/clientes/214V20106819C9780G1X1P108/results/r3.html?evt=11226&epg=6018'
    driver = webdriver.Chrome()
    driver.get(race_link)
    driver.implicitly_wait(1.0)
    race_link = driver.find_element(By.XPATH, "/html/body/div[2]/table/tbody/tr[3]/td[2]/a")
    race_link.click()
    driver.implicitly_wait(1.0)
    summary_table = driver.find_element(By.XPATH, "/html/body/div[3]/table/tbody")

    spec_name = []
    spec_item = []
    for row in summary_table.find_elements(By.XPATH, ".//tr"):
        spec_name.append(row.find_element(By.XPATH, './th').get_attribute('textContent'))
        spec_item.append(row.find_element(By.XPATH, './td/span').get_attribute('textContent'))

    df = pd.DataFrame({"Spec_Name": spec_name, "Spec_Title": spec_item})
    a = 1.0

