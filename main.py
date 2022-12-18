'''
This module prints a kart race evolution from mylaptime.com.
'''

import pandas as pd
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.by import By

def get_summary_table(link: str) -> pd.DataFrame:
    '''
    Use Selenium to get summary race data from site link
    '''

    driver = webdriver.Chrome()
    driver.get(link)
    driver.implicitly_wait(1.0)
    race_link = driver.find_element(By.XPATH, "/html/body/div[2]/table/tbody/tr[3]/td[2]/a")
    race_link.click()
    driver.implicitly_wait(1.0)
    summary_table = driver.find_element(By.XPATH, "/html/body/div[3]/table/tbody")

    column_names = []
    table_dict = defaultdict(dict)
    for i, row in enumerate(summary_table.find_elements(By.XPATH, ".//tr")):
        for j, col in enumerate(row.find_elements(By.XPATH, './td')):
            if i == 0:
                column_names.append(col.get_attribute('textContent'))
            else:
                table_dict[i][column_names[j]] = col.get_attribute('textContent')

    return pd.DataFrame.from_dict(table_dict).transpose()

if __name__ == '__main__':
    race_link = 'http://www.mylaptime.com/laptime/clientes/214V20106819C9780G1X1P108/results/r3.html?evt=11226&epg=6018'

    summary_df = get_summary_table(race_link)

    a = 1.0

