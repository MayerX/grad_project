from mysql_operation.mysql_operation import query_table
from question_analyse.question_pretreatment import question_segment, build_abstract_question, \
    extract_keywords, best_match_template
from template.question_template import build_sql_sentence, build_answer


def answer_question_template(question: str):
    # 分词 并 词性标注
    question_seq = question_segment(question)
    # 构造抽象问句
    abstract_question = build_abstract_question(question_seq)
    # 抽取关键词字典
    keywords = extract_keywords(question_seq)
    # 问题模版类型
    type = keywords['type']
    # 最合适的问题模版
    match_template, keyword, answer_template = best_match_template(abstract_question, type)
    # 构造sql语句
    sql_sentence = build_sql_sentence(match_template, type, keywords)
    # 数据库查询
    answer_list = []
    if sql_sentence == "":
        answer_list.append("无法构建查询语句")
    else:
        result = query_table(sql_sentence)
        if len(result) == 0:
            answer_list.append("无法查询")
        else:
            for item in result:
                answer = build_answer(answer_template, item)
                answer_list.append(answer)
    return answer_list


if __name__ == '__main__':
    print('Hello World')
