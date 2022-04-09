import time
import requests
import lxml
import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


def pre_question_spider(province_id):
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(10)
    driver.set_script_timeout(10)
    try:
        driver.get('https://gaokao.chsi.com.cn/zxdy/#zx')
    except:
        driver.execute_script('window.stop()')
    forumid = []
    pro = driver.find_element(by=By.XPATH, value='//a[@name={}]'.format(province_id))
    ActionChains(driver).move_to_element(driver.find_element_by_id('yxszdSelector')).perform()
    ActionChains(driver).click(pro).perform()
    time.sleep(3)
    # next_page = driver.find_elements(by=By.XPATH, value="//li[@class='lip']")
    soup = BeautifulSoup(driver.page_source, 'lxml')
    max_page = int(soup.find_all('li')[-2].text[0])
    # print(soup.find_all('li')[-3])
    for page in range(max_page):
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        items = soup.find_all('div', class_="yx-item")
        for item in items:
            forumid.append(item.find_all('a')[0]['href'].split(',')[1])
        next_page = driver.find_element(by=By.LINK_TEXT, value='下一页')
        if next_page is not None:
            ActionChains(driver).click().perform()
        # forumid.append(soup.find_all('div', class_="yx-item")[0].find_all('a')[0]['href'].split(',')[1])
    # for id in forumid:
    #     print(id)
    return forumid


if __name__ == '__main__':
    pre_question_spider(44)
