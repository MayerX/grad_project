import time

import openpyexcel
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


class Score:

    driver = webdriver.Chrome()

    def __init__(self):
        pass

    def pre_spider(self, year, province, option, driver):
        # 年龄
        years = driver.find_element(by=By.NAME, value="nf")
        # 省份
        provinces = driver.find_element(by=By.NAME, value="sf")
        # 种类
        options = driver.find_element(by=By.NAME, value="kl")
        # 查询
        check_btn = driver.find_element(by=By.NAME, value="btn_zsjh_cx")
        Select(years).select_by_index(year)
        Select(provinces).select_by_index(province)
        Select(options).select_by_index(option)
        check_btn.click()

    def spider(self):
        driver = self.driver
        driver.get("https:zs.stu.edu.cn/lqfscxjgy.jsp?wbtreeid=1001")
        excel_row = 2
        read = openpyexcel.load_workbook('data/score.xlsx')
        sheet = read.worksheets[0]
        for year in range(6):
            for province in range(34):
                print("省份", province)
                print("-------------------------------")
                for option in range(4):
                    self.pre_spider(year, province, option, driver)
                    soup = BeautifulSoup(driver.page_source, "lxml")
                    tr_list = soup.find_all('tr')
                    for tag in tr_list[2:-1]:
                        elements = tag.get_text().split('\n')[1:-2]
                        print(elements)
                        for col in range(65, 65 + len(elements)):
                            sheet[chr(col) + str(excel_row)] = elements[col - 65]
                        excel_row += 1
                time.sleep(1)
        read.save('score.xlsx')
        read.close()

    def test(self):
        read = openpyexcel.load_workbook('data/score.xlsx')
        sheet = read.worksheets[0]
        print(sheet.values)
        pass


if __name__ == '__main__':
    score = Score()
    # score.spider()
    score.spider()
