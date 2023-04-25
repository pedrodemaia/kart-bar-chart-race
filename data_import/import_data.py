'''
Navegates through mylaptime.com race page, download tables and save to dataframes
'''

from typing import Tuple

import pandas as pd
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_df_from_table(table: webdriver.Firefox) -> pd.DataFrame:
    '''
    Tranform a Selenium webdriver object of a table into pandas dataframe
    '''

    column_names = []
    table_dict = defaultdict(dict)
    for i, row in enumerate(table.find_elements(By.XPATH, ".//tr")):
        for j, col in enumerate(row.find_elements(By.XPATH, './td')):
            if i == 0:
                column_names.append(col.get_attribute('textContent'))
            else:
                table_dict[i][column_names[j]] = col.get_attribute('textContent')

    return pd.DataFrame.from_dict(table_dict).transpose()
def go_to_race_page(driver: webdriver.Firefox) -> None:
    '''
    This function steps the driver from home page into race page
    '''

    driver.implicitly_wait(1.0)
    race_link = driver.find_element(By.XPATH, "/html/body/div[2]/table/tbody/tr[3]/td[2]/a")
    race_link.click()

def go_to_detailed_page(driver: webdriver.Firefox) -> None:
    '''
    This function steps the driver from race page into detailed times page
    '''

    driver.implicitly_wait(1.0)
    detailed_link = driver.find_element(By.XPATH, "/html/body/table[2]/tbody/tr/td/b/a")
    detailed_link.click()

def get_summary_table(driver: webdriver.Firefox) -> pd.DataFrame:
    '''
    Use Selenium to get summary race data from site link
    '''

    go_to_race_page(driver)
    driver.implicitly_wait(1.0)
    summary_table = driver.find_element(By.XPATH, "/html/body/div[3]/table/tbody")

    return get_df_from_table(summary_table)

def get_detailed_table(driver: webdriver.Firefox) -> pd.DataFrame:
    '''
    Use Selenium to get summary race data from site link
    '''

    go_to_detailed_page(driver)
    driver.implicitly_wait(1.0)
    times_table = driver.find_element(By.XPATH, "/html/body/table[2]/tbody/tr/td/table/tbody")

    return get_df_from_table(times_table)

def download_race_data(race_link: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    '''
    Return race tables from URL link
    '''

    driver = webdriver.Firefox()
    driver.get(race_link)
    summary_df = get_summary_table(driver)
    detailed_df = get_detailed_table(driver)
    driver.close()

    return (summary_df, detailed_df)