from HanlpAPI import hanlp_nlp_segment
from logs.logger import logger
from question_analyse.keyword_normalization import time_word_normalize, province_word_normalize
from similarity_calculation.sentence_similarity import SBert_semantic_similarity
from template.question_template import load_template


# 对问句进行hanlp处理
def question_segment(sentence: str):
    return hanlp_nlp_segment(sentence)


# 匹配最合适的问题模版
def best_match_template(abstract_question, template_type):
    template_path = '../template/Template/{}'.format(template_type)
    trait_dict, keyword_list, answer, questions = load_template(template_path)
    logger.info(questions)
    best_match = ''
    max_match = 0
    best_match_keyword = -1
    for question in questions:
        traits = question.split('---')[0].split('}')
        keyword = question.split('---')[1]
        temp = ''
        for trait in traits[:-1]:
            temp += trait_dict[trait[1:]] + ' '
        temp += traits[-1]
        similarity = SBert_semantic_similarity([abstract_question, temp])
        if max_match < similarity:
            best_match = question
            max_match = similarity
            best_match_keyword = int(keyword)
    # print(best_match + '---' + str(best_match_keyword))
    # print(abstract_question)

    logger.info(best_match)
    logger.info(keyword_list[best_match_keyword - 1])
    logger.info(answer[best_match_keyword - 1])

    return best_match, keyword_list[best_match_keyword - 1], answer[best_match_keyword - 1]


# 构造抽象问题
def build_abstract_question(sentence_seg: tuple):
    words = sentence_seg[0]
    natures = sentence_seg[1]
    length = len(words)
    abstract_question = ""

    for index in range(length):
        if natures[index] == 'm' or natures[index] == 't':
            abstract_question += '年份 '
        elif natures[index] == 'major':
            abstract_question += '专业 '
        elif natures[index] == 'course':
            abstract_question += '类型 '
        elif natures[index] == 'ns':
            abstract_question += '省份 '
        else:
            abstract_question += words[index] + ' '

    return abstract_question


# 抽取关键词字典 并 对省份和时间标准化
def extract_keywords(sentence_seq: tuple):
    keywords = {}
    length = len(sentence_seq[0])
    words = sentence_seq[0]
    natures = sentence_seq[1]

    for index in range(length):
        if natures[index] == 'm' or natures[index] == 't':
            normalization = time_word_normalize(words[index])
            if normalization != '':
                keywords['year'] = normalization
            else:
                keywords['year'] = words[index]
            continue
        elif natures[index] == 'major':
            keywords['major'] = words[index]
            continue
        elif natures[index] == 'course':
            keywords['course'] = words[index]
            continue
        elif natures[index] == 'ns':
            normalization = province_word_normalize(words[index])
            if normalization != '':
                keywords['province'] = normalization
            else:
                keywords['province'] = words[index]
            continue
        elif words[index].find('招生计划') != -1 \
                or words[index].find('招生') != -1 \
                or words[index].find('计划') != -1 \
                or words[index].find('招') != -1:
            keywords['type'] = 'plan'
        elif words[index].find('录取分数') != -1 \
                or words[index].find('分数') != -1 \
                or words[index].find('分') != -1 \
                or words[index].find('录取') != -1:
            keywords['type'] = 'score'

    return keywords


if __name__ == '__main__':
    logger = logger()
    question = "一七年汕头大学计算机科学与技术理工科在广东省录取人数"
    # 分词 且 词性标注
    question_seg = question_segment(question)
    # 构造抽象问句
    abstract_question = build_abstract_question(question_seg)
    # 匹配最准确的问题模版
    best_match_template(abstract_question, 'score')
    # print(extract_keywords(question_seg))
