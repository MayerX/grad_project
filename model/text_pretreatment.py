import csv
import re

import jieba
# 获得停用词
from wordcloud import WordCloud


def get_stopword_list(file):
    with open(file, 'r', encoding='utf-8') as f:  #
        stopword_list = [word.strip('\n') for word in f.readlines()]
    return stopword_list


# 对文本进行停用词处理
def move_stopwords(sentence_list, stopwords_list):
    # 去停用词
    out_list = []
    for word in sentence_list:
        if word not in stopwords_list:
            if not remove_digits(word):
                continue
            if word != '\t':
                out_list.append(word)
    return out_list


def remove_digits(input_str):
    punc = u'0123456789.'
    output_str = re.sub(r'[{}]+'.format(punc), '', input_str)
    return output_str


# 对句子进行中文分词
def seg_depart(sentence):
    # 对文档中的每一行进行中文分词
    sentence_depart = jieba.lcut(sentence)
    return sentence_depart


def sentence_pretreatment(file):
    stopword_list = get_stopword_list('stop_words.txt')
    text_treatment_list = []
    with open(file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            text = row[3]
            if text == '问题':
                continue
            text_seg = seg_depart(text)
            text_treatment_list.append(move_stopwords(text_seg, stopword_list))
    # print(text_treatment_list)
    return text_treatment_list


def show_word_cloud(word_str, file_name):
    wc = WordCloud(
        width=400,  # 设置宽为400px
        height=300,  # 设置高为300px
        background_color='white',  # 设置背景颜色为白色
        max_font_size=100,  # 设置最大的字体大小，所有词都不会超过100px
        min_font_size=10,  # 设置最小的字体大小，所有词都不会超过10px
        max_words=5000,  # 设置最大的单词个数
        font_path="/System/Library/fonts/PingFang.ttc"
    )
    wc.generate(word_str)
    wc.to_file(file_name)


if __name__ == '__main__':
    word_lists = sentence_pretreatment('data/question_answer.csv')
    word_str = ''
    for word_list in word_lists:
        for word in word_list:
            word_str += word + ' '
    show_word_cloud(word_str[:-1], 'word_cloud.jpg')
