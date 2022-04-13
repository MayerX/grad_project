import pickle
import re

from logs.logger import logger

trait_dict = {"year": "年份", "major": "专业", "province": "省份", "course": "类型"}
question_template = "{year}{major}{province}{course}{keyword}"


# 所有子集
def subset(question_keyword_list: list):
    result = [[]]
    size = len(question_keyword_list)
    for i in range(size):
        for j in range(len(result)):
            result.append(result[j] + [question_keyword_list[i]])
    return result


def create_template_plan(template_path):
    plan_dict = {"number": ["招生人数", "招生计划", "招多少人", "招生计划是多少", "招生人数是多少"]}
    answer_template = ["{year}{major}{province}招收{course}{number}人，学费为{tuition}"]
    create_template(plan_dict, answer_template, template_path)
    pass


def create_template_score(template_path):
    score_dict = {"highest": ["最高分", "最高分是多少"],
                  "lowest": ["最低分", "平均分是多少"],
                  "average": ["平均分", "最低分是多少", "分数线", "分数线是多少"],
                  "number": ["录取人数", "录取多少人"]}
    answer_template = ["{year}{major}{province}{course}最高分是{highest}",
                       "{year}{major}{province}{course}最低分是{lowest}",
                       "{year}{major}{province}{course}平均分是{average}",
                       "{year}{major}{province}{course}录取人数是{number}"]
    create_template(score_dict, answer_template, template_path)
    pass


def create_template(kind_dict, answer_template, template_path):
    # 具体问题特征词列表
    keyword_list = list(kind_dict)
    # 问句模版特征词列表
    trait_list = list(trait_dict.keys())
    # 模版文件
    template_dict = {"trait_dict": trait_dict, "keyword_list": keyword_list,
                     "answer": answer_template}
    # 构建所有问题
    questions = []
    # 所有子集
    logger.info('构建该模版的所有子集')
    question_subset = subset(trait_list)
    print(keyword_list)
    logger.info('构建模版')
    for index_question in range(len(keyword_list)):
        key_list = kind_dict[keyword_list[index_question]]
        for key in key_list:
            for index_subset in question_subset:
                d_question = question_template.format(year="{year}", major="{major}", course="{course}",
                                                      province="{province}", keyword=key) + "---" + str(index_question)
                if not index_subset:
                    questions.append(d_question)
                elif len(index_subset) == len(trait_list):
                    continue
                else:
                    for index in index_subset:
                        d_question = d_question.replace("{" + index + "}", "")
                    questions.append(d_question)
    template_dict["questions"] = questions
    # print(template_dict)
    with open(template_path, "wb") as file:
        pickle.dump(template_dict, file)
    logger.info(template_dict)


def load_template(template_path: str):
    with open(template_path, "rb") as file:
        template_dict = pickle.load(file)
    return template_dict["trait_dict"], template_dict["keyword_list"], template_dict["answer"], \
           template_dict["questions"]


def build_sql_sentence(match_question_template: str, template_type: str, keywords: dict):
    slots = match_question_template.split('}')[:-1]
    sql_sentence = ""

    for slot in slots:
        value = keywords[slot[1:]]
        if value == "":
            continue
        else:
            sql_sentence += slots[1:] + "='" + value + "' and "
    if sql_sentence != "":
        sql_sentence = "select * from " + template_type + " where " + sql_sentence[:-5] + ";"

    return sql_sentence


# {year}{major}{province}{course}平均分是{average}
def build_answer(answer_template: str, sql_query: tuple):
    pattern = re.compile(r"[{].*?[}]")
    slots = re.findall(pattern, answer_template)
    answer = ''
    for slot in slots:
        answer += sql_query[slot[1:-1]]

    return answer


if __name__ == "__main__":
    logger = logger()
    create_template_score("Template/score")
    create_template_plan("Template/plan")
