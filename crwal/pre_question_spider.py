import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


def pre_question_spider(province_id):
    # 浏览器设置
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(10)
    driver.set_script_timeout(10)
    # 超出时间则停止加载
    try:
        driver.get('https://gaokao.chsi.com.cn/zxdy/#zx')
    except:
        driver.execute_script('window.stop()')
    forumid = []
    universitie_names = []
    # 找到选择的省份链接，广东省是44
    pro = driver.find_element(by=By.XPATH, value='//a[@name={}]'.format(province_id))
    # 模拟移动光标，并点击按钮进入省份所在的所有大学
    ActionChains(driver).move_to_element(driver.find_element_by_id('yxszdSelector')).perform()
    ActionChains(driver).click(pro).perform()
    # 为防止没有加载完成设置挂载时间
    time.sleep(3)
    # 用bs4解析网页信息
    soup = BeautifulSoup(driver.page_source, 'lxml')
    # 设置该省份所在大学数的最大页数
    # max_page = int(soup.find_all('li')[-2].text[0])
    max_page = 1
    # 读取该省份所有大学在该网页的编码
    for page in range(max_page):
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        items = soup.find_all('div', class_="yx-item")
        for item in items:
            forumid.append(item.find_all('a')[0]['href'].split(',')[1])
            universitie_names.append(item.find('span', class_='yxmc-span').text)
        next_page = driver.find_element(by=By.LINK_TEXT, value='下一页')
        if next_page is not None:
            ActionChains(driver).click().perform()
    with open('data/universities_code.txt', 'w') as file:
        for index in range(universitie_names.__len__()):
            file.write(universitie_names[index] + ':' + str(forumid[index]) + '\n')
            print(universitie_names[index] + ':' + str(forumid[index]))
        file.close()
    return universitie_names, forumid


if __name__ == '__main__':
    pre_question_spider(44)
