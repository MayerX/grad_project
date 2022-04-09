import openpyexcel
import requests
from bs4 import BeautifulSoup
from pre_question_spider import pre_question_spider


def spider(province_id):
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
    print("保存Excel")
    book.save('data/question_answer.xlsx')


if __name__ == "__main__":
    spider(44)
