import csv
import os.path
import time

import openpyexcel
import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

from logs.logger import logger
from pre_question_spider import pre_question_spider


def spider(universities_code_path):
    universities_code = []

    # 读取各大学编号
    with open(universities_code_path, 'r', encoding='utf-8') as file:
        universities_code = file.readlines()
        file.close()

    # 对各大学数据爬取前进行预处理
    for item in universities_code:
        universities_name, forumid = item.split(':')
        # print('name: ' + universities_name)
        # print('code: ' + forumid[:-1])
        print('------------------------')
        print('开始爬取{}的招生问题'.format(universities_name))
        logger.info('开始爬取{}的招生问题'.format(universities_name))
        print('------------------------')
        if not os.path.exists('./data/questions'):
            os.makedirs('./data/questions')
        file_path = './data/questions/{}.csv'.format(universities_name)
        spider_to_csv(file_path, forumid[:-1])
        time.sleep(20)
    pass


def spider_to_csv(file_path, code):
    # print(file_path + ': ' + code)
    with open(file_path, 'w', encoding='utf-8') as file:
        # 设置csv写入变量
        writer = csv.writer(file)
        # 设置csv文件标题头
        writer.writerow(['ID','标签', '问题', '答案'])
        # 获取最大页数
        response = requests.get(
            'https://gaokao.chsi.com.cn/zxdy/forum--method-listDefault,{},year-2017,start-{}.dhtml'.format(
                code, 0))
        # 解析网页信息
        soup = BeautifulSoup(response.content, 'lxml')
        numbers = soup.find_all('li', attrs={"class": "lip"})
        max_page = int(numbers[-3].text) * 15
        # 设置ID
        index = 0
        # 进行数据爬取
        for page in range(0, max_page, 15):
            print('------------------------')
            print("当前页面: " + str(int(page / 15)))
            logger.info("当前页面: " + str(int(page / 15)))
            print('------------------------')
            try:
                response = requests.get(
                    'https://gaokao.chsi.com.cn/zxdy/forum--method-listDefault,{},year-2017,start-{}.dhtml'.format(
                        code, page))
            except HTTPError as e:
                logger.error(e)
            soup = BeautifulSoup(response.content, 'lxml')
            # 找到该页面所有问题和答案
            questions = soup.find_all('div', attrs={"class": "question"})
            answers = soup.find_all('div', attrs={"class": "question_a"})
            if page != max_page - 15:
                questions = questions[5:]
                answers = answers[5:]
            for question, answer in zip(questions, answers):
                question = question.text.replace(" ", "").replace("\r\n", "").replace("\n", "")
                answer = answer.text.replace("\r\n", "").replace("\n", "").replace(" ", "")[5:]
                # print('ID: ' + index.__str__() + ' - ''question: ', question, ' - ', 'answer: ', answer)
                logger.info('ID: ' + str(index) + ' - ' + 'question: ' + question + ' - ' + 'answer: ' + answer)
                writer.writerow([index, 0, question, answer])
                index += 1
            time.sleep(2)
        file.close()
    pass


def spider_to_excel(province_id):
    page = 0
    max_page = 0
    print("创建Excel")
    book = openpyexcel.Workbook()
    sheet = book.active
    sheet.cell(1, 1, value="ID")
    sheet.cell(1, 2, value="问题")
    sheet.cell(1, 3, value="答案")
    index = 2
    print("获取最大页数")
    forumid_list = pre_question_spider(province_id)
    for forumid in forumid_list:
        if page == 0:
            response = requests.get(
                'https://gaokao.chsi.com.cn/zxdy/forum--method-listDefault,{},year-2005,start-{}.dhtml'.format(
                    forumid, page))
            soup = BeautifulSoup(response.content, 'lxml')
            numbers = soup.find_all('li', attrs={"class": "lip"})
            max_page = int(numbers[-3].text) * 15
            # print(numbers[-3].text)
        print("爬取问题和答案")
        for page in range(0, max_page, 15):
            print("page: ", page)
            response = requests.get(
                'https://gaokao.chsi.com.cn/zxdy/forum--method-listDefault,{},year-2005,start-{}.dhtml'.format(
                    forumid, page))
            soup = BeautifulSoup(response.content, 'lxml')
            questions = soup.find_all('div', attrs={"class": "question"})
            answers = soup.find_all('div', attrs={"class": "question_a"})
            if page != max_page - 15:
                questions = questions[5:]
                answers = answers[5:]
            for question, answer in zip(questions, answers):
                question = question.text.replace(" ", "").replace("\r\n", "").replace("\n", "")
                answer = answer.text.replace("\r\n", "").replace("\n", "").replace(" ", "")[5:]
                print("question: ", question)
                print("answer: ", answer)
                sheet.cell(index, 1, value=index - 1)
                sheet.cell(index, 2, value=question)
                sheet.cell(index, 3, value=answer)
                index += 1
            response.close()
    print("保存Excel")
    book.save('data/question_answer.xlsx')


if __name__ == "__main__":
    logger = logger()
    universities_code_path = 'data/universities_code.txt'
    spider(universities_code_path)
