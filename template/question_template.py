import pickle

common_keyword_dict = {"year": "年份", "major": "专业", "province": "省份", "course": "科类"}
question_template = "{year}{major}{province}{course}{keyword}"


def subset(question_keyword_list: list):
    result = [[]]
    size = len(question_keyword_list)
    for i in range(size):
        for j in range(len(result)):
            result.append(result[j] + [question_keyword_list[i]])
    return result


def create_template_plan(template_path):
    plan_dict = {"number": ["招生人数", "招生计划", "招多少人", "招生计划是多少", "招生人数是多少"]}
    answer = ["{year}{major}{province}招收{type}{number}人，学费为{tuition}"]
    create_template(plan_dict, answer, template_path)


def create_template_score(template_path):
    score_dict = {"highest": ["最高分", "最高分是多少"],
                  "lowest": ["最低分", "平均分是多少"],
                  "average": ["平均分", "最低分是多少", "分数线", "分数线是多少"],
                  "number": ["录取人数", "录取多少人"]}
    answer = ["{year}{major}{province}{type}最高分是{highest}",
              "{year}{major}{province}{type}平均分是{average}",
              "{year}{major}{province}{type}最低分是{lowest}",
              "{year}{major}{province}{type}录取人数是{amount}"]
    create_template(score_dict, answer, template_path)


def create_template(kind_dict, answer, template_path):
    """
    :param kind_dict:
    :param answer:
    :param template_path:
    :return:
    """
    print("开始构建模版")
    # 问题特殊关键字
    question_keyword_list = list(kind_dict.keys())
    common_keyword_list = list(common_keyword_dict.keys())
    # 模版文件
    template_dict = {"common_keyword": common_keyword_dict, "question_keyword": question_keyword_list, "answer": answer}
    # 构建所有问题
    questions = []
    # 所有子集
    question_subset = subset(common_keyword_list)
    print(question_keyword_list)
    for index_question in range(len(question_keyword_list)):
        key_list = kind_dict[question_keyword_list[index_question]]
        print(key_list)
        for key in key_list:
            for index_subset in question_subset:
                d_question = question_template.format(year="{year}", major="{major}", course="{course}",
                                                      province="{province}", keyword=key) + "---" + str(index_question)
                if not index_subset:
                    questions.append(d_question)
                elif len(index_subset) == len(common_keyword_list):
                    continue
                else:
                    for index in index_subset:
                        d_question = d_question.replace("{" + index + "}", "")
                    questions.append(d_question)
    template_dict["questions"] = questions
    # print(template_dict)
    with open(template_path, "wb") as file:
        pickle.dump(template_dict, file)
    print(template_dict)


def load_template(template_path: str):
    with open(template_path, "rb") as file:
        template_dict = pickle.load(file)
    return template_dict["common_keyword"], template_dict["question_keyword"], template_dict["answer"], \
           template_dict["questions"]


if __name__ == "__main__":
    create_template_score("Template/score")
    create_template_plan("Template/plan")
